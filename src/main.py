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
            
            haystack_img = cv.imread("Thing.png", cv.IMREAD_ANYCOLOR)
            needle_img = cv.imread("redheart.png", cv.IMREAD_ANYCOLOR)
            result = cv.matchTemplate(haystack_img, needle_img, cv.TM_SQDIFF_NORMED)
            threshold = 0.08
            # The np.where() return value will look like this:
            # (array([482, 483, 483, 483, 484], dtype=int32), array([514, 513, 514, 515, 514], dtype=int32))
            locations = np.where(result <= threshold)
            # We can zip those up into a list of (x, y) position tuples
            locations = list(zip(*locations[::-1]))
            print(len(locations))
            
            
            if locations:
                print('Found needle.')
                needle_w = needle_img.shape[1]
                needle_h = needle_img.shape[0]
                line_color = (0, 255, 0)
                line_type = cv.LINE_4

                # Loop over all the locations and draw their rectangle
                for loc in locations:
                    # Determine the box positions
                    top_left = loc
                    bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
                    # Draw the box
                    cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
            cv.imwrite('ThingWithBox.jpg', haystack_img)
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
    