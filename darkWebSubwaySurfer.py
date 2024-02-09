import subprocess
import requests
import re

imageList = []

def showImage(save_path):
    subprocess.run(str("mv " + save_path + " " + "./loadedImage"), shell=True, capture_output=True, text=True)

def saveImage(url, save_path):
    response = requests.get(url)
    if response.status_code == 200:
        with open(save_path, 'wb') as f:
            f.write(response.content)
        print("Image downloaded successfully")
        return(True)
    else:
        print("Failed to download image")
        return(False)


def find_expression(filename):
    with open(filename, 'r') as file:
        content = file.read()

    # Regular expression pattern
    pattern = r'content="https://[^"]+\.(png|jpg)"'
    pattern = pattern[9:-1]
    # Search for the pattern
    match = re.search(pattern, content)

    if match:
        return match.group()
    else:
        return None


def downloadImage(url, name):
    global imageList
    subprocess.run(str("wget -p --convert-links " + url), shell=True, capture_output=True, text=True)
    filename = str("prnt.sc/" + name)
    print(filename)
    expression = find_expression(filename)
    if expression == None:
        return(None)
    print(expression)
    subprocess.run(str("rm -r prnt.sc"), shell=True, capture_output=True, text=True)
    if (saveImage(expression, str("images/" + name))):
        imageList.append(str("images/" + name))



import pyautogui
from pynput.keyboard import Key, Listener, Controller
import time
import threading
import webbrowser


def generate_next_string(current_string, steps=1):
    # Convert the string to a base 36 integer
    current_number = int(current_string, 36)
    
    # Increment the number by the specified number of steps
    next_number = current_number + steps
    
    # Convert the incremented number back to base 36 string
    next_string = base36encode(next_number)
    
    # If the length of the generated string is less than 6, prepend zeros
    next_string = next_string.zfill(6)
    
    return next_string

def base36encode(number):
    if not isinstance(number, int):
        raise TypeError('Number must be an integer')

    if number < 0:
        raise ValueError('Number must be positive')

    alphabet = '0123456789abcdefghijklmnopqrstuvwxyz'
    base36 = ''

    while number:
        number, i = divmod(number, 36)
        base36 = alphabet[i] + base36

    return base36 or '0'

def open_webpage(url):
    try:
        webbrowser.open(url)
    except Exception as e:
        pass

def close_tab():
    try:
        # Simulate pressing Ctrl + W
        pyautogui.hotkey('ctrl', 'w')
    except Exception as e:
        pass

currentString = input("3 lowercase letters followed by 3 numbers :     ")
import webbrowser
webbrowser.open_new_tab("darkWebPage.html")


paused = False
nextFlip = time.time()
def generateLoop():
    global paused, nextFlip, imageList, currentString
    while True:
        print(imageList)
        if not paused:
            if (time.time() > nextFlip) and len(imageList) != 0:
                showImage(imageList.pop(0))
                nextFlip = time.time() + 3
        time.sleep(0.1)
        if len(imageList) < 10:
            currentString = generate_next_string(currentString, 1)
            url = "https://prnt.sc/" + currentString
            downloadImage(url, currentString)
            print(url)

mainLoop = threading.Thread(target=generateLoop)
mainLoop.daemon = True  # Set the thread as daemon so it stops when the main program stops
mainLoop.start()


def on_press(key):
    global currentString, paused
    if hasattr(key, 'char'):
        if key.char == 'p': 
            paused = not paused
        #print("Key pressed:", key.char)
    

def on_release(key):
    pass

# Collect events until released




with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()


