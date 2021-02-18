import base64
import json
import os
import pyautogui as pyautogui
import requests
from pyclick import HumanClicker

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
API_URL = 'http://localhost:8080'
id_device = 1


def uploadImage(path, id_device):
    image_file = path

    with open(image_file, "rb") as f:
        im_bytes = f.read()
    im_b64 = base64.b64encode(im_bytes).decode("utf8")

    payload = json.dumps({"image": im_b64, "id_device": id_device})
    response = requests.post('{api}/upload'.format(api=API_URL), data=payload, headers=headers)


def getCommand(id_device):
    response = requests.get('{api}/commands/{id_device}'.format(api=API_URL, id_device=id_device),
                            headers=headers)
    return response.json()


def open_browser(url):
    os.system("firefox --url" + url)
    pass


def take_screenshot(id_device):
    path = str(id_device) + "/browser.png"
    pyautogui.press('tab')
    pyautogui.sleep(0.5)
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(path)
    return path


def moveClick(width, height):
    hc = HumanClicker()
    # move the mouse to position (100,100) on the screen in approximately 2 seconds
    hc.move((int(width), int(height)), 1)
    # mouse click(left button)
    hc.click()
    pass


def typeMSG(msg):
    pyautogui.typewrite(msg)


if __name__ == '__main__':
    while True:
        pyautogui.sleep(3)
        response = getCommand(id_device)
        command = response['command']
        if command == 'OPEN_BROWSER':
            open_browser(response['params'])
        elif command == "TAKE_SCREEN_SHOT":
            path = take_screenshot(id_device)
            uploadImage(path, id_device)
        elif command == "MV_CLICK":
            width = command['parametrs']['width']
            height = command['parametrs']['height']
            moveClick(width, height)
        elif command == "TYPE_MSG":
            typeMSG(command['params'])