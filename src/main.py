import pyautogui
import pyscreeze
import pygetwindow as gw
import time
import os
from helper import *
try: 
    #? This focuses on the isaac window then gets a screenshot of it
    window = gw.getWindowsWithTitle("Binding of Isaac: Repentance")[0]
    window.activate()
    window.resizeTo(1280, 720)
    time.sleep(2)
    PreStartHP = 0.0 # Starting health to let program know when we actually started
    pastHP = 0.0
    hitstaken = 0
    gameStarted = False
    while True:
        try:
            window_region = (window.left+125, window.top+50, 300, 100)
            screenshot = pyautogui.screenshot(region=window_region)
            screenshot.save("img/Thing.png")
        
            #Inputting to terminal
            os.system('cls' if os.name == 'nt' else 'clear')
            CurrentHP = getRedHearts(debug=False)
            print(f"Total hearts found: {CurrentHP}")
            
            # To not set false game start flags
            if CurrentHP > PreStartHP:
                gameStarted = True
                
            if hitstaken > 0:
                print(f"Hits Taken: {hitstaken}")
                
            if gameStarted == True:
                if pastHP > CurrentHP:
                    print("Lost HP") 
                    #! INSERT PUNISHMENT CODE HERE
                    
                    hitstaken += 1
                    
                elif pastHP == CurrentHP:
                    print("no change")
                else:
                    print("Gained HP, no change")
                    


            pastHP = CurrentHP
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
    