
import pyautogui
import time


default_click_delay = .06
region_level_hire = (15, 215, 380, 840)
region_current_stage = (1300, 135, 270, 40)
region_name_check = (260, 270, 620, 800)


def get_image_path(image_name):
    return "images\\" + image_name


def move_mouse_to_level_safe_location():
    pyautogui.moveTo(890, 1030)


def click_image_center(image_name, multiple=False,
                       num_clicks=1, gray_scale=True, confidence=.9, check_region=None):
    image_location = get_image_path(image_name)
    try:
        if multiple:
            all_matches = list(pyautogui.locateAllOnScreen(image_location, grayscale=gray_scale,
                                                           region=check_region, confidence=confidence))
            all_matches.reverse()
            for match in all_matches:
                pyautogui.moveTo(pyautogui.center(match))
                pyautogui.click(clicks=num_clicks, interval=default_click_delay/2)
            time.sleep(default_click_delay)
        else:
            match = pyautogui.locateOnScreen(image_location, grayscale=gray_scale, confidence=confidence)
            pyautogui.click(pyautogui.center(match), clicks=num_clicks, interval=default_click_delay)
    except TypeError:
        print("failed to click the center of:\t{}".format(image_name))


def click_play():
    print("clicking play")
    click_image_center("play_button.png", gray_scale=True, check_region=(825, 40, 300, 150))


def is_boss():
    return pyautogui.locateOnScreen("images\\boss_timer.png", confidence=.7,
                                    region=(1270, 170, 200, 200)) is not None


def attack(num_attacks=20):
    pyautogui.click(1400, 600, num_attacks, interval=default_click_delay)


def move_to_scroll_location():
    pyautogui.click(430, 563)


def scroll_bottom_heroes():
    move_to_scroll_location()
    pyautogui.scroll(-1000000000)
    time.sleep(1)


def next_level():
    print("attempting to move to next level...")
    current_level_img = get_level_image()
    pyautogui.click(1555, 77, clicks=5, interval=.1)
    if pyautogui.locateOnScreen(current_level_img, region=region_current_stage, confidence=.99) is None:
        print("successfully moved to next region")
    else:
        print("cannot move to next region currently")


def get_level_image():
    return pyautogui.screenshot(region=region_current_stage)


def scroll_next_set_heroes():
    print("scrolling up")
    if pyautogui.locateOnScreen("images\\cid.png", confidence=.7, region=region_name_check) is not None:
        print("ok I got all the heroes")
        return False
    move_to_scroll_location()
    pyautogui.scroll(800)
    time.sleep(.5)
    return True


def level_hero():
    click_image_center("level_up.png", True, 10, False, check_region=region_level_hire, confidence=.9)


def level_up():
    print("leveling up heroes...")
    scroll_bottom_heroes()
    level_hero()
    while scroll_next_set_heroes():
        level_hero()


def hire_hero():
    click_image_center("hire.png", True, 3, False, check_region=region_level_hire, confidence=.9)


def hire():
    print("hiring heroes...")
    scroll_bottom_heroes()
    hire_hero()
    while scroll_next_set_heroes():
        hire_hero()


if __name__ == '__main__':

    time.sleep(3)
    while True:
        hire()
        level_up()
        next_level()
        if is_boss():
            print("currently attacking some boss")
            attack(int(35/default_click_delay))
        else:
            print("attacking normal minions")
            attack(100)
