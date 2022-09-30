from enum import Enum
import time


class MODE(Enum):
    LAVA = 0
    MONOCHROME = 1


STEP_DELAY = 0.025


class State:
    def __init__(self):
        self._mode = MODE.LAVA
        self._time_step = 0

    def time_step(self):
        return self._time_step

    def mode(self) -> MODE:
        return self._mode

    def set_mode(self, mode: MODE):
        self._mode = mode

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


def lava_lamp_main(step):
    paint_cube(step)


def monochrome_main(step):
    hue = (step % 100) / 100
    display.set_all(hsv_colour(hue, 1, 1))


def run_mode_switcher(state: State):
    mode_to_set = buttons.top_pressed_count % len(MODE)
    state.set_mode(MODE(mode_to_set))


def main():
    state = State()
    while True:
        if state.mode() == MODE.LAVA:
            lava_lamp_main(state.time_step())
        elif state.mode() == MODE.MONOCHROME:
            monochrome_main(state.time_step())
        run_mode_switcher(state)
        state.next_step()


main()
