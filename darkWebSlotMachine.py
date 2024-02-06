import pyautogui
from pynput.keyboard import Key, Listener, Controller
import time
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

def on_press(key):
    global currentString
    if hasattr(key, 'char'):
        if key.char == 'd': 
            currentString = generate_next_string(currentString, 10)
        if key.char == 'c': 
            currentString = generate_next_string(currentString, 100)
        if key.char == 'm': 
            currentString = generate_next_string(currentString, 1000)
        # For regular alphanumeric keys
        #print("Key pressed:", key.char)
    elif hasattr(key, 'name') and key.name == 'space':
        currentString = generate_next_string(currentString, 1)
        close_tab()
        url = "https://prnt.sc/" + currentString
        open_webpage(url)
        pyautogui.hotkey('ctrl', 'shift', 'tab')
        print(url)


def on_release(key):
    pass

# Collect events until released


paused = False
open_webpage("https://croissantage.slash-root.fr/")
open_webpage("https://croissantage.slash-root.fr/")
"""
while True:
    if not paused:
        url = "https://prnt.sc/alt035"
        open_webpage(url)
        print(url)
    time.sleep(3)
    if not paused :
        close_tab()
"""

with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
