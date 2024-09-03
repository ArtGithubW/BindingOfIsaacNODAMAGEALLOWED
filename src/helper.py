import cv2 as cv
import numpy as np
import pyautogui

#! This function will read the latest captured frame and return how many red hearts are on the screen in float form
def getRednSoulHearts(window_region,debug=False) -> float:
    # Load images
    screenshot = pyautogui.screenshot(region=window_region)
    screenshot.save("img/Capture/Thing.png") #! pyautogui is not immediately readable by opencv, so we save it as a file then read it using opencv
    haystack_img = cv.imread("img/Capture/Thing.png", cv.IMREAD_UNCHANGED)
    full_redheart_img = cv.imread("img/Hearts/redheart.png", cv.IMREAD_UNCHANGED)
    half_redheart_img = cv.imread("img/Hearts/halfredheart.png", cv.IMREAD_UNCHANGED)
    full_soulheart_img = cv.imread("img/Hearts/soulheart.png", cv.IMREAD_UNCHANGED)
    half_soulheart_img = cv.imread("img/Hearts/halfsoulheart.png", cv.IMREAD_UNCHANGED)

    # Converts all images to BGR format to remove ANY alpha channels from PNG's RGBA support
    haystack_BGR = cv.cvtColor(haystack_img, cv.COLOR_BGRA2BGR)
    full_redheart_BGR = cv.cvtColor(full_redheart_img, cv.COLOR_BGRA2BGR)
    half_redheart_BGR = cv.cvtColor(half_redheart_img, cv.COLOR_BGRA2BGR)
    full_soulheart_BGR = cv.cvtColor(full_soulheart_img, cv.COLOR_BGRA2BGR)
    half_soulheart_BGR = cv.cvtColor(half_soulheart_img, cv.COLOR_BGRA2BGR)
    
    # 90% confidence threshold template matching
    threshold = 0.9
    loc_redfull = np.where(cv.matchTemplate(haystack_BGR, full_redheart_BGR, cv.TM_CCOEFF_NORMED) >= threshold)
    loc_redhalf = np.where(cv.matchTemplate(haystack_BGR, half_redheart_BGR, cv.TM_CCOEFF_NORMED) >= threshold)
    loc_soulfull = np.where(cv.matchTemplate(haystack_BGR, full_soulheart_BGR, cv.TM_CCOEFF_NORMED) >= threshold)
    loc_soulhalf = np.where(cv.matchTemplate(haystack_BGR, half_soulheart_BGR, cv.TM_CCOEFF_NORMED) >= threshold)

    # Count the number of matches that passes threshold
    count_full = float(len(list(zip(*loc_redfull[::-1]))) + len(list(zip(*loc_soulfull[::-1]))))
    count_half = (float(len(list(zip(*loc_redhalf[::-1]))) )/2) + (float(len(list(zip(*loc_soulhalf[::-1]))) )/2)
    
    # Drawing bounding boxes on the haystack image to visualize what the computer sees
    # TODO: Maybe add confidence values too to have a better sense
    # TODO: Add debug for soul hearts
    if debug == False:
        pass
    else:
        cv.imwrite("img/DEBUG/DEBUGHAYSTACK.png",haystack_BGR)
        cv.imwrite("img/DEBUG/DEBUGFULLRED.png",full_redheart_BGR)
        cv.imwrite("img/DEBUG/DEBUGHALFRED.png",half_redheart_BGR)
        #DEBUG - Drawing boundingbox of detected image
        if loc_redfull:
            for pt in zip(*loc_redfull[::-1]):
                cv.rectangle(haystack_img, pt, (pt[0] + full_redheart_BGR.shape[1], pt[1] + full_redheart_BGR.shape[0]), (0, 255, 0), 2)
        if loc_redhalf:
            for pt in zip(*loc_redhalf[::-1]):
                cv.rectangle(haystack_img, pt, (pt[0] + half_redheart_BGR.shape[1], pt[1] + half_redheart_BGR.shape[0]), (0, 255, 0), 2)
        
        cv.imwrite('img/DEBUG/DEBUGHAYSTACKWITHBOX.jpg', haystack_img)
    
    #Returns the amount of red health we have
    return (count_full + count_half)

