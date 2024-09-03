import pyautogui
import pyscreeze
import pygetwindow as gw
import time
import os
from helper import *


#TODO: ADD BLACK HEART, SOUL HEART TRACKING
try: 
    #? This focuses on the isaac window and sets it to 1280 x 720
    window = gw.getWindowsWithTitle("Binding of Isaac: Repentance")[0]
    window.activate()
    window.resizeTo(1280, 720)
    time.sleep(2)
    
    #* Init values and flag
    PreStartHP = 0.0
    pastHP = 0.0
    hitstaken = 0
    gameStarted = False
    while True:
        try:
            window_region = (window.left+125, window.top+50, 300, 100)
        
            os.system('cls' if os.name == 'nt' else 'clear') # Clearing Terminal
            CurrentHP = getRedHearts(window_region,debug=False)
        
            # Initial Flag to check if we have started a game or not 
            if CurrentHP > PreStartHP:
                gameStarted = True
            
            # If game has started
            if gameStarted == True:
                
                # Check for sudden disappearance of health(I.E changing levels, using teleports,etc...)
                # Resumes the program if the pastHP is equal to the newest detected HP value
                while CurrentHP == 0.0 and pastHP > 0.5:
                    time.sleep(1)
                    os.system('cls' if os.name == 'nt' else 'clear')
                    print("Game Transitioning/Paused")
                    CurrentHP = getRedHearts(window_region,debug=False)
                    print(f"CurrentHP: {CurrentHP}")
                    print(f"PastHP: {pastHP}")
                    if CurrentHP == pastHP: # Game resume
                        break
                else:
                    
                    #Checking for health interaction
                    print(f"Total hearts found: {CurrentHP}")
                    if pastHP > CurrentHP:
                        print("Lost HP") 
                        #! INSERT PUNISHMENT CODE HERE
                        hitstaken += 1
                    elif pastHP == CurrentHP:
                        print("no change")
                    else:
                        print("Gained HP, no change")

                    print(f"Hits Taken: {hitstaken}")

            # Update values
            pastHP = CurrentHP
            time.sleep(0.5)

        
        except pyscreeze.ImageNotFoundException:
            print("Nothing Found or Confidence too low")
            time.sleep(0.5)
            continue
        
        except KeyboardInterrupt:
            break
        
except IndexError:
    print("Isaac is not opened")
except RuntimeError:
    print("sumting wrong :D")
    