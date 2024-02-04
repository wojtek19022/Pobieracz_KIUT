import pyautogui

def poruszanie_ekran(kod_powiatu,output,value,name):
    if kod_powiatu == 1465:  # Jeżeli mają być dane pobrane z Warszawy
        pyautogui.moveTo(1581, 676, duration=1)
        pyautogui.rightClick()
        pyautogui.moveTo(1585, 713, duration=1)
        pyautogui.leftClick()

    pyautogui.moveTo(982, 60, duration=1)
    pyautogui.click(982, 60)

    pyautogui.press("enter")
    with pyautogui.hold("ctrl"):
        pyautogui.press("A")

    pyautogui.typewrite(output)
    pyautogui.moveTo(195, 790, duration=1)

    pyautogui.click(195, 790)

    with pyautogui.hold("ctrl"):
        pyautogui.press("A")

    pyautogui.typewrite(f"Obszar_{value}_{name}")
    pyautogui.moveTo(1148, 890, duration=1)
    pyautogui.click(1148, 890)