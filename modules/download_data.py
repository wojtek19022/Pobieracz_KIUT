from requests import request

from . import save_data

def sciaganie_danych(n,i,extent_total,file_linki,przekierowanie,kod_powiatu,output):
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

    main_link = f"https://integracja01.gugik.gov.pl/cgi-bin/KrajowaIntegracjaUzbrojeniaTerenu/{kod_powiatu}"
    polecenie = request("GET", url=main_link, params=parameters, timeout=10, allow_redirects=True)

    if polecenie.url.count("png") >= 1:
        przekierowanie = True

        if kod_powiatu == 1465:
            url_zapis = str(polecenie.url)
        else:
            url_zapis = str(polecenie.url).replace("png", "tiff")
        file_linki.write(str(n) + ' ' + str(url_zapis) + "\n")
        print("Zapisany link: ", str(n) + ' ' + url_zapis)
    else:
        przekierowanie = False
        print("Pobrano: ", polecenie.url)

    if polecenie.status_code == 200 and polecenie.url.count("png") == 0:
        save_data.zapis_danych(polecenie_zawartosc=polecenie.content,
                               output=output,
                               n=n,
                               i=i)
    if polecenie.status_code == 200 and polecenie.url.count("png") == 1 and kod_powiatu == 1465:
        save_data.zapis_danych(polecenie_zawartosc=polecenie.content,
                               output=output,
                               n=n,
                               i=i)
    elif polecenie.url.count("png") > 0:
        pass
    else:
        print(f"Failed to fetch image. Status code: {polecenie.status_code}")

    return przekierowanie