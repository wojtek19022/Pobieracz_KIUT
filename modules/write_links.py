import os
import fiona
from time import sleep
from requests.exceptions import HTTPError, RequestException
from shapely.geometry import shape

from .download_data import data_downloading
from .redownload import download_again


def save_link(
        txt_file, county_code, layers, desktop, networks, new_networks, redirection, output
):
    coords = {}

    with open(txt_file, "w+") as file_links:
        n = 1
        for i in layers:
            path_to_file = os.path.join(desktop, i)
            file = fiona.open(path_to_file, "r")

            for layer in file:
                for feature in file:
                    geometry = shape(feature["geometry"])
                    extent = [
                        point for point in geometry.exterior.coords
                    ]  # odczytywane są granice warstwy, która została wybrana

                    # ulx = extent[0][0]
                    # uly = extent[0][1]
                    # lrx = extent[2][0]
                    # lry = extent[2][1]

                    xmin = extent[3][0]
                    ymin = extent[3][1]
                    xmax = extent[1][0]
                    ymax = extent[1][1]

                    # extent_total_transform = f"{ulx},{uly},{lrx},{lry}"
                    extent_total = f"{xmin},{ymin},{xmax},{ymax}"

                    file_name = str(i.split("\\")[-1].split(".")[0])
                    print(f"Nazwa pliku: --- {file_name} ---")

                    coords.update({file_name: extent_total})
                    print("Extent: ", extent_total)

                    for network in networks:
                        try:
                            sleep(2)
                            redirection,response = data_downloading(
                                n=n,
                                i=network,
                                extent_total=extent_total,
                                file_links=file_links,
                                redirection=redirection,
                                county_code=county_code,
                                output=output,
                            )
                            print(response)
                        except fiona.errors.DriverError or fiona._err.CPLE_OpenFailedError as e:
                            print(f"Zły format: {e}")

                        except RequestException as e:
                            file_links.write(
                                str(
                                    f"{str(n)} {response.url.replace('png','tiff')}"
                                    ) + "\n"
                                )
                            print(f"Request failed: {e}")

                        except HTTPError as e:
                            print(f"HTTP error occurred: {e}")

                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")

            n += 1
    file_links.close()

    if redirection is True:
        print(f"Przekierowano: {redirection}")
        with open(txt_file, "r") as file_links:
            for row in file_links.readlines():
                if len(new_networks) > 1:
                    name_network = [name for name in new_networks if name in row][0]
                else:
                    name_network = new_networks[0]
                sleep(2)
                download_again(
                    county_code=county_code, output=output, value=row, name=name_network
                )
        file_links.close()
    else:
        print("Nie przekierowano łącza do serwera powiatowego pod wskazaną lokalizacją")
