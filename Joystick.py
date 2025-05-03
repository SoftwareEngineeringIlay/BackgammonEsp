# joystick.py
"""
Standalone module to read joystick data from ESP32 over serial,
compute direction (including button press) and emit Pygame USEREVENTs.
"""
import pygame
import serial
import threading
import time

# Configuration: adjust SERIAL_PORT to your ESP32 USB port
SERIAL_PORT   = 'COM6'
BAUDRATE      = 115200
JOY_DEADZONE  = 200    # same units as analogRead (0–4095)
JOY_THRESHOLD = 2048
POLL_INTERVAL = 0.05   # seconds between reads

# Define custom Pygame event for joystick
JOY_EVENT = pygame.USEREVENT + 1

def get_joystick_direction(x, y, btn_pressed):
    """
    Exactly the same deadzone/threshold logic as your Arduino:
    PRESS if button down, otherwise CENTER/UP/DOWN/LEFT/RIGHT.
    """
    x_dev = x - JOY_THRESHOLD
    y_dev = y - JOY_THRESHOLD

    if btn_pressed:
        return 'PRESS'
    if abs(x_dev) < JOY_DEADZONE and abs(y_dev) < JOY_DEADZONE:
        return 'CENTER'
    if abs(x_dev) > abs(y_dev):
        return 'LEFT' if x_dev < 0 else 'RIGHT'
    else:
        return 'UP' if y_dev < 0 else 'DOWN'

def _reader_thread(port, baud, callback):
    """
    Low-level reader: accumulates incoming bytes, splits on '\n',
    and attempts to parse exactly three integers per line.
    """
    ser = serial.Serial(port, baud, timeout=0)
    buf = ''

    while True:
        data = ser.read(64).decode('ascii', errors='ignore')
        if data:
            buf += data
            # Process all complete lines
            while '\n' in buf:
                line, buf = buf.split('\n', 1)
                line = line.strip()
                # Expect exactly three comma-separated numeric fields
                parts = line.split(',')
                if len(parts) == 3 and all(p.isdigit() for p in parts):
                    x, y, b = map(int, parts)
                    # Debug print to confirm correct parsing
                    print(f"DEBUG CSV → x={x}, y={y}, btn={b}")
                    direction = get_joystick_direction(x, y, b == 0)
                    callback(direction)
                # else: ignore any non-CSV debug lines
        time.sleep(POLL_INTERVAL)

class JoystickReader(threading.Thread):
    """
    Thread wrapping the _reader_thread function.
    Posts high-level JOY_EVENTs into Pygame.
    """
    def __init__(self, port, baud, callback):
        super().__init__(daemon=True)
        self.port = port
        self.baud = baud
        self.callback = callback

    def run(self):
        _reader_thread(self.port, self.baud, self.callback)

    def close(self):
        # Optionally implement if you need to clean up the serial port
        pass

# Example standalone test:
if __name__ == '__main__':
    pygame.init()

    def post_dir(direction):
        print(f"CALLBACK → {direction}")
        evt = pygame.event.Event(JOY_EVENT, {'dir': direction})
        pygame.event.post(evt)

    reader = JoystickReader(SERIAL_PORT, BAUDRATE, post_dir)
    reader.start()

    screen = pygame.display.set_mode((200, 200))
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == JOY_EVENT:
                print(f"EVENT → {event.dir}")

        screen.fill((30, 30, 30))
        pygame.display.flip()
        clock.tick(30)

    reader.close()
    pygame.quit()
