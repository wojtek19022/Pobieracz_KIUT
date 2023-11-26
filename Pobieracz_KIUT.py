import fiona
from requests.exceptions import HTTPError,RequestException
from requests import request
from pathlib import Path
import os
import geopandas as gpd
import webbrowser
from time import sleep
import pyautogui
import ctypes

# TODO uodpornienie kursora w sytuacji jeżeli istnieje plik

"""
    Tytuł: Pobieracz KIUT®
    Autor: Wojciech Sołyga
    Wersja: 0.1
    Data publikacji: 26.11.2023 r.
"""

class KIUT_dane:

    def __init__(self):
        self.Desktop = None
        self.kod_powiatu = None
        self.Output = None
        i = None
        n = None
        self.polecenie = None
        self.czy_przekierowanie = False
        self.layers = []
        self.sieci = ['przewod_wodociagowy', 'przewod_kanalizacyjny', 'przewod_gazowy', 'przewod_elektroenergetyczny']
        self.new_sieci = ['siec_wodociagowa', 'siec_kanalizacyjna', 'siec_gazowa', 'siec_elektroenergetyczna']

        self.start_pobranie()

    def success_message(self,title, text, style):
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

    def zapis_danych(self,n,i):
        # Save the response content as a GeoTIFF file
        nazwa_pliku = f"obszar_{n}_{i}.tif"

        with open(f"{os.path.join(self.Output, nazwa_pliku)}", "wb") as tiff_file:
            tiff_file.write(self.polecenie.content)
        print(f"GeoTIFF saved as obszar {n}_{i}.tif")

    def przeszukanie_pliki(self):
        for i in os.listdir(self.Desktop):
            if 'id' in i.split(".")[0]:
                layer = os.path.join(self.Desktop, i)
                self.layers.append(layer)
            else:
                if i.endswith(".gpkg") or i.endswith(".shp"):
                    layer = os.path.join(self.Desktop, i)
                    self.layers.append(layer)
                else:
                    print(f"Plik {i} posiada złe rozszerzenie.")

    def poruszanie_ekran(self,value,name):
        pyautogui.moveTo(438, 64, duration=1)
        pyautogui.click(438, 64)

        pyautogui.press("enter")
        with pyautogui.hold("ctrl"):
            pyautogui.press("A")

        pyautogui.typewrite(self.Output)
        pyautogui.moveTo(195,790, duration=1)
        pyautogui.click(195,790)

        with pyautogui.hold("ctrl"):
            pyautogui.press("A")

        pyautogui.typewrite(f"Obszar_{value}_{name}")
        pyautogui.moveTo(1148, 890, duration=1)
        pyautogui.click(1148, 890)


    def ponowne_pobranie(self,value,name):
        print('Pobieranie: ', name,value.strip().replace("png","tiff"))

        # Na przyszłość: [i for i in range(5)][0]
        webbrowser.open(url=value.split(' ')[1].strip().replace("png","tiff"))
        sleep(3)
        self.poruszanie_ekran(value=value.split(' ')[0],name=name)
        sleep(1)

    def sciaganie_danych(self,n,i,extent_total,file_linki):
        parameters = {"LAYERS": i,
                      "REQUEST": "GetMap",
                      "SERVICE": "WMS",
                      "FORMAT": "image/tiff",
                      "HEIGHT": 2160,
                      "VERSION": "1.1.1",
                      "SRS": "EPSG:2180",
                      "WIDTH": 3840,
                      "BBOX": extent_total,
                      "TRANSPARENT": 'TRUE',
                      "EXCEPTIONS": 'application/vnd.ogc.se_xml'}

        main_link = f"https://integracja01.gugik.gov.pl/cgi-bin/KrajowaIntegracjaUzbrojeniaTerenu/{self.kod_powiatu}"
        polecenie = request("GET", url=main_link, params=parameters, timeout=10, allow_redirects=True)


        if polecenie.url.count("png") >= 1:
            self.czy_przekierowanie = True
            url_zapis = str(polecenie.url).replace("png", "tiff")
            file_linki.write(str(n) + ' ' + str(url_zapis) + "\n")
            print("Zapisany link: ", str(n) + ' ' + url_zapis)
        else:
            self.czy_przekierowanie = False
            print("Pobrano: ", polecenie.url)

        if polecenie.status_code == 200 and polecenie.url.count("png") == 0:
            self.zapis_danych(n,i)
        elif polecenie.url.count("png") > 0:
            pass
        else:
            print(f"Failed to fetch image. Status code: {polecenie.status_code}")

    def start_pobranie(self):
        while type(self.Desktop) != str() or type(self.kod_powiatu) != int() or type(self.Output) != str():

            try:
                self.Desktop = str(input("-----------------------------------------------------"
                    "\nPodaj ścieżkę do folderu w którym są zapisane zakresy do opracowania \n"
                                         "[1 zakres, to jedno zestawienie rastrów. Im mniejszy rozmiar kafla w metrach, tym dokładniejsze opracowanie!]: "))
                if os.path.exists(self.Desktop):
                    self.kod_powiatu = int(input("Wprowadź kod miejscowości: "))
                    self.Output = str(input("Podaj ścieżkę do folderu w którym zostaną zapisane wynikowe rastry po przetworzeniu: "))
                    print("-----------------------------------------------------")

                    if os.path.exists(self.Output):

                        self.przeszukanie_pliki()

                        plik_txt = os.path.join(self.Output,'linki_kiut.txt')
                        with open(plik_txt,'w+') as file_linki:
                            n = 1
                            for i in self.layers:
                                file = gpd.read_file(i)
                                extent_sum = file.total_bounds #odczytywane są granice warstwy, która została wybrana
                                extent = [str(i).strip() for i in extent_sum]
                                xmin = extent[0]
                                xmax = extent[2]
                                ymin = extent[1]
                                ymax = extent[3]
                                extent_total = f"{xmin},{ymin},{xmax},{ymax}"

                                print("Extent: ", extent_total)

                                for i in self.sieci:
                                    try:
                                        self.sciaganie_danych(n,i,extent_total,file_linki)

                                    except fiona.errors.DriverError or fiona._err.CPLE_OpenFailedError as e:
                                        print(f"Zły format: {e}")

                                    except RequestException as e:
                                        file_linki.write(str(f"{str(n)} https://integracja01.gugik.gov.pl/cgi-bin/KrajowaIntegracjaUzbrojeniaTerenu/{self.kod_powiatu}?LAYERS={i}&REQUEST=GetMap&SERVICE=WMS&FORMAT=image/tiff&STYLES=,,,&HEIGHT=2160&VERSION=1.1.1&SRS=EPSG:2180&WIDTH=3840&BBOX={extent_total}&TRANSPARENT=TRUE&EXCEPTIONS=application/vnd.ogc.se_xml")+"\n")
                                        print(f"Request failed: {e}")

                                    except HTTPError as e:
                                        print(f"HTTP error occurred: {e}")

                                    except Exception as e:
                                        print(f"An unexpected error occurred: {e}")

                                n += 1
                        file_linki.close()

                        print(self.czy_przekierowanie)
                        if self.czy_przekierowanie is True:
                            print(f"Przekierowano: {self.czy_przekierowanie}")
                            with open(plik_txt, 'r') as file_linki:
                                for row in file_linki.readlines():
                                    name_siec = [name for name in self.new_sieci if name in row][0]
                                    sleep(2)
                                    self.ponowne_pobranie(value=row,name=name_siec)
                                    pass
                            file_linki.close()
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

            except ValueError:
                print("Wprowadzono nieprawidłową wartość, wpisz poprawnie parametry")
            except IndexError:
                pass
            except FileNotFoundError:
                pass

        self.success_message('Sukces', 'Ukończono pobieranie plików', 0)
        self.reset()

    def reset(self):
        self.Desktop = None
        self.kod_powiatu = None
        self.Output = None
        self.polecenie = None
        self.czy_przekierowanie = False
        self.layers.clear()


# Jeżeli nie pracuję w innym programie to muszę zrobić taką instancję
# Create an instance of the class
try:
    kiut_dane_instance = KIUT_dane()
    first_start = None
    # Call the function on the instance
    kiut_dane_instance.start_pobranie()

except KeyboardInterrupt:
    # Przekazanie tu jeżeli zabijemy proces programu
    print("\n---------------------------")
    print("Zatrzymano pracę programu")