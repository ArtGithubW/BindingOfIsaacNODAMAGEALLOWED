import pyautogui
import pyscreeze
import pygetwindow as gw
import time
import cv2 as cv
import numpy as np
try: 
    #? This focuses on the isaac window then gets a screenshot of it
    window = gw.getWindowsWithTitle("Binding of Isaac: Repentance")[0]
    window.activate()
    window.resizeTo(1280, 960)
    time.sleep(1)

    
    while True:
        try:
            window_region = (window.left+180, window.top+50, 350, 100)
            screenshot = pyautogui.screenshot(region=window_region)
            screenshot.save("Thing.png")
            # fullredheart = list(pyautogui.locateAllOnScreen("redheart.png", region=window_region, confidence=0.7))
            # halfredheart = list(pyautogui.locateAllOnScreen("img/halfredheart.png", region=window_region, confidence=0.7))
            # count = len(fullredheart) #+ len(halfredheart)

            # print(f"Number of redheart.png instances found: {count}")
            # screenshot = pyautogui.screenshot(region=(int(boxlocation.left)+100, int(boxlocation.top)+100, boxlocation.width+100, boxlocation.height+100))
            time.sleep(0.5)

        except pyautogui.ImageNotFoundException:
            print("Nothing Found")
            time.sleep(0.5)
            continue
        
        except pyscreeze.ImageNotFoundException:
            print("Nothing Found or Confidence too low")
            time.sleep(0.5)
            continue
        
        except KeyboardInterrupt:
            break
except RuntimeError:
    print("sumting wrong :D")
    