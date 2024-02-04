import os

def zapis_danych(polecenie_zawartosc,output,n, i):
    # Save the response content as a GeoTIFF file
    nazwa_pliku = f"obszar_{n}_{i}.tif"

    if polecenie_zawartosc is not None:
        with open(f"{os.path.join(output, nazwa_pliku)}", "wb") as tiff_file:
            tiff_file.write(polecenie_zawartosc)
        print(f"GeoTIFF saved as obszar {n}_{i}.tif")

    else:
        print("NIE")
        pass