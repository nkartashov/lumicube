from enum import Enum
import time
from datetime import datetime


class MODE(Enum):
    LAVA = 0
    MONOCHROME = 1
    RAINBOW = 2


class TIME_MODE(Enum):
    DAY = 0
    NIGHT = 1


STEP_DELAY = 0.025


class State:
    def __init__(self):
        self._mode = MODE.LAVA
        self._time_mode = TIME_MODE.DAY
        self._time_step = 0

    def time_step(self):
        return self._time_step

    def mode(self) -> MODE:
        return self._mode

    def time_mode(self) -> TIME_MODE:
        return self._time_mode

    def set_mode(self, mode: MODE):
        self._mode = mode

    def set_time_mode(self, time_mode: TIME_MODE):
        self._time_mode = time_mode

    def next_step(self):
        self._time_step += 1
        time.sleep(STEP_DELAY)


def lava_colour(x, y, z, t):
    scale = 0.10
    speed = 0.05
    hue = noise_4d(scale * x, scale * y, scale * z, speed * t)
    return hsv_colour(hue, 1, 1)


def paint_cube(t):
    colours = {}
    for x in range(9):
        for y in range(9):
            for z in range(9):
                if x == 8 or y == 8 or z == 8:
                    colour = lava_colour(x, y, z, t)
                    colours[x, y, z] = colour
    display.set_3d(colours)


def draw_moon():
    w = white
    g = grey
    moon = [
        [0, 0, w, w, w, w, g, 0],
        [0, w, w, w, w, w, w, g],
        [w, w, w, w, g, 0, 0, 0],
        [w, w, w, g, 0, 0, 0, 0],
        [w, w, w, g, 0, 0, 0, 0],
        [w, w, w, w, g, 0, 0, 0],
        [0, w, w, w, w, w, w, g],
        [0, 0, w, w, w, w, g, 0],
    ]
    return moon


def draw_sparkles():
    w = white
    p = pink
    sparkles = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, p, 0, 0, 0, 0, 0],
        [0, p, w, p, 0, 0, 0, 0],
        [0, 0, p, 0, 0, p, 0, 0],
        [0, 0, 0, 0, p, w, p, 0],
        [0, 0, p, 0, 0, p, 0, 0],
        [0, p, w, p, 0, 0, 0, 0],
        [0, 0, p, 0, 0, 0, 0, 0],
    ]
    return sparkles


def draw_wizard_fire():
    w = white
    light_blue = hsv_colour(0.6, 0.4, 1)
    blue = hsv_colour(0.6, 0.9, 1)
    b = blue
    l = light_blue
    wizard_fire = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, l, 0, l, 0, 0, 0, 0],
        [l, 0, l, w, l, 0, 0, 0],
        [0, 0, l, l, w, b, 0, 0],
        [0, l, l, w, l, l, b, 0],
        [0, b, w, w, w, l, b, 0],
        [0, b, l, w, w, b, 0, 0],
        [0, 0, b, b, b, 0, 0, 0],
    ]
    return wizard_fire


def draw_heart():
    r = red
    o = orange
    w = white
    heart = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, r, r, 0, 0, r, r, 0],
        [r, w, o, r, r, r, r, r],
        [r, o, r, r, r, r, o, r],
        [0, r, r, r, r, o, r, 0],
        [0, 0, r, r, r, r, 0, 0],
        [0, 0, 0, r, r, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
    ]
    return heart


class MainLoop:
    def __init__(self):
        self._state = State()

    def _lava_lamp_main(self):
        paint_cube(self._state.time_step())

    def _monochrome_main(self):
        hue = (self._state.time_step() % 100) / 100
        display.set_all(hsv_colour(hue, 1, 1))

    def _rainbow_main(self):
        leds = {}
        for y in range(16):
            for x in range(16):
                if x < 8 or y < 8:
                    leds[x, y] = hsv_colour((x + y) / 24, 1, 1)
        display.set_leds(leds)

    def _night_mode_main(self):
        display.set_panel("left", draw_moon())
        display.set_panel("right", draw_sparkles())
        display.set_panel("top", draw_heart())

    def run_mode_switcher(self):
        mode_to_set = buttons.top_pressed_count % len(MODE)
        self._state.set_mode(MODE(mode_to_set))
        now = datetime.now()
        if 9 < now.hour < 21:
            self._state.set_time_mode(TIME_MODE.DAY)
        else:
            self._state.set_time_mode(TIME_MODE.NIGHT)

    def run(self):
        MODES_TO_HANDLER = {
            MODE.LAVA: self._lava_lamp_main,
            MODE.MONOCHROME: self._monochrome_main,
            MODE.RAINBOW: self._rainbow_main,
        }

        while True:
            if self._state.time_mode() == TIME_MODE.DAY:
                try:
                    MODES_TO_HANDLER[self._state.mode()]()
                except KeyError:
                    print(f"Unrecognized mode: {self._state.mode()}")
            elif self._state.time_mode():
                self._night_mode_main()
            self.run_mode_switcher()
            self._state.next_step()


def main():
    main_loop = MainLoop()
    main_loop.run()


main()
