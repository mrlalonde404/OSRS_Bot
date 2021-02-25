from auto_input import *
from PIL import Image


def log_in():
    # get the login credentials
    f = open("login_credentials.txt", 'r')
    lines = f.readlines()
    # open the language offset pic
    lang = Image.open("pics/language_offset.png")
    language_loc = pyautogui.locateCenterOnScreen(lang, confidence=0.90)

    # make an adjustment for if the language option is on the client login screen
    language_adj = 0
    # if the image is on the screen, make an adjustment of 20 pixels, otherwise, go with the original locations
    if language_loc is not None:
        print("language login option is present")
        language_adj = 20
    else:
        print("language option not found")
    # press the first button for existing users
    move_to_left_click(1020, 356 + language_adj)
    # go to the username slot, left click it
    move_to_left_click(978, 311 + language_adj)
    # do a backspace to delete everything in the username/email slot
    clear_form(2.5)
    # enter the username
    pyautogui.typewrite(lines[0], 0.125)
    # go to the password slot, left click it
    move_to_left_click(978, 331 + language_adj)
    # enter the password
    pyautogui.typewrite(lines[1], 0.125)
    # click the world button
    move_to_left_click(632, 541 + language_adj)
    # change the world to the f2p - trade world, 301
    move_to_left_click(675, 108 + language_adj)
    # press the login button
    move_to_left_click(883, 383 + language_adj)
    # wait and then press the play button, then waits for 2 seconds
    time.sleep(10)
    move_to_left_click(956, 394)
    time.sleep(2)


def log_out():
    # get the logout x button, get a random part on it
    logout_x_button = (1905, 80)
    logout_x_button_rand = (add_randomness(logout_x_button[0]), add_randomness(logout_x_button[1]))

    # move the mouse to the x button, wait, left-click it, and then wait again
    pyautogui.moveTo(logout_x_button_rand[0], logout_x_button_rand[1],
                     get_move_to_time(logout_x_button_rand[0], logout_x_button_rand[1]))
    time.sleep(random.uniform(0.25, 0.50))
    left_click()
    time.sleep(random.uniform(0.25, 0.50))

    # get the click here to logout button, get the random part of it
    click_logout_button = (1816, 937)
    click_logout_button_rand = (add_randomness(click_logout_button[0]), add_randomness(click_logout_button[1]))

    # move the mouse to the click here to logout button, wait, left-click it, and then wait again
    pyautogui.moveTo(click_logout_button_rand[0], click_logout_button_rand[1],
                     get_move_to_time(click_logout_button_rand[0], click_logout_button_rand[1]))
    time.sleep(random.uniform(0.25, 0.50))
    left_click()
    time.sleep(random.uniform(0.25, 0.50))