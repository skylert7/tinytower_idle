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


# MacOS dimesion
# center_x = NSScreen.mainScreen().frame().size.width // 2
# center_y = NSScreen.mainScreen().frame().size.height // 2
def get_screenshot():
    global GAME_REGION
    # print(f'Started at {pyautogui.position()}')
    # Capture a screenshot
    screenshot = pyautogui.screenshot(region=GAME_REGION)
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_BGR2GRAY)
    # print(f'Screenshot size: {screenshot.shape}')

    # # Display the result
    # cv2.imshow('Screenshot Result', screenshot)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite('screnshot_vanilla.jpg', screenshot)

    return screenshot


def parachuteClick():
    focus_window('Tiny Tower')

    screenshot = get_screenshot()
    # Load the template image
    template = cv2.imread("parachute.png")
    template = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)

    # # Display the result
    # cv2.imshow('parachute', template)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Draw a rectangle around the match
    h, w = template.shape
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    cv2.rectangle(screenshot, top_left, bottom_right, (0, 255, 0), 2)

    # Display the result
    # cv2.imshow('Template Matching Result', screenshot)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    cv2.imwrite('result.jpg', screenshot)

    # Calculate the center of the matched rectangle
    center_x = (top_left[0] + w // 2) // 2  # // 4 because of Macos
    center_y = (top_left[1] + h // 2) // 2  # // 4 because of Macos

    print(center_x, center_y)

    # Click on the center of the matched rectangle
    # pyautogui.moveTo(center_x, center_y + 100)
    pyautogui.click(center_x, center_y + 50)
    time.sleep(0.5)

    parachute_continue_no_ads = (1117, 573)
    pyautogui.click(parachute_continue_no_ads)
    time.sleep(0.5)


def viewimage():
    # Load the template image
    template = cv2.imread("parachute.png")
    # template = np.array(template)
    print(template)

    # Display the result
    cv2.imshow('Template Matching Result', template)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    time.sleep(0.5)


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

    # Print the coordinates
    print(f"Start: {start_lc_int}, Size: {size_lc_int}")
    return start_lc_int, size_lc_int


windowName = 'Tiny Tower'
start, size = get_window_coord(windowName)

GAME_REGION = (start[0] * 2, start[1] * 2, size[0] * 2, size[1] * 2) # * 2 because of macos
print(GAME_REGION)
parachuteClick()
