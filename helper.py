import cv2
import pyautogui

pyautogui.FAILSAFE = False
import numpy as np
from PIL import Image
import time
import subprocess
from subprocess import Popen, PIPE
from datetime import datetime
import logging
import _thread
from imutils.object_detection import non_max_suppression  # pip install imutils
import schedule
import os

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

start = (0, 0)
size = (0, 0)
GAME_REGION = (0, 0, 0, 0)


def get_screenshot(tinytower_game_screen=True):
    global size, GAME_REGION
    if tinytower_game_screen:
        if size[1] > 900:
            GAME_REGION_MACOS = [i for i in GAME_REGION]
        else:
            GAME_REGION_MACOS = [i * 2 for i in GAME_REGION]  # * 2 because of macos

        # logger.info(f'Started at {pyautogui.position()}')
        # Capture a screenshot
        logger.info(f'Taking screenshot for region {GAME_REGION_MACOS}')
        screenshot = pyautogui.screenshot(region=GAME_REGION_MACOS)
        screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
        # screenshot_monitor = pyautogui.screenshot()
        # screenshot_monitor = cv2.cvtColor(np.array(screenshot_monitor), cv2.COLOR_BGR2GRAY)

        # logger.info(f'Screenshot size: {screenshot.shape}')

        # # Display the result
        # cv2.imshow('Screenshot Result', screenshot)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.imwrite('screnshot_vanilla.jpg', screenshot)
        # cv2.imwrite('screenshot_monitor.jpg', screenshot_monitor)
    else:
        wsop_start = (150, 650)
        wsop_end = (1250, 800)
        region_taken = [wsop_start[0], wsop_start[1], wsop_end[0]-wsop_start[0], wsop_end[1]-wsop_start[1]]
        logger.info(f'Taking screenshot')
        # screenshot_monitor = pyautogui.screenshot(region=region_taken)
        screenshot_monitor = pyautogui.screenshot()
        screenshot_monitor = cv2.cvtColor(np.array(screenshot_monitor), cv2.COLOR_BGR2GRAY)
        cv2.imwrite('screenshot_monitor.jpg', screenshot_monitor)
        screenshot = screenshot_monitor
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


def set_up_for_auto():
    global start, size, GAME_REGION
    windowName = 'Tiny Tower'
    # windowName = 'qemu-system-aarch64'
    focus_window(windowName)
    start, size = get_window_coord(windowName)

    # GAME_REGION = (start[0] * 2, start[1] * 2, size[0] * 2, size[1] * 2)  # * 2 because of macos
    GAME_REGION = (start[0], start[1], size[0], size[1])  # * 2 because of macos
    TOP_LEFT = start

    logger.info(f'GAME_REGION: {GAME_REGION}')
    return start, size, GAME_REGION


def add_suffix_to_filename(filename, suffix='_big'):
    base_name, extension = os.path.splitext(filename)
    return f"{base_name}{suffix}{extension}"


def click_by_image_name(image_name, yes_click=True, yes_move=False, tinytower_gamescreen=True):
    global start, size, GAME_REGION

    # Check game size
    # [663, 950] - big screen
    # [623, 831] - mac screen
    if size[1] > 900:
        image_name = add_suffix_to_filename(image_name, '_big')  # use image with _big

    # Capture a screenshot
    screenshot = get_screenshot(tinytower_gamescreen)

    # # Display the result
    # cv2.imshow('Screenshot Result', screenshot)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # cv2.imwrite('screnshot_vanilla.jpg', screenshot)

    # Load the template image
    template = cv2.imread(image_name)
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # # Display the result
    # cv2.imshow('parachute', template)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    logger.info(f'Max val is: {max_val} matching {image_name}')
    logger.info(f'Min val is: {min_val} matching {image_name}')

    is_matched = False
    threshold = 0.9
    center_x = -1
    center_y = -1
    if 'parachute' in image_name:
        threshold = 0.5
    elif 'liftready' in image_name:
        threshold = 0.8
    elif 'vip' in image_name:
        threshold = 0.92
    elif 'techtree' in image_name:
        threshold = 0.7
    elif 'buildfloor' in image_name:
        threshold = 0.7

    logger.info(f'Threshold is {threshold} for template {image_name}')
    # Find the locations where the result is above the threshold
    locations = np.where(result >= threshold)

    # COULD DO: draw all matches and add their confidence score

    # Count the number of matches
    num_matches = len(locations[0])

    # Print the number of matches
    logger.info(f"Number of matches: {num_matches}")

    # DEBUG - Try
    # (yCoords, xCoords) = np.where(result >= threshold)
    #
    # # Perform non-maximum suppression.
    # template_h, template_w = template.shape[:2]
    # rects = []
    # for (x, y) in zip(xCoords, yCoords):
    #     rects.append((x, y, x + template_w, y + template_h))
    # pick = non_max_suppression(np.array(rects))
    #
    # # Optional: Visualize the results
    # for (startX, startY, endX, endY) in pick:
    #     cv2.rectangle(screenshot, (startX, startY), (endX, endY), (0, 255, 0), 2)
    # cv2.imshow('Results', screenshot)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    # DEBUG - Try

    if max_val >= threshold:
        # Draw a rectangle around the match
        h, w = template.shape
        top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)

        # Display the result
        # cv2.imshow('Template Matching Result', screenshot)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        # cv2.imwrite('result.jpg', screenshot)

        # Calculate the center of the matched rectangle
        if size[1] > 900:
            center_x = GAME_REGION[0] + (top_left[0] + w // 2)
            center_y = GAME_REGION[1] + (top_left[1] + h // 2)
        else:
            center_x = GAME_REGION[0] + (top_left[0] + w // 2) // 2  # // 4 because of MacOS
            center_y = GAME_REGION[1] + (top_left[1] + h // 2) // 2  # // 4 because of MacOS

        # logger.info(center_x, center_y)

        # Click on the center of the matched rectangle
        # pyautogui.moveTo(center_x, center_y + 100)
        if yes_click:
            logger.info(f'Clicking {(center_x, center_y)} when matching {image_name}')
            pyautogui.click(center_x, center_y)
            time.sleep(0.5)
        elif yes_move:
            logger.info(f'Moving to {(center_x, center_y)} when matching {image_name}')
            pyautogui.moveTo(center_x, center_y)
            time.sleep(0.5)
        is_matched = True

    else:
        logger.info(f"Template {image_name} doesn't match well.")
        time.sleep(0.5)

    return is_matched, center_x, center_y, num_matches


'''
NOTES:
adb shell wm size => Physical size: 1080x2220
adb shell getevent -lt /dev/input/event1
adb shell input tap 74 1992 => lift

"So it seems like you need to divide your axis value from evtest by 65535 and multiply it by width or height of device
(in pixels). For example, if you get X=30000, and width of your LCD panel is 1080 pixels, you need to do:

X = round((30000 / 65535) * 1080) = 494 pixels"
adb shell input tap 148 1992 => second from left
adb shell input tap 74 1992 => first from left
adb shell input tap 64 670 => 5minbux
adb shell input tap 256 670 => 5minbux_second
adb shell input tap 708 1356 => 5minbux_collect
adb shell input tap 564 1362 => center (awesome, continue)

result = subprocess.run('adb shell input tap 74 1992', shell=True)
'''
