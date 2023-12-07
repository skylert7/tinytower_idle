import cv2
import numpy as np
import subprocess
import time
from datetime import datetime
import schedule
import re

ASSETS_FOLDER = './android_assets'


def run_adb_command_subprocess(command):
    result = subprocess.run(f'{command}', shell=True, stdout=subprocess.DEVNULL)
    # result = subprocess.run(f'{command}', shell=True)
    # print(result.stdout)
    return result


def get_android_screenshot():
    take_screenshot_cmd = f'adb shell screencap -p /sdcard/screenshot.png'
    save_screenshot_cmd = f'adb pull /sdcard/screenshot.png ./{ASSETS_FOLDER}/screenshot.png'
    run_adb_command_subprocess(take_screenshot_cmd)
    run_adb_command_subprocess(save_screenshot_cmd)


def template_matching_location(template_path, screenshot_path):
    # Read the template and screenshot images
    template = cv2.imread(template_path)
    screenshot = cv2.imread(screenshot_path)

    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    # print(f'Max val is: {max_val} matching {template_path}')

    # Define a threshold for matching
    threshold = 0.95

    # Check if the maximum correlation value is above the threshold
    if max_val > threshold:
        # Return the coordinates of the top-left corner of the matched region
        return max_loc
    else:
        # Return None if no match is found
        return None


def template_matching(template_path, screenshot_path):
    # Read the template and screenshot images
    template = cv2.imread(template_path)
    screenshot = cv2.imread(screenshot_path)

    # Perform template matching
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Define a threshold for matching
    threshold = 0.95

    # Check if the maximum correlation value is above the threshold
    if max_val > threshold:
        result = True

    else:
        result = False

    # print(result)
    return result


def get_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def get_screen_size():
    # Input string
    get_screen_size_command = 'adb shell wm size'
    result = subprocess.run(get_screen_size_command, shell=True, stdout=subprocess.PIPE, text=True)

    # Use regular expression to extract numbers
    match = re.search(r'(\d+)x(\d+)', result.stdout)
    w, h = 0, 0
    # Check if there is a match
    if match:
        # Extract values and convert to integers
        w = int(match.group(1))
        h = int(match.group(2))

        # Output the values
        print("w:", w)
        print("h:", h)

    else:
        print(f"Pattern not found in get screen size result: {result}.")
    return w, h


def collect_5minbux():
    print(f'{get_time()}: Start collecting 5minbux')
    time.sleep(5)
    # Collect 5minbux
    run_adb_command_subprocess('adb shell input tap 64 670')
    time.sleep(0.5)
    run_adb_command_subprocess('adb shell input tap 256 670')
    time.sleep(0.5)
    run_adb_command_subprocess('adb shell input tap 708 1356')
    print(f'{get_time()}: Finish collecting 5minbux')


def buildfloor():
    print(f'{get_time()}: Start building floor')
    time.sleep(5)

    # Go to top of building
    w, h = get_screen_size()
    run_adb_command_subprocess(f'adb shell input tap {w // 2} {50}')
    time.sleep(2)

    # Click build floor
    get_android_screenshot()
    result_matching = template_matching_location(buildfloor_template_path_arg, screenshot_path_arg)
    if result_matching:
        x, y = result_matching[0], result_matching[1]
        run_adb_command_subprocess(f'adb shell input tap {x} {y}')

    time.sleep(1)

    get_android_screenshot()
    result_matching = template_matching_location(buildfloor_yes_template_path_arg, screenshot_path_arg)
    if result_matching:
        x, y = result_matching[0], result_matching[1]
        run_adb_command_subprocess(f'adb shell input tap {x} {y}')
    print(f'{get_time()}: Finish building floor')


def rebuild():
    print(f'{get_time()}: Rebuilding...')
    time.sleep(5)

    # Check if 100 floor
    # Go to top of building
    w, h = get_screen_size()
    run_adb_command_subprocess(f'adb shell input tap {w // 2} {50}')
    time.sleep(1)

    get_android_screenshot()
    result_matching = template_matching_location(menu_template_path_arg, screenshot_path_arg)
    if result_matching:
        x, y = result_matching[0], result_matching[1]
        run_adb_command_subprocess(f'adb shell input tap {x} {y}')

    time.sleep(0.5)

    get_android_screenshot()
    result_matching = template_matching_location(rebuild_template_path_arg, screenshot_path_arg)
    if result_matching:
        x, y = result_matching[0], result_matching[1]
        run_adb_command_subprocess(f'adb shell input tap {x} {y}')

    time.sleep(0.5)

    get_android_screenshot()
    result_matching = template_matching_location(rebuild_tower_template_path_arg, screenshot_path_arg)
    if result_matching:
        x, y = result_matching[0], result_matching[1]
        run_adb_command_subprocess(f'adb shell input tap {x} {y}')

    time.sleep(0.5)

    get_android_screenshot()
    result_matching = template_matching_location(rebuild_confirm_template_path_arg, screenshot_path_arg)
    if result_matching:
        x, y = result_matching[0], result_matching[1]
        run_adb_command_subprocess(f'adb shell input tap {x} {y}')

    time.sleep(0.5)

    get_android_screenshot()
    result_matching = template_matching_location(rebuild_confirm_template_path_arg, screenshot_path_arg)
    if result_matching:
        x, y = result_matching[0], result_matching[1]
        run_adb_command_subprocess(f'adb shell input tap {x} {y}')

    time.sleep(0.5)

    # Skip tutorial
    get_android_screenshot()
    result_matching = template_matching_location(yes_template_path_arg, screenshot_path_arg)
    if result_matching:
        x, y = result_matching[0], result_matching[1]
        run_adb_command_subprocess(f'adb shell input tap {x} {y}')

    print(f'{get_time()}: Finish rebuilding')


