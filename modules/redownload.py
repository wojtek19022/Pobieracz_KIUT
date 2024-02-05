import webbrowser
from time import sleep

from .move_cursor import move_cursor_on_screen


def download_again(county_code, output, value, name):
    if county_code == 1465:
        print("Pobieranie: ", name, value.strip())
        webbrowser.open(url=value.split(" ")[1].strip())
    else:
        print("Pobieranie: ", name, value.strip().replace("png", "tiff"))
        webbrowser.open(url=value.split(" ")[1].strip().replace("png", "tiff"))
    # Na przyszłość: [i for i in range(5)][0]
    sleep(3)
    move_cursor_on_screen(
        county_code=county_code, output=output, value=value.split(' ')[0], name=name
    )
    sleep(1)
