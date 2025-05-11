"""
SpeakerController – routes game events to DFPlayer via the shared
serial queue in JoystickMouse.send_command().
"""
from JoystickMouse import send_command
import time

class SpeakerController:
    def play_start(self):
        send_command("START_SND")

    def play_end(self):
        send_command("END_SND")

    def start_background(self):
        send_command("BG_START")

    def stop_background(self):
        send_command("BG_STOP")
        time.sleep(0.2)