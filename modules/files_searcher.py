import os


def lookup_files(desktop, layers):
    for i in os.listdir(desktop):
        if "id" in i.split(".")[0]:
            layer = os.path.join(desktop, i)
            layers.append(layer)
        else:
            if i.endswith(".gpkg") or i.endswith(".shp"):
                layer = os.path.join(desktop, i)
                layers.append(layer)
            else:
                print(f"Plik {i} posiada złe rozszerzenie.")
