import cv2 as cv
import numpy as np
import pyautogui

#! This function will read the latest captured frame and return how many red hearts are on the screen in float form
def getRedHearts(window_region,debug=False) -> float:
    # Load images
    screenshot = pyautogui.screenshot(region=window_region)
    screenshot.save("img/Capture/Thing.png")
    
    haystack_img = cv.imread("img/Capture/Thing.png", cv.IMREAD_UNCHANGED)
    full_heart_img = cv.imread("img/Hearts/redheart.png", cv.IMREAD_UNCHANGED)
    half_heart_img = cv.imread("img/Hearts/halfredheart.png", cv.IMREAD_UNCHANGED)

    # Convert images to BGR to remove any alpha channels
    haystack_BGR = cv.cvtColor(haystack_img, cv.COLOR_BGRA2BGR)
    full_heart_BGR = cv.cvtColor(full_heart_img, cv.COLOR_BGRA2BGR)
    half_heart_BGR = cv.cvtColor(half_heart_img, cv.COLOR_BGRA2BGR)
    cv.imwrite("img/DEBUG/DEBUGHAYSTACK.png",haystack_BGR)
    cv.imwrite("img/DEBUG/DEBUGFULLRED.png",full_heart_BGR)
    cv.imwrite("img/DEBUG/DEBUGHALFRED.png",half_heart_BGR)
    
    # Perform template matching for full heart
    threshold = 0.9
    res_full = cv.matchTemplate(haystack_BGR, full_heart_BGR, cv.TM_CCOEFF_NORMED)
    loc_full = np.where(res_full >= threshold)

    # Perform template matching for half heart
    res_half = cv.matchTemplate(haystack_BGR, half_heart_BGR, cv.TM_CCOEFF_NORMED)
    loc_half = np.where(res_half >= threshold)

    # Count the number of matches that passes threshold
    count_full = len(list(zip(*loc_full[::-1])))
    count_half = len(list(zip(*loc_half[::-1]))) 
    
    # Drawing bounding boxes on the haystack image to visualize what the computer sees
    # TODO: Maybe add confidence values too to have a better sense
    if debug == False:
        pass
    else:
        #DEBUG - Showing boundingbox of detected image
        if loc_full:
            for pt in zip(*loc_full[::-1]):
                cv.rectangle(haystack_img, pt, (pt[0] + full_heart_BGR.shape[1], pt[1] + full_heart_BGR.shape[0]), (0, 255, 0), 2)

        if loc_half:
        # Draw bounding boxes for half hearts
            for pt in zip(*loc_half[::-1]):
                cv.rectangle(haystack_img, pt, (pt[0] + half_heart_BGR.shape[1], pt[1] + half_heart_BGR.shape[0]), (255, 0, 0), 2)
        
        cv.imwrite('img/DEBUG/DEBUGHAYSTACKWITHBOX.jpg', haystack_img)
    
    #Returns the amount of red health we have
    return (float(count_full)) + float(count_half/2)

