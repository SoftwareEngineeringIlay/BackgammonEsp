"""
RingController (shared‑port edition)
===================================
Sends GAME_START / GAME_END to the ESP32 *via* the joystick thread so
only one Serial handle exists.
"""
from JoystickMouse import send_command


class RingLightController:
    def start_game(self) -> None:
        send_command("GAME_START")

    def end_game(self) -> None:
        send_command("GAME_END")
