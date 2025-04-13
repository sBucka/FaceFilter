import cv2 
from math import floor
import enum

# load the required trained XML classifiers
# https://github.com/Itseez/opencv/blob/master/
# data/haarcascades/haarcascade_frontalface_default.xml
# Trained XML classifiers describes some features of some
# object we want to detect a cascade function is trained
# from a lot of positive(faces) and negative(non-faces)
# images.
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

# https://github.com/Itseez/opencv/blob/master
# /data/haarcascades/haarcascade_righteye_2splits.xml
# Trained XML file for detecting righteye_2splits
# And for left eye the same but with lefteye_2splits

right_eye_cascade = cv2.CascadeClassifier('haarcascade_righteye_2splits.xml')

left_eye_cascade = cv2.CascadeClassifier('haarcascade_lefteye_2splits.xml')


# capture frames from a camera
cap = cv2.VideoCapture(0)

colors = {
    "blue": (255, 0, 0),
    "green": (0, 255, 0),
    "red": (0, 0, 255),
    "yellow": (0, 255, 255),
    "cyan": (255, 255, 0),
    "magenta": (255, 0, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0)
}
color = 0

class Filter(enum.Enum):
    OUTLINES = 1
    NOSE = 2
    CUSTOM_EYES = 3
    PUPILS = 4

active_filters = {
    Filter.OUTLINES: True,
    Filter.NOSE: False,
    Filter.CUSTOM_EYES: False,
    Filter.PUPILS: False,
}

# Define a dictionary to hold the color index for each filter.
color_indices = {
    Filter.PUPILS: 0,
    Filter.CUSTOM_EYES: 0,
    Filter.NOSE: 0,
}

def cycle_color(filter_type: Filter):
    global color_indices
    total_colors = len(colors)
    
    # If the filter is not active, activate it and initialize the index.
    if not active_filters[filter_type]:
        toggle_filter(filter_type)
        color_indices[filter_type] = 0
        return

    # Cycle the color index modulo the total number of colors.
    color_indices[filter_type] = (color_indices[filter_type] + 1) % total_colors

    # If the cycle comes back to 0, deactivate the filter.
    if color_indices[filter_type] == 0:
        toggle_filter(filter_type)
        

def toggle_filter(filter_type: Filter):
    active_filters[filter_type] = not active_filters[filter_type]
    





# loop runs if capturing has been initialized.
while 1: 
    current_color = list(colors.values())[color]
    next_color = list(colors.values())[(color + 1) % len(colors)]
    current_color_pupils = list(colors.values())[color_indices[Filter.PUPILS]]
    current_color_custom_eyes = list(colors.values())[color_indices[Filter.CUSTOM_EYES]]
    current_color_nose = list(colors.values())[color_indices[Filter.NOSE]]
 
    # reads frames from a camera
    ret, img = cap.read() 
    
    # convert to gray scale of each frames
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    cv2.putText(img, "Press esc to exit", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, current_color, 1)
    
    cv2.putText(img, "Press space to change outline", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.4, current_color, 1)
    cv2.putText(img, "Press 0 to toggle outlines", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.4, current_color, 1)
    cv2.putText(img, "Press 1 to cycle nose color", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.4, current_color, 1)
    cv2.putText(img, "Press 2 to cycle eyes color", (10, 120), cv2.FONT_HERSHEY_SIMPLEX, 0.4, current_color, 1)
    cv2.putText(img, "Press 3 to cycle pupils color", (10, 140), cv2.FONT_HERSHEY_SIMPLEX, 0.4, current_color, 1)
    
    # Detects faces of different sizes in the input image
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x,y,w,h) in faces:
        # To draw a rectangle in a face 
        if active_filters[Filter.OUTLINES]:
            cv2.putText(img, "Face", (x, y-10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, current_color, 2)
            cv2.rectangle(img,(x,y),(x+w,y+h),current_color,2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]

        right_eye = right_eye_cascade.detectMultiScale(roi_gray)
        left_eye = left_eye_cascade.detectMultiScale(roi_gray)
        
        eyes = zip(right_eye, left_eye)
        
        for (rex,rey,rew,reh), (lex,ley,lew,leh) in eyes:
            lenght_between_eyes = lex - rex
            
            
            if active_filters[Filter.OUTLINES]:
                cv2.putText(roi_color, "Right", (rex, rey-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, next_color, 1)
                cv2.putText(roi_color, "Left", (lex, ley-10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, next_color, 1)
                cv2.rectangle(roi_color,(rex,rey),(rex+rew,rey+reh),next_color,2)
                cv2.rectangle(roi_color,(lex,ley),(lex+lew,ley+leh),next_color,2)
            
                #cv2.putText(img, "Distance between eyes: " + str(lenght_between_eyes), (x, y-30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, current_color, 1)
            
            if active_filters[Filter.CUSTOM_EYES]:
                cv2.circle(roi_color, (rex + rew//2, rey + reh//2), rew//2, current_color_custom_eyes, 2)
                cv2.circle(roi_color, (lex + lew//2, ley + leh//2), lew//2, current_color_custom_eyes, 2)
                
            if lenght_between_eyes > 30 and active_filters[Filter.NOSE]:
                cv2.circle(roi_color, (floor((rex + lex + lew) / 2), floor((rey + ley + leh) / 2)+40), floor((rey + ley + leh) / 6), current_color_nose, -1)
            
            if active_filters[Filter.PUPILS]:
                cv2.circle(roi_color, (rex + rew//2, rey + reh//2), rew//8, current_color_pupils, -1)
                cv2.circle(roi_color, (lex + lew//2, ley + leh//2), lew//8, current_color_pupils, -1)
                
                
                
            

    # Display an image in a window
    cv2.imshow('img',img)

    # Wait for Esc key to stop
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
    if k == 32: 
        color = (color + 1) % len(colors)
    if k == 48:
        toggle_filter(Filter.OUTLINES)
    if k == 49:
        cycle_color(Filter.NOSE)
    if k == 50:
        cycle_color(Filter.CUSTOM_EYES)
    if k == 51:
        cycle_color(Filter.PUPILS)


# Close the window
cap.release()

# De-allocate any associated memory usage
cv2.destroyAllWindows() 