import argparse
import base64
import json
import os
import pyautogui as pyautogui
import requests
from pyclick import HumanClicker
import threading
import api

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
API_URL = ''
id_device = ''


def uploadImage(path, id_device, cron):
    image_file = path

    with open(image_file, "rb") as f:
        im_bytes = f.read()
    im_b64 = base64.b64encode(im_bytes).decode("utf8")
    if cron:
        payload = json.dumps({"image": im_b64, "id_device": id_device, "cron": True})
    else:
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
    myScreenshot = pyautogui.screenshot()
    myScreenshot.save(path)
    return path


def moveClick(width, height):
    hc = HumanClicker()
    hc.move((int(width), int(height)), 1)
    hc.click()


def moveMove(width, height):
    hc = HumanClicker()
    hc.move((int(width), int(height)), 1)
    pass

def typeMSG(msg):
    pyautogui.typewrite(msg)

def scroll(ticks):
    pyautogui.scroll(ticks)

def close_browser():
    command = 'pkill firefox'
    os.system(command)
    pass
def verifyJob(id_device):
    requests.get('{api}/jobVerify/{id_device}'.format(api=API_URL, id_device=id_device),
                 headers=headers)



if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Client Automation Script.')
    parser.add_argument('-d', dest='id_device',required=True, help='Id of the Device')
    parser.add_argument('-s', dest='api',required=True, help='Server Ip')
    args = parser.parse_args()
    API_URL = args.api
    # API_URL = "http://127.0.0.1:8080"
    id_device = args.id_device
    # id_device = "1"
    t1 = threading.Thread(target=api.run_server_api)
    t1.setDaemon(True)
    t1.start()
    if not os.path.exists(str(id_device)):
        os.makedirs(str(id_device))
    while True:
        pyautogui.sleep(1)
        path = take_screenshot(id_device)
        uploadImage(path,id_device, True)
        response = getCommand(id_device)
        command = response['command']
        print(command)
        if command == 'OPEN_BROWSER':
            open_browser(response['params'])
            verifyJob(id_device)
        elif command == "TAKE_SCREEN_SHOT":
            path = take_screenshot(id_device)
            uploadImage(path, id_device, False)
            verifyJob(id_device)
        elif command == "MV_CLICK":
            width = response['params']['width']
            height = response['params']['height']
            moveClick(float(width), float(height))
            verifyJob(id_device)
        elif command == "TYPE_MSG":
            typeMSG(response['params'])
            verifyJob(id_device)
        elif command == "SLEEP":
            pyautogui.sleep(int(response['params']))
        elif command == "PRESS_KEY":
            pyautogui.press(response['params'])
            verifyJob(id_device)
        elif command == "CLOSE_BROWSER":
            close_browser()
            verifyJob(id_device)
        elif command == "MV_MV":
            width = response['params']['width']
            height = response['params']['height']
            moveMove(float(width), float(height))
            if not 'interact' in response['params']:
                verifyJob(id_device)