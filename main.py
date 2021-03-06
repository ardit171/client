import argparse
import base64
import json
import os
import pyautogui as pyautogui
import requests
from pyclick import HumanClicker

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
API_URL = ''
id_device = ''


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
    command = 'firefox {url} &'.format(url=url)
    os.system(command)
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
    hc.move((int(width), int(height)), 1)
    hc.click()
    pass


def typeMSG(msg):
    pyautogui.typewrite(msg)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Client Automation Script.')
    parser.add_argument('-d', dest='id_device',required=True, help='Id of the Device')
    parser.add_argument('-s', dest='api',required=True, help='Server Ip')
    args = parser.parse_args()
    API_URL = args.api
    id_device = args.id_device
    if not os.path.exists(str(id_device)):
        os.makedirs(str(id_device))
    while True:
        pyautogui.sleep(3)
        response = getCommand(id_device)
        command = response['command']
        print(command)
        if command == 'OPEN_BROWSER':
            open_browser(response['params'])
        elif command == "TAKE_SCREEN_SHOT":
            path = take_screenshot(id_device)
            uploadImage(path, id_device)
        elif command == "MV_CLICK":
            width = response['params']['width']
            height = response['params']['height']
            moveClick(float(width), float(height))
        elif command == "TYPE_MSG":
            typeMSG(response['params'])
        elif command == "SLEEP":
            pyautogui.sleep(int(response['params']))
        elif command == "PRESS_KEY":
            pyautogui.press(response['params'])