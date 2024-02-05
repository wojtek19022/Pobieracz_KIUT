import os
import ctypes
from modules import write_links, files_searcher

# TODO uodpornienie kursora w sytuacji jeżeli istnieje plik
# TODO uproszczenie logiki działania programu (zrobienie podziału na siatkę po zakresie na wejściu)

"""
    Tytuł: Pobieracz KIUT®
    Autor: Wojciech Sołyga
    Wersja: 0.2.2
    Data publikacji: 26.11.2023 r.
"""


class KIUT_dane:
    def __init__(self):
        self.desktop = None
        self.county_code = None
        self.output = None
        i = None
        n = None
        self.order = None
        self.if_redirection = False
        self.workspace = os.getcwd()
        self.layers = []
        self.networks = [
            "przewod_wodociagowy",
            "przewod_kanalizacyjny",
            "przewod_gazowy",
            "przewod_elektroenergetyczny",
            "przewod_telekomunikacyjny",
        ]
        self.new_networks = [
            "siec_wodociagowa",
            "siec_kanalizacyjna",
            "siec_gazowa",
            "siec_elektroenergetyczna",
            "siec_telekomunikacja",
        ]
        self.download_start()

    def run(self):
        """Funkcja uruchamia wszsytkie podległe procesy do przetworzenia danych"""
        if os.path.exists(self.output):
            files_searcher.lookup_files(desktop=self.desktop, layers=self.layers)
            self.txt_file = os.path.join(self.output, "links_kiut.txt")
            write_links.save_link(
                txt_file=self.txt_file,
                county_code=self.county_code,
                layers=self.layers,
                desktop=self.desktop,
                networks=self.networks,
                new_networks=self.new_networks,
                redirection=self.if_redirection,
                output=self.output,
            )

    def success_message(self, title, text, style):
        """Funkcja zwraca komentarz o sukcesie zakończenia procesu"""
        return ctypes.windll.user32.MessageBoxW(0, text, title, style)

    def download_start(self):
        """
        Rozpoczęcie działania programu
        """
        while (
            type(self.desktop) != str()
            or type(self.county_code) != int()
            or type(self.output) != str()
        ):

            try:
                self.desktop = str(
                    input(
                        "-----------------------------------------------------"
                        "\nPodaj ścieżkę do folderu w którym są zapisane zakresy do opracowania \n"
                        "[1 zakres, to jedno zestawienie rastrów. Im mniejszy rozmiar kafla w metrach, tym dokładniejsze opracowanie!]: "
                    )
                )
                if os.path.exists(self.desktop):
                    self.county_code = int(input("Wprowadź kod miejscowości: "))
                    self.output = str(
                        input(
                            "Podaj ścieżkę do folderu w którym zostaną zapisane wynikowe rastry po przetworzeniu: "
                        )
                    )
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

        self.success_message("Sukces", "Ukończono pobieranie plików", 0)
        self.reset()

    def reset(self):
        """
        Funkcja resetująca wszystkie zmienne do domyślnych wartości
        """
        self.desktop = None
        self.county_code = None
        self.output = None
        self.order = None
        self.if_redirection = False
        self.layers.clear()


try:
    kiut_data_instance = KIUT_dane()
    # inicjalizacja klasy
    kiut_data_instance.download_start()

except KeyboardInterrupt:
    # Przekazanie tu jeżeli zabijemy proces programu
    print("\n---------------------------")
    print("Zatrzymano pracę programu")
