from requests import request
from .save_data import data_saving

def data_downloading(n, i, extent_total, file_links, redirection, county_code, output):
    parameters = {
        "LAYERS": i,
        "REQUEST": "GetMap",
        "SERVICE": "WMS",
        "FORMAT": "image/tiff",
        "HEIGHT": 2160,
        "VERSION": "1.1.1",
        "SRS": "EPSG:2180",
        "WIDTH": 3840,
        "BBOX": extent_total,
        "TRANSPARENT": "TRUE",
        "EXCEPTIONS": "application/vnd.ogc.se_xml",
    }

    main_link = f"https://integracja01.gugik.gov.pl/cgi-bin/KrajowaIntegracjaUzbrojeniaTerenu/{county_code}"
    response = request(
        "GET", url=main_link, params=parameters, timeout=10, allow_redirects=True
    )

    if response.url.count("png") >= 1:
        redirection = True

        if county_code == 1465:
            url_zapis = str(response.url)
        else:
            url_zapis = str(response.url).replace("png", "tiff")
        file_links.write(str(n) + " " + str(url_zapis) + "\n")
        print("Zapisany link: ", str(n) + " " + url_zapis)
    else:
        redirection = False
        print("Pobrano: ", response.url)

    if response.status_code == 200 and response.url.count("png") == 0:
        data_saving(
            response_content=response.content, output=output, n=n, i=i
        )
    if (
        response.status_code == 200
        and response.url.count("png") == 1
        and county_code == 1465
    ):
        data_saving(
            response_content=response.content, output=output, n=n, i=i
        )
    elif response.url.count("png") > 0:
        pass
    else:
        print(f"Failed to fetch image. Status code: {response.status_code}")

    return redirection,response
