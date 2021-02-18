import pyautogui

path = str(1) + "/browser.png"
pyautogui.press('tab')
pyautogui.sleep(0.5)
myScreenshot = pyautogui.screenshot()
myScreenshot.save(path)