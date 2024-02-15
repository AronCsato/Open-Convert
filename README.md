# Open-Convert

## This program open files from a specific folder and open it one by one, then saves the the flat pattern in .3dxf
### How its works:
* First step it finds all the ```--type``` files in the specified folder path with argument ```--path```
* Opens all the files from the folder with the specified program, deined by the ```--program``` argument (full path of the program .exe file)
* Took a screenshot from the screen
> **NOTE:** If multiple monitors are conected its works only when Inventor is opened on the 1 monitor
* Get all the text from the screenshot and finds ```Pattern``` to identify where is Flat Pattern on the screen
* Clicks on with right mouse button
* Takes another screenshot and finds ```As...``` in the texts from the screenshot and click on with the mouse
* After the Save As windows appears it navigates throught to save in .3dx format with keyboard commands
* At each step closes the Inventor enad reopens it
> **NOTE:** There are delays introduced in the program in form os sleep times, this time intervals can be tuned by ```tx``` arguments
### The program can be run from cmd with ```convert23dx.exe```
* The command to run it:`start convert23dx.exe`
### For run the program you need to install tesseract on your local pc, you will find the neccesarry info:
`https://github.com/UB-Mannheim/tesseract/wiki`

### Arguments to run the program
#### Necesarry arguments:
* -p or --path: path to the folder where the files are
* -t or --type: file type to look for in the folder
* -pr or --program: program .exe path
#### Aditional arguments:
* --tesseract_path: by default is C:\\Program Files\\Tesseract-OCR\\tesseract.exe, path where tesseract is installed
* --print_scrsht_text: print all the text from screenshot for debug
* -t1: by default is 15s set the time sleep for openeing the Inventor
* -t2: by default is 5s set the time sleep befor taking the screenshots
* -t3: by default is 1s set the time between pressing the buttons from keyboard
* -t4: by default is 10s set the time between open another file in inventor
### Example how to use:
`python3 .\convert23dx.py -p F:\Bedo_program\test_folder -t ipt -pr "C:\\Program Files\\Autodesk\\Inventor 2019\\Bin\\Inventor.exe" `