import pyautogui
import pytesseract
import mss
import cv2
import numpy as np

# Take a screenshot of the screen
with mss.mss() as sct:
    
    # Get information of monitor 2
    monitor_number = 1
    mon = sct.monitors[monitor_number]

    # The screen part to capture
    monitor = {
        "top": mon["top"],
        "left": mon["left"],
        "width": mon["width"],
        "height": mon["height"],
        "mon": monitor_number,
    }
    output = "sct-mon{mon}_{top}x{left}_{width}x{height}.png".format(**monitor)

    # Grab the data
    sct_img = sct.grab(monitor)
    img = np.array(sct.grab(monitor)) # BGR Image
    
pytesseract.pytesseract.tesseract_cmd = "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
# Perform OCR on the screenshot
rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
results = pytesseract.image_to_data(rgb, output_type=pytesseract.Output.DICT)

# Then loop over each of the individual text 
# localizations 
pos_text = [i for i, x in enumerate((results["text"])) if x == "Fat"]
x = results["left"][pos_text[0]] 
y = results["top"][pos_text[0]]
pyautogui.rightClick(x+2,y-2)


