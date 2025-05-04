"""
JoystickMouseLocal
==================
Serial → Pygame cursor (no OS SendInput).  Works only while the game window
is focused, so desktop icons stay safe.
"""

import threading
import serial
import time
import pygame

SERIAL_PORT      = "COM6"
BAUDRATE         = 115200
PIXELS_PER_STEP  = 3
FPS_LIMIT        = 144

_DIR_TO_DELTA = {
    "UP":    (0, -PIXELS_PER_STEP),
    "DOWN":  (0,  PIXELS_PER_STEP),
    "LEFT":  (-PIXELS_PER_STEP, 0),
    "RIGHT": ( PIXELS_PER_STEP, 0),
}

class _Worker(threading.Thread):
    daemon = True

    def run(self):
        try:
            ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.01)
        except serial.SerialException as e:
            print(f"[Joystick] {e}")
            return

        clock = pygame.time.Clock()
        active_dir = None  # current held direction
        last_move_time = 0.0
        REPEAT_HZ = 180  # how many moves per second
        MIN_DT = 1.0 / REPEAT_HZ

        while True:
            line = ser.readline().decode(errors="ignore").strip()
            now = time.time()

            # update active direction on any token
            if line in _DIR_TO_DELTA or line == "CENTER":
                active_dir = None if line == "CENTER" else line

            # click still works immediately
            if line == "PRESS":
                pos = pygame.mouse.get_pos()
                for t in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    pygame.event.post(pygame.event.Event(t, {"pos": pos, "button": 1}))

            # continuous movement
            if active_dir and (now - last_move_time) >= MIN_DT:
                dx, dy = _DIR_TO_DELTA[active_dir]
                x, y = pygame.mouse.get_pos()
                w, h = pygame.display.get_window_size()
                pygame.mouse.set_pos(max(0, min(w - 1, x + dx)),
                                     max(0, min(h - 1, y + dy)))
                last_move_time = now

            clock.tick(REPEAT_HZ)


def start_local_mouse():
    _Worker().start()
