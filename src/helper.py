import cv2 as cv
import numpy as np


#This function will read the latest captured frame and return how many red hearts are on the screen in float form
def getRedHearts(debug=False) -> float:
    haystack_img = cv.imread("img/Thing.png", cv.IMREAD_ANYCOLOR)
    full_heart_img = cv.imread("img/redheart.png", cv.IMREAD_ANYCOLOR)
    half_heart_img = cv.imread("img/halfredheart.png", cv.IMREAD_ANYCOLOR)
    HalfHeartRes = cv.matchTemplate(haystack_img, half_heart_img, cv.TM_SQDIFF_NORMED)
    FullHeartRes = cv.matchTemplate(haystack_img, full_heart_img, cv.TM_SQDIFF_NORMED)
    threshold = 0.08 #This threshold works best for now
    
    # Find locations of hearts
    fullHeartLocation = np.where(FullHeartRes <= threshold)
    fullHeartLocation = list(zip(*fullHeartLocation[::-1]))
    HalfHeartLocation = np.where(HalfHeartRes <= threshold)
    HalfHeartLocation = list(zip(*HalfHeartLocation[::-1]))
    
    if debug == False:
        pass
    else:
        #DEBUG - Showing boundingbox of detected image
        if fullHeartLocation:
            needle_w = full_heart_img.shape[1]
            needle_h = full_heart_img.shape[0]
            line_color = (0, 255, 0)
            line_type = cv.LINE_4
            # Loop over all the fullHeartLocation and draw their rectangle
            for loc in fullHeartLocation:
                # Determine the box positions
                top_left = loc
                bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
                # Draw the box
                cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
        
        if HalfHeartLocation:
            needle_w = half_heart_img.shape[1]
            needle_h = half_heart_img.shape[0]
            line_color = (255, 0, 0)
            line_type = cv.LINE_4
            # Loop over all the fullHeartLocation and draw their rectangle
            for loc in HalfHeartLocation:
                # Determine the box positions
                top_left = loc
                bottom_right = (top_left[0] + needle_w, top_left[1] + needle_h)
                # Draw the box
                cv.rectangle(haystack_img, top_left, bottom_right, line_color, line_type)
        cv.imwrite('img/ThingWithBox.jpg', haystack_img)
        
    return (float(len(fullHeartLocation))) + float(len(HalfHeartLocation)/2)