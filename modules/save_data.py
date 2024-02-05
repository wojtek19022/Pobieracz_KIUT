import os


def data_saving(response_content, output, n, i):
    # Save the response content as a GeoTIFF file
    nazwa_pliku = f"obszar_{n}_{i}.tif"

    if response_content is not None:
        with open(f"{os.path.join(output, nazwa_pliku)}", "wb") as tiff_file:
            tiff_file.write(response_content)
        print(f"GeoTIFF saved as obszar {n}_{i}.tif")

    else:
        print("NIE")
        pass
