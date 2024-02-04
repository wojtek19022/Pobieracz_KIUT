from time import sleep
import fiona
from shapely.geometry import shape
import os
from requests.exceptions import HTTPError,RequestException

from . import download_data,redownload,save_data

def zapisz_linki(plik_txt,kod_powiatu,layers,desktop,sieci,new_sieci,przekierowanie,output):
    coords = {}

    with open(plik_txt, 'w+') as file_linki:
        n = 1
        for i in layers:
            path_to_file = os.path.join(desktop, i)
            file = fiona.open(path_to_file, 'r')

            for layer in file:
                for feature in file:
                    geometry = shape(feature['geometry'])
                    extent = [point for point in
                              geometry.exterior.coords]  # odczytywane są granice warstwy, która została wybrana

                    ulx = extent[0][0]
                    uly = extent[0][1]
                    lrx = extent[2][0]
                    lry = extent[2][1]

                    xmin = extent[3][0]
                    ymin = extent[3][1]
                    xmax = extent[1][0]
                    ymax = extent[1][1]

                    extent_total_transform = f"{ulx},{uly},{lrx},{lry}"
                    extent_total = f"{xmin},{ymin},{xmax},{ymax}"

                    file_name = str(i.split("\\")[-1].split(".")[0])
                    print(f"Nazwa pliku: --- {file_name} ---")

                    coords.update({file_name: extent_total})
                    print("Extent: ", extent_total)

                    for i in sieci:
                        try:
                            sleep(2)
                            przekierowanie = download_data.sciaganie_danych(n=n,
                                                           i=i,
                                                           extent_total=extent_total,
                                                           file_linki=file_linki,
                                                           przekierowanie=przekierowanie,
                                                           kod_powiatu=kod_powiatu,
                                                           output=output)

                        except fiona.errors.DriverError or fiona._err.CPLE_OpenFailedError as e:
                            print(f"Zły format: {e}")

                        except RequestException as e:
                            file_linki.write(
                                str(f"{str(n)} https://integracja01.gugik.gov.pl/cgi-bin/KrajowaIntegracjaUzbrojeniaTerenu/{kod_powiatu}?LAYERS={i}&REQUEST=GetMap&SERVICE=WMS&FORMAT=image/tiff&STYLES=,,,&HEIGHT=2160&VERSION=1.1.1&SRS=EPSG:2180&WIDTH=3840&BBOX={extent_total}&TRANSPARENT=TRUE&EXCEPTIONS=application/vnd.ogc.se_xml") + "\n")
                            print(f"Request failed: {e}")

                        except HTTPError as e:
                            print(f"HTTP error occurred: {e}")

                        except Exception as e:
                            print(f"An unexpected error occurred: {e}")

            n += 1
    file_linki.close()

    if przekierowanie is True:
        print(f"Przekierowano: {przekierowanie}")
        with open(plik_txt, 'r') as file_linki:
            for row in file_linki.readlines():
                if len(new_sieci) > 1:
                    name_siec = [name for name in new_sieci if name in row][0]
                else:
                    name_siec = new_sieci[0]
                sleep(2)
                redownload.ponowne_pobranie(kod_powiatu=kod_powiatu,
                                            output=output,
                                            value=row,
                                            name=name_siec)
        file_linki.close()
    else:
        print("Nie przekierowano łącza do serwera powiatowego pod wskazaną lokalizacją")
