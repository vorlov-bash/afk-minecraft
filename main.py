import time
import random
from typing import Literal

from pynput.keyboard import Key, Controller as KController
from pynput.mouse import Button, Controller as MController
from tqdm import tqdm

from window import MinecraftWindow


class Controller:
    def __init__(self, window: MinecraftWindow, mouse=None, keyboard=None):
        self.window = window

        if mouse is None:
            self.mouse = MController()
        else:
            self.mouse = mouse

        if keyboard is None:
            self.keyboard = KController()
        else:
            self.keyboard = keyboard

    def step(self, key: str, sec: int = 5):
        print(f'Start step "{key}" for {sec} sec')
        self.keyboard.press(key)
        time.sleep(sec)
        self.keyboard.release(key)
        print(f'Stop step "{key}" for {sec} sec')

    def make_mouse_direction_action(
            self, direction: Literal['left', 'right', 'up', 'down'],
            size: int,
            speed: int = 10,
            output: bool = True
    ):
        if output: print(f'Start moving mouse to "{direction}"')

        if direction == 'left':
            for i in range(size // speed):
                self.mouse.move(-speed, 0)
                time.sleep(0.00000000001)

        if direction == 'right':
            for i in range(size // speed):
                self.mouse.move(speed, 0)
                time.sleep(0.00001)

        if direction == 'up':
            for i in range(size // speed):
                self.mouse.move(0, -speed)
                time.sleep(0.00001)

        if direction == 'down':
            for i in range(size // speed):
                self.mouse.move(0, speed)
                time.sleep(0.00001)

        if output: print(f'Stop moving mouse to {direction}')

    def make_inventory_actions(self):
        print('Start inventory actions')
        self.keyboard.press('e')
        self.keyboard.release('e')
        self.make_mouse_direction_action('left', 60)
        self.make_mouse_direction_action('up', 60)
        self.make_mouse_direction_action('right', 60)
        self.make_mouse_direction_action('down', 60)
        self.keyboard.press(Key.esc)
        self.keyboard.release(Key.esc)
        print('Stop inventory actions')

    def take_a_snack(self):
        self.keyboard.press(str(random.randint(1, 9)))
        print('Start taking a snack')
        self.mouse.press(Button.right)
        time.sleep(4)
        self.mouse.release(Button.right)
        print('Stop taking a snack')

    def iteration(self):
        self.step(random.choice(('w', 'a', 's', 'd', Key.space)), random.randint(1, 5))
        self.make_mouse_direction_action(
            direction=random.choice((
                'left',
                'right',
            )),
            size=random.randint(1700, 2300)
        )
        self.step(random.choice(('w', 'a', 's', 'd', Key.space)), random.randint(1, 5))
        self.make_mouse_direction_action(
            direction=random.choice((
                'left',
                'right',
            )),
            size=random.randint(1700, 2300)
        )

    def is_cursor_out_of_window(self):
        self.mouse.position = (self.window.mx, self.window.my)
        self.make_mouse_direction_action('left', size=1000, speed=30, output=False)

        mouse_x, mouse_y = self.mouse.position

        if mouse_x < self.window.x1 or mouse_x > self.window.x2 or mouse_y < mouse_y or mouse_y > self.window.y2:
            return True
        return False

    def run(self):
        i = 0
        while True:
            print(f'=== Iteration {i} ===')
            while self.is_cursor_out_of_window():
                print(self.window.mx, self.window.my)
                self.mouse.position = (self.window.mx, self.window.my + 180)
                self.mouse.click(Button.left)
                self.mouse.position = (self.window.mx, self.window.my)
                time.sleep(1)
                self.mouse.click(Button.left, 2)
                time.sleep(30)

            if i >= 5 and i % 5 == 0:
                self.take_a_snack()

            if i >= 5 and i % 5 == 0:
                self.make_inventory_actions()
            self.iteration()
            i += 1


if __name__ == '__main__':
    print('''
                __ _      __  __ _             _____ _ _            _   
         /\    / _| |    |  \/  (_)           / ____| (_)          | |  
        /  \  | |_| | __ | \  / |_ _ __   ___| |    | |_  ___ _ __ | |_ 
       / /\ \ |  _| |/ / | |\/| | | '_ \ / _ \ |    | | |/ _ \ '_ \| __|
      / ____ \| | |   <  | |  | | | | | |  __/ |____| | |  __/ | | | |_ 
     /_/    \_\_| |_|\_\ |_|  |_|_|_| |_|\___|\_____|_|_|\___|_| |_|\__|
    ''')

    pbar = tqdm(bar_format='{desc}...', leave=False)
    pbar.set_description('Capturing mouse')
    time.sleep(random.randint(1, 3))
    _mouse = MController()
    pbar.set_description('Capturing keyboard')
    time.sleep(random.randint(1, 3))
    _keyboard = KController()
    pbar.set_description('Preparing minecraft window')

    window = MinecraftWindow('Excalibur')
    window.prepare()
    time.sleep(1)

    pbar.clear()
    pbar.close()

    _mouse.position = (window.mx, window.my)

    c = Controller(window)
    c.run()
