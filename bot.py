import cv2 as cv
import numpy as np
from PIL import Image
from auto_input import *
import login
import os


# all measurements are based on a 1920x1080 screen
# Requirements: in game
# must turn on hide all roofs and shift-click to drop
# must turn NPC attack options to left-click when available


class Bot:
    def __init__(self):
        self.health = 0
        self.prayer = 0
        self.run_energy = 0
        self.special_attack = 0
        self.gold = 0
        self.quest_points = 0
        self.map_dir = ""
        self.view = ""
        self.menu_open = ""
        self.outfit = dict()
        self.skills = dict()
        self.inventory = []
        self.running = False
        self.in_combat = False
        self.moving = False
        self.animating = False
        self.in_building = False
        self.skulled = False
        self.in_wilderness = False
        self.typing = False
        self.analyzing_screen = False

    def look_north(self):
        # set mad dir to north
        self.map_dir = "North"
        # coordinates for middle of the compass button
        north_pos = (1760, 85)
        # look north
        pyautogui.moveTo(add_randomness(north_pos[0], 5), add_randomness(north_pos[1], 5),
                         get_move_to_time(north_pos[0], north_pos[1]))
        time.sleep(0.2)
        pyautogui.click()
        time.sleep(0.2)

    def look_to_right(self):
        # make the player look to the right, then update the map direction they are facing
        pyautogui.keyDown("left")
        time.sleep(0.829)
        pyautogui.keyUp('left')
        time.sleep(0.25)
        if self.map_dir == "North":
            self.map_dir = "East"
        elif self.map_dir == "East":
            self.map_dir = "South"
        elif self.map_dir == "South":
            self.map_dir = "West"
        elif self.map_dir == "West":
            self.map_dir = "North"
            self.setup(self.get_view())
        print(f"Bot now looking {self.map_dir}")

    def set_view(self, view):
        # create an overhead view
        if view == "above":
            self.view = "above"
            # create an overhead view by pressing the up arrow key
            pyautogui.keyDown('up')
            time.sleep(random.uniform(1.8, 2.0))
            pyautogui.keyUp('up')
        elif view == "player":  # create a view that looks at the player level
            self.view = "player"
            pyautogui.keyDown('down')
            time.sleep(random.uniform(1.8, 2.0))
            pyautogui.keyUp('down')

    def get_view(self):
        return self.view

    def setup(self, view):
        # set the fail safe to true, move the mouse to the top left to stop it
        pyautogui.FAILSAFE = True
        # make the player look north
        self.look_north()
        # center the mouse
        center_mouse()
        # look from above the bot
        self.set_view(view)
        # wait 2 seconds after panning upwards so next action isn't immediate
        time.sleep(random.uniform(0.25, 0.50))

    def toggle_running(self):
        # move the mouse and left click to the running emblem and left click it
        move_to_left_click(add_randomness(1760, 2), add_randomness(195, 2))
        if self.running:
            self.running = False
        else:
            self.running = True

    def get_running(self):
        return self.running

    # make a running function that looks at the pixel location on the screen to see if the data orb is yellow or not
    def check_running(self):
        self.running = False

    def get_moving_time(self, x, y):
        # get the distance from the center to the x, y
        distance = sqrt(((center_screen[0] - x) ** 2) + ((center_screen[1] - y) ** 2))
        # get the most updated running status
        self.check_running()
        # assume the size of a tile is 50 pixels looking from above
        tile_size = 0
        if self.view == "above":
            tile_size = 50
        elif self.view == "player":
            tile_size = 85
        # game tick is 0.6 seconds. If walking it takes 1 tick to walk a tile, .5 ticks to walk a tile while running
        # the time moving is 0.6 seconds times the number of tiles moved, which is the amount of pixels / tile size
        num_tiles = distance / tile_size
        tiles_per_second = 0.6
        next_click_scale = 1.25
        time_moving = num_tiles * tiles_per_second * next_click_scale
        # if running the time is in half
        if self.get_running():
            time_moving *= 0.5
        return time_moving

    def move_in_dir(self, direction=None, distance=0):
        # direction: direction to move is left, up, right, down, left-up, right-up, left-down, or right-down
        # time for moving in 1 direction
        if direction == "left" or direction == "up" or direction == "right" or direction == "down":
            t = get_relative_move_time(distance, 0)
        else:  # time for moving in 2 directions
            t = get_relative_move_time(distance, distance)
        # move the mouse in the direction by an amount
        if direction is None:
            pyautogui.moveTo(add_randomness(center_screen[0], 2), add_randomness(center_screen[1], 2), t)
        else:
            if direction == "left":
                pyautogui.moveTo(center_screen[0] + (-1 * distance), center_screen[1], t)
            elif direction == "up":
                pyautogui.moveTo(center_screen[0], center_screen[1] + (-1 * distance), t)
            elif direction == "right":
                pyautogui.moveTo(center_screen[0] + distance, center_screen[1], t)
            elif direction == "down":
                pyautogui.moveTo(center_screen[0], center_screen[1] + distance, t)
            elif direction == "left-up":
                pyautogui.moveTo(center_screen[0] + (-1 * distance), center_screen[1] + (-1 * distance), t)
            elif direction == "right-up":
                pyautogui.moveTo(center_screen[0] + distance, center_screen[1] + (-1 * distance), t)
            elif direction == "left-down":
                pyautogui.moveTo(center_screen[0] + (-1 * distance), center_screen[1] + distance, t)
            elif direction == "right-down":
                pyautogui.moveTo(center_screen[0] + distance, center_screen[1] + distance, t)
            else:
                print("Invalid direction...")
        # after moving the mouse to direction, wait half a second and then click it to move
        time.sleep(random.uniform(0.2, 0.25))
        left_click()
        # change the bots variables to indicate that they are moving and animating
        if direction is not None:
            self.moving = True
            self.animating = True
            time_moving = self.get_moving_time(0, distance)
            # sleep the amount of time that they are moving
            time.sleep(time_moving)
            print("time moving:", time_moving)
            # change the bots variables back to show that they aren't moving or animating anymore
            self.moving = False
            self.animating = False

    # fix
    def fire_making(self):
        # get tinderbox image and location
        tinderbox_pic = Image.open("pics/tinderbox.png")
        tinderbox_pos = pyautogui.locateCenterOnScreen(tinderbox_pic, confidence=.90)
        if tinderbox_pos is None:
            pyautogui.write("tinderbox pic not found", 0.125)
            return
        # open the inventory menu
        self.open_tab("Inventory")
        # load the log image
        log_pic = Image.open("pics/inventory/inventory_logs.png")
        while True:
            # find the picture of the logs on the screen
            log_location = pyautogui.locateCenterOnScreen(log_pic, confidence=.90)
            if log_location is None:
                break
            else:
                # add randomness to log location
                lx, ly = (add_randomness(log_location[0]), add_randomness(log_location[1]))
                # move the mouse to that position
                pyautogui.moveTo(lx, ly, get_move_to_time(lx, ly))
                # wait random amount of time
                time.sleep(random.uniform(.15, .25))
                # press the left-click the logs
                left_click()
                # wait random amount of time
                time.sleep(random.uniform(.15, .25))
                # add randomness to tinderbox location
                tx, ty = (add_randomness(tinderbox_pos[0]), add_randomness(tinderbox_pos[1]))
                # move the mouse to the tinderbox
                pyautogui.moveTo(tx, ty, get_move_to_time(tx, ty))
                # left-click the tinderbox
                left_click()
                # wait (7, 9) random seconds in between clicking another log
                time.sleep(random.uniform(7, 9))
        print("fire-making done...")

    def move_in_square(self, num_times):
        # move right, down, left, then up
        for _ in range(num_times):
            # move right, and wait
            self.move_in_dir("right", 100)
            # move down, and wait
            self.move_in_dir("down", 100)
            # move left, and wait
            self.move_in_dir("left", 100)
            # move up, and wait
            self.move_in_dir("up", 100)

    # fix
    def move_in_diamond(self, num_times):
        # move right, down, left, then up
        for _ in range(num_times):
            # move left, and wait
            self.move_in_dir("left", 100)
            # move right-up, and wait
            self.move_in_dir("right-up", 100)
            # move right-down, and wait
            self.move_in_dir("right-down", 100)
            # move left-down, and wait
            self.move_in_dir("left-down", 100)
            # move left-up, and wait
            self.move_in_dir("left-up", 100)
            # move right, and wait
            self.move_in_dir("right", 100)

    # fix
    def move_to_target_x_y(self, target_x, target_y):
        # the target x and the target y is one specific pixel on the screen
        # get this pixel from image processing and then move to it

        # get the distance in the x and the y direction that the player must move to go to the target
        dx, dy = (target_x - center_screen[0], target_y - center_screen[1])
        # generate a series of x and y points that are within the
        tolerance = 10
        print(f"dx: {dx}, dy:{dy}")
        self.move_in_dir("up", tolerance)

    def open_tab(self, tab):
        tab_exists = True
        if tab == "inventory" and self.menu_open != "inventory":
            # press the escape key to go to the inventory tab
            press_key('esc')
        elif tab == "combat" and self.menu_open != "combat":
            # press the f1 key to go to the combat tab
            press_key('f1')
        elif tab == "skills" and self.menu_open != "skills":
            # press the f2 key to go to the skills tab
            press_key('f2')
        elif tab == "equipment" and self.menu_open != "equipment":
            # press the f4 key to go to the equipment tab
            press_key('f4')
        elif tab == "prayer" and self.menu_open != "prayer":
            # press the f5 key to go to the prayer tab
            press_key('f5')
        elif tab == "magic" and self.menu_open != "magic":
            # press the f6 key to go to the magic tab
            press_key('f6')
        else:
            print("Tab doesn't exist")
            tab_exists = False
        if tab_exists:
            self.menu_open = tab

    def drop_logs(self):
        # open the inventory menu
        self.open_tab("inventory")
        # load the log image
        log_pic = Image.open("pics/inventory/inventory_logs.png")
        while True:
            # find the picture of the logs on the screen
            log_location = pyautogui.locateCenterOnScreen(log_pic, confidence=.90)
            if log_location is None:
                break
            else:
                # add randomness to log location
                mx, my = (add_randomness(log_location[0]), add_randomness(log_location[1]))
                # move the mouse to that position
                pyautogui.moveTo(mx, my,
                                 get_relative_move_time(pyautogui.position()[0] - mx, pyautogui.position()[1] - my))
                # wait random amount of time
                time.sleep(random.uniform(.15, .25))
                # shift click to drop and then wait
                shift_click()
                time.sleep(random.uniform(0.25, 0.50))

    def find_image_on_screen(self, screen_path, image_file_path, found_image_file_path, method,
                             threshold, write_image=False, draw_marker=False):
        # make sure that method is an integer
        method = int(method)
        # All the 6 methods for comparison in a list
        methods = ['cv.TM_CCOEFF', 'cv.TM_CCOEFF_NORMED', 'cv.TM_CCORR',
                   'cv.TM_CCORR_NORMED', 'cv.TM_SQDIFF', 'cv.TM_SQDIFF_NORMED']
        meth = eval(methods[method])
        self.analyzing_screen = True
        # take a picture of the screen
        pyautogui.screenshot(screen_path)
        # read in the template pic
        template = cv.imread(image_file_path, cv.IMREAD_COLOR)
        # read the screen in
        screen = cv.imread(screen_path, cv.IMREAD_COLOR)
        # type on osrs that a screenshot has been taken and then delete it after a second
        pyautogui.typewrite("screen", 0.125)
        time.sleep(1)
        clear_form(0.55)
        # get the result image by comparing the template to the screen using the selected method
        result = cv.matchTemplate(screen, template, meth)
        # threshold value is tweaked to help with determining what is an image and what isn't
        # get the locations on the screen where the result is less than the threshold
        locations = np.where(result <= threshold)
        # locations come as a list of y's and then list of x's, make it x,y then zip them in to a list of (x,y) tuples
        locations = list(zip(*locations[::-1]))
        # cv uses y,x, so height is 0 and width is 1
        template_h = template.shape[0]
        template_w = template.shape[1]
        # get the rectangles around the template on the screen
        rectangles = []
        for loc in locations:
            rect = [loc[0], loc[1], template_w, template_h]
            # append twice so some rectangles don't get lost from the groupRectangles filtering out
            rectangles.append(rect)
            rectangles.append(rect)
        # group the rectangles
        rectangles, weights = cv.groupRectangles(np.array(rectangles).tolist(), 1, 0.5)
        # loop through all the rectangles
        if len(rectangles) > 0:
            # green line color
            line_color = (0, 255, 0)
            line_width = 2
            marker_color = (255, 0, 0)
            for (x, y, w, h) in rectangles:
                top_left = (x, y)
                bottom_right = (x + w, y + h)
                # draw the rectangles
                cv.rectangle(screen, top_left, bottom_right, line_color, line_width)
                if draw_marker:
                    cv.drawMarker(screen, (x + int(w/2), y + int(h/2)), marker_color)
        # save the screen found with the rectangles
        if write_image:
            cv.imwrite(found_image_file_path, screen)
        # remove the screen image so duplicates aren't made
        try:
            os.remove(screen_path)
            print("removed screen.jpg")
        except:
            print("didn't remove screen.jpg")
        self.analyzing_screen = False
        return rectangles

    # expand using type tree so it can cut more than just regular trees
    def find_trees(self, counter, type_tree="tree"):
        print("*" * 20)
        print("looking for trees...")
        print("*" * 20)
        if self.view != "player":
            self.set_view("player")
        # find the tree on the screen
        trees = self.find_image_on_screen("pics/trees/screen.jpg", f"pics/trees/{type_tree}_trunk.png",
                                          f"pics/trees/found_trees{counter}.jpg", int(5), 0.07, True, False)
        print("*" * 20)
        print(f"done looking for trees... found: {len(trees)}")
        print("*" * 20)
        self.analyzing_screen = False
        return trees

    # fix
    def wood_cutting(self, num_trees, type_tree="tree", make_fire=False):
        print("*" * 20)
        print("starting woodcutting...")
        print("*" * 20)
        trees_chopped = 0
        while trees_chopped < num_trees:
            # check the screen for trees
            trees = self.find_trees(trees_chopped, type_tree)
            # if trees were found
            if len(trees) > 0:
                first_tree = trees[0]
                tree_center = (first_tree[0] + int(first_tree[2]/2), first_tree[1] + int(first_tree[3]/2))
                print("tree:", first_tree)
                # go to first tree and click it, with a little added randomness to the lower right section of location
                move_to_left_click(tree_center[0], tree_center[1])
                # sleep the time needed to move to the tree
                time.sleep(self.get_moving_time(trees[0][0], trees[0][1]))
                # sleep the time needed to chop the tree
                time.sleep(random.uniform(6, 6.5))
                print(f"tree chopped down...{trees_chopped}")
                # a tree was cut done
                trees_chopped += 1
                if make_fire:
                    self.fire_making()
                    print("fire made...")
                    time.sleep(random.uniform(6, 6.5))
            else:  # if no trees were found, write it out and then break out of the woodcutting loop
                print("no trees found")
                pyautogui.write("none", 0.125)
                clear_form(0.5)
                # if there aren't any trees around, keep looking right until the bot sees some
                self.look_to_right()
        print("*" * 20)
        print("finishing woodcutting...")
        print("*" * 20)

    # fix
    def check_in_building(self):
        # checks to see if bot is in a building or not
        return self.in_building

    # fix
    def check_door_stuck(self):
        pass

    # fix
    def check_skulled(self):
        return self.skulled

    # fix
    def check_in_wilderness(self):
        return self.in_wilderness

    def send_message(self, message):
        # bot started typing
        self.typing = True
        # type each letter with different intervals to make it look more random
        for letter in message:
            pyautogui.write(letter, random.uniform(.15, .2))
        # send the message
        pyautogui.write('\n', .10)
        # bot stopped typing
        self.typing = False

    def auto_click(self, num_times, direction, distance, refresh_rate):
        for _ in range(num_times):
            self.move_in_dir(direction, distance)
            time.sleep(refresh_rate)

    def find_bank_clerk(self):
        pass

    def open_bank(self):
        pass

    def find_ge_clerk(self):
        pass

    def open_ge(self):
        pass

    def flip_items(self, items):
        # items is a list of things you wish to trade
        pass


def main():
    # window pops up to start or abort the script
    conf_win = pyautogui.confirm(text='Start the bot by clicking start, abort by clicking cancel or by closing window',
                                 title='Menu', buttons=['Start', 'Cancel'])

    # clicking cancel button or the close button will abort the script
    if conf_win == 'Cancel' or conf_win is None:
        return
    else:
        # go to the window and then click Start and the program will start in one second
        time.sleep(1)

    # Make the bot
    bot = Bot()

    # login to the osrs with the credentials in the login_credentials.txt
    # login.log_in()

    # actions to do while bot is made
    bot.setup("player")
    time.sleep(0.25)

    bot.wood_cutting(3)
    time.sleep(0.25)

    # actions completed
    pyautogui.write("done", 0.10)

    # time.sleep(0.5)
    # log out of the account
    # login.log_out()


if __name__ == "__main__":
    main()
