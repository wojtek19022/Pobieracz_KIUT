import os
import ctypes

from modules import (write_linki,files_searcher)

# TODO uodpornienie kursora w sytuacji jeżeli istnieje plik
# TODO uproszczenie logiki działania programu (zrobienie podziału na siatkę po zakresie na wejściu)

"""
    Tytuł: Pobieracz KIUT®
    Autor: Wojciech Sołyga
    Wersja: 0.2.1
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
        self.workspace = os.getcwd()
        self.layers = []
        self.sieci = ['przewod_wodociagowy', 'przewod_kanalizacyjny', 'przewod_gazowy', 'przewod_elektroenergetyczny']
        self.sieci = ['przewod_telekomunikacyjny']
        self.new_sieci = ['siec_wodociagowa', 'siec_kanalizacyjna', 'siec_gazowa', 'siec_elektroenergetyczna']
        self.new_sieci = ['siec_telekomunikacja']
        self.start_pobranie()

    def run(self):
        """Funkcja uruchamia wszsytkie podległe procesy do przetworzenia danych"""
        if os.path.exists(self.Output):
            files_searcher.przeszukanie_pliki(desktop=self.Desktop,
                                              layers=self.layers)
            self.plik_txt = os.path.join(self.Output, 'linki_kiut.txt')
            write_linki.zapisz_linki(plik_txt=self.plik_txt,
                                     kod_powiatu=self.kod_powiatu,
                                     layers=self.layers,
                                     desktop=self.Desktop,
                                     sieci=self.sieci,
                                     new_sieci = self.new_sieci,
                                     przekierowanie=self.czy_przekierowanie,
                                     output=self.Output)

    def success_message(self,title, text, style):
        """Funkcja zwraca komentarz o sukcesie zakończenia procesu"""
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

    def start_pobranie(self):
        """
        Rozpoczęcie działania programu
        """
        while type(self.Desktop) != str() or type(self.kod_powiatu) != int() or type(self.Output) != str():

            try:
                self.Desktop = str(input("-----------------------------------------------------"
                    "\nPodaj ścieżkę do folderu w którym są zapisane zakresy do opracowania \n"
                                         "[1 zakres, to jedno zestawienie rastrów. Im mniejszy rozmiar kafla w metrach, tym dokładniejsze opracowanie!]: "))
                if os.path.exists(self.Desktop):
                    self.kod_powiatu = int(input("Wprowadź kod miejscowości: "))
                    self.Output = str(input("Podaj ścieżkę do folderu w którym zostaną zapisane wynikowe rastry po przetworzeniu: "))
                    print("-----------------------------------------------------")
                    self.run()
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
        """
        Funkcja resetująca wszystkie zmienne do domyślnych wartości
        """
        self.Desktop = None
        self.kod_powiatu = None
        self.Output = None
        self.polecenie = None
        self.czy_przekierowanie = False
        self.layers.clear()

try:
    kiut_dane_instance = KIUT_dane()
    # Call the function on the instance
    kiut_dane_instance.start_pobranie()

except KeyboardInterrupt:
    # Przekazanie tu jeżeli zabijemy proces programu
    print("\n---------------------------")
    print("Zatrzymano pracę programu")