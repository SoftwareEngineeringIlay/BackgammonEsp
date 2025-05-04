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
PIXELS_PER_STEP  = 25
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
            ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.02)
        except serial.SerialException as e:
            print(f"[JoystickMouseLocal] ⚠ {e}")
            return

        clock       = pygame.time.Clock()
        last_dir    = None
        last_move   = 0.0
        MIN_DT      = 1.0 / 120.0     # max 60 cursor moves per sec

        while True:
            line = ser.readline().decode(errors="ignore").strip()
            now  = time.time()

            if line == "PRESS":
                # Synthesise a click at current cursor pos
                pos = pygame.mouse.get_pos()
                for etype in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP):
                    pygame.event.post(pygame.event.Event(etype,
                                                         {"pos": pos,
                                                          "button": 1}))
                continue

            if line in _DIR_TO_DELTA:
                if line == last_dir and (now - last_move) < MIN_DT:
                    continue
                dx, dy = _DIR_TO_DELTA[line]
                x, y   = pygame.mouse.get_pos()
                w, h   = pygame.display.get_window_size()
                pygame.mouse.set_pos(max(0, min(w-1, x+dx)),
                                     max(0, min(h-1, y+dy)))
                last_dir  = line
                last_move = now

            clock.tick(FPS_LIMIT)

def start_local_mouse():
    _Worker().start()