'''
adb shell input tap 148 1992 => second from left
adb shell input tap 74 1992 => first from left
adb shell input tap 64 670 => 5minbux
adb shell input tap 256 670 => 5minbux_second
adb shell input tap 708 1356 => 5minbux_collect
adb shell input tap 564 1362 => center (awesome, continue)
adb shell input tap 990 2118 => back button
'''

liftready_template_path_arg = f'{ASSETS_FOLDER}/liftready.png'
vipready_template_path_arg = f'{ASSETS_FOLDER}/vipready.png'
awesome_template_path_arg = f'{ASSETS_FOLDER}/awesome.png'
backbutton_template_path_arg = f'{ASSETS_FOLDER}/backbutton.png'
continue_template_path_arg = f'{ASSETS_FOLDER}/continue.png'
buildfloor_template_path_arg = f'{ASSETS_FOLDER}/buildfloor.png'
buildfloor_yes_template_path_arg = f'{ASSETS_FOLDER}/buildfloor_yes.png'
menu_template_path_arg = f'{ASSETS_FOLDER}/menu.png'
rebuild_template_path_arg = f'{ASSETS_FOLDER}/rebuild.png'
rebuild_tower_template_path_arg = f'{ASSETS_FOLDER}/rebuild_tower.png'
rebuild_confirm_template_path_arg = f'{ASSETS_FOLDER}/rebuild_confirm.png'
yes_template_path_arg = f'{ASSETS_FOLDER}/yes.png'
hundred_floor_template_path_arg = f'{ASSETS_FOLDER}/100_floor.png'
screenshot_path_arg = f'{ASSETS_FOLDER}/screenshot.png'


# Replace these paths with the actual paths of your template and screenshot

def run():
    epoch = 300000
    epoch_count = 0

    get_android_screenshot()
    buildfloor()
    schedule.every(5).minutes.do(collect_5minbux)
    schedule.every(2.5).minutes.do(buildfloor)

    while epoch_count < epoch:
        print(f'{get_time()}: Epoch {epoch_count}/{epoch}')
        # Take and get device screenshot
        get_android_screenshot()

        # Check lift is ready
        result_matching = template_matching_location(liftready_template_path_arg, screenshot_path_arg)
        if result_matching:
            x, y = result_matching[0], result_matching[1]
            run_adb_command_subprocess(f'adb shell input tap {x} {y}')

        # Wait for lift
        wait_for_lift = 4  # seconds
        while wait_for_lift > 0:
            get_android_screenshot()
            result_matching = template_matching_location(awesome_template_path_arg, screenshot_path_arg)
            if result_matching:
                x, y = result_matching[0], result_matching[1]
                run_adb_command_subprocess(f'adb shell input tap {x} {y}')
                break
            # if template_matching(awesome_template_path_arg, screenshot_path_arg):
            #     run_adb_command_subprocess('adb shell input tap 564 1362')
            #     break
            wait_for_lift -= 1
            time.sleep(1)

        # Press back button if applicable
        get_android_screenshot()
        result_matching = template_matching_location(backbutton_template_path_arg, screenshot_path_arg)
        if result_matching:
            x, y = result_matching[0], result_matching[1]
            run_adb_command_subprocess(f'adb shell input tap {x} {y}')
            # run_adb_command_subprocess(f'adb shell input tap 990 2118')

        # Check continue buttion if applicable
        get_android_screenshot()
        result_matching = template_matching_location(continue_template_path_arg, screenshot_path_arg)
        if result_matching:
            x, y = result_matching[0], result_matching[1]
            run_adb_command_subprocess(f'adb shell input tap {x} {y}')

        # Rebuild if reaches 100th
        get_android_screenshot()
        result = template_matching_location(hundred_floor_template_path_arg, screenshot_path_arg)
        if result:
            x, y = result[0], result[1]
            run_adb_command_subprocess(f'adb shell input tap {x} {y}')
            rebuild()

        schedule.run_pending()
        epoch_count += 1
        time.sleep(1)


def test():
    get_android_screenshot()
    result = template_matching_location(hundred_floor_template_path_arg, screenshot_path_arg)
    print(result)
    if result:
        x, y = result[0], result[1]
        run_adb_command_subprocess(f'adb shell input tap {x} {y}')


run()