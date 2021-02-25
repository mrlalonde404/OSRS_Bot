import pyautogui
import time
from math import sqrt
import random

# mouse move speed, dots per second
dps = 600

# inventory region
inventory_region = (1718, 704, 1918, 972)

# player center of map, where the player is in the map
map_center = (1839, 150)

# get the size of the screen
size = pyautogui.size()

# get the center of the screen
center_screen = (int(size[0] / 2), int(size[1] / 2))


# move the mouse to the exact center of the screen
def center_mouse():
    print(f"mouse centered: moved mouse to {center_screen}")
    pyautogui.moveTo(center_screen[0], center_screen[1], get_move_to_time(center_screen[0], center_screen[1]))


# left-click where the mouse is located
def left_click():
    # print("left click")
    pyautogui.click()


# right-click where the mouse is located
def right_click():
    # print("right click")
    pyautogui.rightClick()


# left-click while pressing down on shift
def shift_click():
    # press the shift button
    pyautogui.keyDown('shift')
    # wait random amount of time
    time.sleep(random.uniform(.15, .25))
    # press the left-click the logs
    left_click()
    # wait random amount of time
    time.sleep(random.uniform(.15, .25))
    # release the shift button to complete the shift+left-click on the logs
    pyautogui.keyUp('shift')


# move to a specific x,y and then left click it
def move_to_left_click(x, y):
    pyautogui.moveTo(x, y, get_move_to_time(x, y))
    time.sleep(0.25)
    left_click()
    time.sleep(0.25)


# For mouse move times
def get_relative_move_time(dx, dy):
    # get the overall distance from relative position to dx and dy position
    d = int(sqrt((dx ** 2) + (dy ** 2)))
    # return the time of the distance in pixel divided by the velocity in dots per second
    return d / dps


# For mouse move times
def get_move_to_time(x, y):
    sx = pyautogui.position()[0]
    sy = pyautogui.position()[1]
    d = sqrt(((sx - x) ** 2) + ((sy - y) ** 2))
    return d / dps


def add_randomness(pos, amount=10):
    return pos + random.randint(-amount, amount)


# delete everything in a text form
def clear_form(num_secs):
    pyautogui.keyDown("backspace")
    time.sleep(num_secs)
    pyautogui.keyUp("backspace")
    time.sleep(0.25)


def press_key(key, times=1):
    for _ in range(times):
        pyautogui.keyDown(key)
        time.sleep(random.uniform(0.05, 0.10))
        pyautogui.keyUp(key)
        if times > 1:
            time.sleep(random.uniform(0.02, 0.10))


# fix
def random_mouse_to_x_y():
    pass
