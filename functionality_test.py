from helper import *
import schedule
import time


set_up_for_auto()


def vip_recognition():
    is_matched, center_x, center_y, num_matches = click_by_image_name('lobby.png', yes_click=True)

    is_matched, center_x, center_y, num_matches = click_by_image_name('vip_bigspender.png',
                                                                      yes_click=False,
                                                                      yes_move=True)
    print(f'Number of VIP spender: {num_matches}')

    is_matched, center_x, center_y, num_matches = click_by_image_name('vip_celeb.png',
                                                                      yes_click=False,
                                                                      yes_move=True)
    print(f'Number of VIP celeb: {num_matches}')

    is_matched, center_x, center_y, num_matches = click_by_image_name('vip_agent.png',
                                                                      yes_click=False,
                                                                      yes_move=True
                                                                      )
    print(f'Number of VIP agent: {num_matches}')

    is_matched, center_x, center_y, num_matches = click_by_image_name('vip_stock.png',
                                                                      yes_click=False,
                                                                      yes_move=True)
    print(f'Number of VIP full stock: {num_matches}')

    is_matched, center_x, center_y, num_matches = click_by_image_name('vip_billionaire.png',
                                                                      yes_click=False,
                                                                      yes_move=True
                                                                      )
    print(f'Number of VIP billionaire: {num_matches}')

    is_matched, center_x, center_y, num_matches = click_by_image_name('vip_influencer.png',
                                                                      yes_click=False,
                                                                      yes_move=True)
    print(f'Number of VIP influencer: {num_matches}')


def back_to_mainscreen():
    click_by_image_name('cancel.png')
    click_by_image_name('back_button.png')


def get_techtree_point():
    click_by_image_name('menu.png')
    click_by_image_name('techtree.png')
    click_by_image_name('techtree_collect.png')
    back_to_mainscreen()
    back_to_mainscreen()
    back_to_mainscreen()

schedule.every(361).minutes.do(get_techtree_point)

# while True:
#     schedule.run_pending()
#     time.sleep(1)