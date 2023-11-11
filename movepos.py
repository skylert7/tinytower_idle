import cv2
import pyautogui
import numpy as np
from PIL import Image
import time
from AppKit import NSScreen
import pygetwindow as gw
import subprocess
from subprocess import Popen, PIPE
from datetime import datetime
import logging

# Create a logger
logger = logging.getLogger('my_logger')

# Set the logging level (you can change this to suit your needs)
logger.setLevel(logging.INFO)

# Create a file handler to log to a file
file_handler = logging.FileHandler('my_log_file.log')

# Create a console handler to log to the console
console_handler = logging.StreamHandler()

# Define the log format
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


def get_screenshot():
    global GAME_REGION
    # logger.info(f'Started at {pyautogui.position()}')
    # Capture a screenshot
    GAME_REGION_MACOS = [i * 2 for i in GAME_REGION]  # * 2 because of macos
    logger.info(f'Taking screenshot for region {GAME_REGION_MACOS}')
    screenshot = pyautogui.screenshot(region=GAME_REGION_MACOS)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    # logger.info(f'Screenshot size: {screenshot.shape}')

    # # Display the result
    # cv2.imshow('Screenshot Result', screenshot)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite('screnshot_vanilla.jpg', screenshot)

    return screenshot


def get_window_coord(windowname):
    # Replace 'Window Name' with the name of the window you want to find
    window_name = windowname

    # AppleScript to get the window coordinates
    applescript = f"""
    tell application "System Events"
        tell process "{window_name}"
            tell UI element 1 of window 1
                set p to position
                set s to size
            end tell
        end tell
    end tell
    
    set xCoordinate to (item 1 of p) + (item 1 of s) / 2
    set yCoordinate to (item 2 of p) + (item 2 of s) / 2
    return {{p, s}}
    """

    p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    stdout, stderr = p.communicate(applescript)
    result = stdout.replace(',', '')

    # Split the result into start pos and size
    start_lc, size_lc = (result.split()[0], result.split()[1]), (result.split()[2], result.split()[3])
    start_lc_int = [eval(i) for i in start_lc]
    size_lc_int = [eval(i) for i in size_lc]

    # logger.info the coordinates
    logger.info(f"Start: {start_lc_int}, Size: {size_lc_int}")
    return start_lc_int, size_lc_int


def focus_window(windowname):
    # Replace 'Window Name' with the actual title of the window you want to focus on
    window_name = windowname

    # AppleScript to focus on a window by name
    applescript = f"""
    tell application "System Events"
        set frontApp to name of first application process whose frontmost is true
        if frontApp is not "{window_name}" then
            tell application "{window_name}" to activate
        end if
    end tell
    """

    # Run the AppleScript
    subprocess.call(["osascript", "-e", applescript])


windowName = 'Tiny Tower'

focus_window(windowName)
start, size = get_window_coord(windowName)

GAME_REGION = (start[0], start[1], size[0], size[1])  # * 2 because of macos
logger.info(f'GAME_REGION: {GAME_REGION}')

logger.info(f'Move to {start}')
pyautogui.moveTo(start)

newpos = (start[0] + (size[0] // 2), start[1] + 20)
logger.info(f'Move to {newpos}')
pyautogui.moveTo(newpos)
