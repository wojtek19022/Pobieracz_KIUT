# Pobieracz_KIUT
Wtyczka służy do pobierania za pomocą zapytania GetMap fragmentów sieci uzbrojenia terenu. Możliwe są braki możliwości pobrania danych z powodu blokad serwerowych.

Kroki przed uruchomieniem narzędzia:
1. Przed uruchomieniem narzędzia, należy z poziomu command window przejść do ścieżki roboczej:<br>
```cd sciezka\robocza```

2. Będąc w lokalizacji ścieżki roboczej, należy wpisać poniższą komendę w celu instalacji wymaganych bibliotek:<br>
```pip install -r requirements.txt```

## Aby pobrać fragmenty sieci uzbrojenia terenu należu:
**1.** Należy prawidłowo pobrać dane:
- Dane wymagają utworzenia pliku Shapefile lub Geopackage z zakresem do pobrania w formacie powierzchniowym,
- Z utworzonego zakresu należy utworzyć regularną siatkę (np. kwadratów o równych wymiarach),
- Siatkę kwadratów należy podzielić na osobne pliki, w programie QGIS możliwe jest to przez funkcję Podziel warstwę wektorową

**2.** Ścieżkę w której znajdują się zakresy należy wpisać w pierwszym komunikacie.

**3.** W komunikacie odnoszącym się do kodu TERYT powiatu w formacie: WWPP.

**4.** Ostatni komunikat należy uzupełnić ścieżką do folderu w którym mają być przechowane wszystkie rastry wynikowe z fragmentami sieci uzbrojenia terenu.


<div align='center'>
    <br>
    <b>Autor:</b> Wojciech Sołyga <br>
    <b>Data publikacji:</b> 26.11.2023 r.<br>
    <b>Data aktualizacji:</b> 4.02.2024 r.
</div>
