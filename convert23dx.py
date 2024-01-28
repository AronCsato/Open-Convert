import sys
import os
import argparse
import subprocess
import time
from pynput.keyboard import Key, Controller
import pygetwindow as gw
import pyautogui
import pytesseract
import mss
import cv2
import numpy as np
import wmi

def find_files(folder_path:str,file_type:str)->list:
    """
    Find specified file types in a folder and return the files full path in a list
    :folder_path: where to look for file full path
    :file_type: the file extension
    :return: list of founded files full path
    """
    file_paths = []
    for file in os.listdir(folder_path):
        if file.endswith(file_type):
            print(os.path.join(folder_path,file))
            file_paths.append(os.path.join(folder_path,file))
    if file_paths:
        return file_paths
    else:
        print("There are no files in {} with {} extension".format(folder_path,file_type))
        sys.exit()


def open_file(file_path:str,program_path:str)->None:
    subprocess.Popen([program_path,file_path])

def wait_until_open(window_name)->None:
    """
    Wait until window_name is appeard in opened windows
    :param window_name: the opened window name
    :return: -
    """
    while True:
        try:
            handle = gw.getWindowsWithTitle(window_name)[0]
            break
        except ValueError:
                time.sleep(10)

    handle.activate()     

def type_in_window(list_of_phrase:list,compound_keys:dict, simple_keys:list)->None:
        """
        Type multiple phareses in window and hit enter after and/or press compund keys and release
        :param list_of_phrase: list type of pharese to type in window and hit enter after each one
        :param compound_keys: press compound keys key-> hold pressed value hit and release
        :return: -
        """
        keyboard = Controller()
        if len(list_of_phrase):
            for list_item in list_of_phrase:
                keyboard.type(list_item)
                keyboard.press(Key.enter)
                keyboard.release(Key.enter)
                time.sleep(10)
        else:
            pass

        if compound_keys:
            for keys,value in compound_keys.items():
                with keyboard.pressed(eval(keys)):
                    keyboard.press(eval(value))
                    keyboard.release(eval(value))
        else:
            pass

        if simple_keys:
            for list_item in simple_keys:
                keyboard.press(list_item)
                keyboard.release(list_item)
                time.sleep(1)

def create_screenshot(monitor_nr:int,word2fnd:str,arg2print:argparse,path_tesseract:str)->None:
    """
    Create screenshot from a specififc monitor and find a word on a screenshot and click on the word
    :monitor_nr: nr of the monitor to take screenshot from
    :word2fnd: find this word
    :arg2print: for debug print all the word find on screenshot
    :path_tesseract: the full path to tesseract
    :return: None
    """
    with mss.mss() as sct:
    
        mon = sct.monitors[monitor_nr]

        monitor = {
            "top": mon["top"],
            "left": mon["left"],
            "width": mon["width"],
            "height": mon["height"],
            "mon": monitor_nr,
        }
        img = np.array(sct.grab(monitor)) # BGR Image
    
    pytesseract.pytesseract.tesseract_cmd = path_tesseract
    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) 
    results = pytesseract.image_to_data(rgb, output_type=pytesseract.Output.DICT)
    if arg2print:
        print(results["text"])

    pos_text = [i for i, x in enumerate((results["text"])) if x == word2fnd]
    if pos_text:
        x = results["left"][pos_text[0]] 
        y = results["top"][pos_text[0]]
        mouse_click(x+2,y-2,'right')
    else:
        print("The word {} is not find in the screenshot. Try run --print_scrsht_text to find your text".format(word2fnd))
        sys.exit()

def mouse_click(x:float,y:float,button:str)->None:
    """
    Click with the mouse
    :x: x postition on the screen of the mouse
    :y: y position on the screen of the mouse
    :button: perform a right or a left click
    :return: None
    """
    if button =='right':
        pyautogui.rightClick(x,y)
    elif button== 'left':
        pyautogui.leftClick(x,y)
    else:
        pass

def close_program(process_name:str)->None:
    """
    Close the program
    :return: -
    """
    os.system("TASKKILL /F /IM {}".format(process_name))

def close_process(process_name:str)->None:
    """
    Check if the process is alive and close else pass
    :return:
    """
    f = wmi.WMI()
    if [True for process in f.Win32_Process() if process.Name == process_name]:
        close_program(process_name)
        time.sleep(1)
    else:
        pass


def main():
    parser = argparse.ArgumentParser(description='This program help Bedo at his daily job')
    parser.add_argument('-p', '--path', help='Path to the folder where the files are')
    parser.add_argument('-t', '--type', help='File type to look for in the folder')
    parser.add_argument('-pr','--program',help='Program .exe path')
    parser.add_argument('--print_scrsht_text',help='print all the text from screenshot')
    parser.add_argument('--tesseract_path',default="C:\\Program Files\\Tesseract-OCR\\tesseract.exe",help='Path where tesseract is installed, by default is "C:\\Program Files\\Tesseract-OCR\\tesseract.exe"')
    args = parser.parse_args()
    print(args)
    file_paths = find_files(args.path,args.type)
    # file_paths = find_files("F:\\Bedo_program\\test_folder",'ipt')
    change_to3dmodel = [Key.alt,'e']
    save_dxf = [Key.tab,Key.down,Key.down,Key.down, Key.enter,Key.tab,Key.tab,Key.tab,Key.enter,Key.enter]

    for file in file_paths:
        open_file(str(file),args.program)
        # open_file(str(file),"C:\Program Files\Autodesk\Inventor 2019\Bin\Inventor.exe")  
        wait_until_open('Autodesk') 
        time.sleep(15)    
        type_in_window([],[],change_to3dmodel)
        time.sleep(5)
        create_screenshot(1,"Pattern",args.print_scrsht_text,args.tesseract_path)
        time.sleep(5)
        create_screenshot(1,"As...",args.print_scrsht_text,args.tesseract_path)
        # type_in_window([],[],save_as)
        type_in_window([],[],save_dxf)
        close_process('Inventor.exe')
        time.sleep(10)   


if __name__=="__main__":
    main()
