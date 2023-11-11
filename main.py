import _thread

from helper import *


def parachuteClick():
    logger.info(f'Started at {pyautogui.position()}')
    click_by_image_name('parachute.png')
    time.sleep(0.5)
    is_matched, _, _, _ = click_by_image_name('nothanks_parachute.png')
    if not is_matched:
        # Check for continue
        click_by_image_name('continue.png')
    # click_by_image_name('nothanks_parachute.png')


def restock():
    click_by_image_name('restock.png')
    click_by_image_name('yes_restock.png')
    click_by_image_name('continue.png')


def go_to_building_top():
    global start, size, GAME_REGION

    '''

    1. Check loop if is_at_top
    2. If not, keep clicking midtop point

    :return:
    '''
    is_matched, _, _, _ = click_by_image_name('buildfloor.png', yes_click=False)
    max_try = 4
    while not is_matched and max_try > 0:
        is_matched, _, _, _ = click_by_image_name('buildfloor.png', yes_click=False)
        # logger.info(f'Move to {topleft}')
        # pyautogui.moveTo(topleft)
        logger.info('Go to top of building now')
        midtop = (start[0] + (start[0] // 2), start[1] + 20)
        logger.info(f'Click cursor on {midtop}')
        pyautogui.click(midtop)

        # Check for continue
        click_by_image_name('continue.png')
        max_try = max_try - 1
    logger.info('At top of building now. Exit go_to_building_top')


def check_and_collect_5minbux():
    is_matched, x_gift, y_gift, num_matches = click_by_image_name('5minbux.png')
    if is_matched:
        # Click next to 5min bux icon
        if size[1] > 900:
            pyautogui.click(x_gift + 120, y_gift)
        else:
            pyautogui.click(x_gift + 80, y_gift)
        time.sleep(0.5)
        # Click collect 5min bux
        is_matched, x_gift, y_gift, num_matches = click_by_image_name('5minbux_collect.png')


def check_lift_and_click():
    # Check if lift is ready
    '''

    1. Check if lift is ready
    2. Click on lift icon if available

    :return:
    '''
    is_matched, x1_gift, y1_gift, num_matches = click_by_image_name('liftready.png', yes_click=True)
    # is_matched, x2_gift, y2_gift = click_by_image_name('liftready.png', yes_click=False)
    # if abs(x1_gift - x2_gift) < 30 and abs(y1_gift - y2_gift) < 30:
    #     click_by_image_name('liftready.png')


def check_techtree():
    '''
    1. Click Menu
    2. Click TechTree
    3. Return to MainScreen - loop

    :return:
    '''


def back_to_mainscreen():
    click_by_image_name('cancel.png')
    click_by_image_name('back_button.png')
    # Check for continue
    click_by_image_name('continue.png')


def get_techtree_point():
    logger.info('Starting get_techtree_point')
    click_by_image_name('menu.png')
    click_by_image_name('techtree.png')
    click_by_image_name('techtree_collect.png')
    back_to_mainscreen()
    back_to_mainscreen()
    back_to_mainscreen()
    logger.info('Exiting get_techtree_point')


def check_and_get_tech_point():
    click_by_image_name('back_button.png')


def enter_raffle():
    click_by_image_name('back_button.png')


def click_awesome():
    click_by_image_name('awesome.png')


def build_new_floor():
    # TODO: read current money and see if it's enough to build floor - right now pacing it 30 mins between
    # TODO: building floor
    go_to_building_top()
    click_by_image_name('buildfloor.png')
    click_by_image_name('buildfloor_yes.png')
    click_by_image_name('buildfloor_continue.png')


def run_job_at_specific_time(job_func, specific_time):
    schedule.every().day.at(specific_time).do(job_func)


def mainloop(seconds_to_run):
    global start, size, GAME_REGION
    time_started = datetime.now()
    a_list = []

    # _thread.start_new_thread(input_thread, (a_list,))

    # Set up schedule tasks:
    schedule.every(21).minutes.do(get_techtree_point)
    schedule.every(31).minutes.do(build_new_floor)
    schedule.every(61).minutes.do(set_up_for_auto)

    # Set the specific time in HH:MM format (00:27)
    specific_time = "00:01"
    run_job_at_specific_time(click_awesome, specific_time)
    # Run once and let schedule do the job
    get_techtree_point()
    build_new_floor()
    start, size, GAME_REGION = set_up_for_auto()

    while not a_list:
        main()
        # time.sleep(1)
        # restock()
        # time.sleep(1)
        time_now = datetime.now()
        if (time_now - time_started).total_seconds() > seconds_to_run:
            break
        time.sleep(1)
        logger.info('Started running all scheduled jobs')
        schedule.run_pending()
        logger.info('Finished running all scheduled jobs')
        time.sleep(1)


def main():
    logger.debug(f'start is {start}, size is {size}')
    # parachuteClick()
    check_and_collect_5minbux()
    check_lift_and_click()
    # go_to_building_top()
    # parachuteClick()
    back_to_mainscreen()


def input_thread(a_list):
    input()  # use input() in Python3
    a_list.append(True)


if __name__ == '__main__':
    start, size, GAME_REGION = set_up_for_auto()

    # logger.info(f'GAME_REGION: {GAME_REGION}')
    mainloop(99999999)
    # main()
