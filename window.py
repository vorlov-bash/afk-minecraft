import win32gui
import win32con


class MinecraftWindow:
    def __init__(self, window_title: str):
        self.window_title = window_title

        self.x1 = 0
        self.y1 = 0

        self.x2 = 0
        self.y2 = 0

        self.mx = 0
        self.my = 0

        self.hwnd = None

    def prepare(self):
        def callback(hwnd, extra):
            wtext = win32gui.GetWindowText(hwnd)
            if self.window_title in wtext:
                self.hwnd = hwnd

                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                # x = win32gui.GetWindowPlacement(hwnd)
                # win32gui.SetActiveWindow(hwnd)

                self.x1, self.y1, self.x2, self.y2 = win32gui.GetWindowRect(hwnd)
                self.mx, self.my = (self.x1 + self.x2) / 2, (self.y1 + self.y2) / 2

                # mouse.position = (x1, y1)
                # make_mouse_direction_action('right', x2 - x1, speed=40, output=False)
                # make_mouse_direction_action('down', y2 - y1, speed=40, output=False)
                # make_mouse_direction_action('left', x2 - x1, speed=40, output=False)
                # make_mouse_direction_action('up', y2 - y1, speed=40, output=False)
                #
                # mouse.position = (mx, my)

        win32gui.EnumWindows(callback, None)

    def focus(self, mouse):
        win32gui.SetForegroundWindow(self.hwnd)
        # mouse.position = (x1, y1)
        # make_mouse_direction_action('right', x2 - x1, speed=40, output=False)
        # make_mouse_direction_action('down', y2 - y1, speed=40, output=False)
        # make_mouse_direction_action('left', x2 - x1, speed=40, output=False)
        # make_mouse_direction_action('up', y2 - y1, speed=40, output=False)
        #
        # mouse.position = (mx, my)

w = MinecraftWindow('Excalibur-Craft')
w.prepare()
print(w.mx, w.my)
