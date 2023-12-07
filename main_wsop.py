import _thread

from helper import *


def find_template(template_path, screenshot_path, threshold=0.8):
    # Load the template and screenshot images
    template = cv2.imread(template_path)
    screenshot = pyautogui.screenshot()
    screenshot = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)

    # Match the template in the screenshot
    result = cv2.matchTemplate(screenshot, template, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    # Get the coordinates of the matched template
    template_width, template_height = template.shape[1], template.shape[0]
    top_left = max_loc
    bottom_right = (top_left[0] + template_width, top_left[1] + template_height)

    # Get the confidence score
    confidence = max_val

    # Check if confidence is above the threshold
    if confidence >= threshold:
        print(f'Matching {template_path} with confidence {confidence} and threshold is {threshold}')
        return top_left, bottom_right, confidence
    else:
        return None, None, None


def click_on_template(template_path, threshold=0.95):
    # Find the template in the screenshot
    template_info = find_template(template_path, None, threshold)

    if template_info[0]:
        # Click on the center of the template
        center_x = (template_info[0][0] + template_info[1][0]) // 2
        center_y = (template_info[0][1] + template_info[1][1]) // 2

        pyautogui.click(center_x, center_y)
        print(f"Clicked on the template at coordinates: ({center_x}, {center_y}) with confidence: {template_info[2]}")
    else:
        print("Template not found or confidence below threshold.")


def click_check():
    # Replace 'path_to_template_image.png' with the actual path to your template image
    template_path = 'check.png'
    # Click on the template
    click_on_template(template_path)


def click_bet1x():
    # Replace 'path_to_template_image.png' with the actual path to your template image
    template_path = 'bet1x.png'
    # Click on the template
    click_on_template(template_path)


def click_call7m():
    # Replace 'path_to_template_image.png' with the actual path to your template image
    template_path = 'call7m.png'
    # Click on the template
    click_on_template(template_path)


def mainloop(seconds_to_run):
    time_started = datetime.now()
    a_list = []

    while not a_list:
        main()


def main():
    # click_call7m()
    click_check()
    time.sleep(1)
    click_bet1x()
    time.sleep(1)


mainloop(9999999999)
