import pygame
import sys
from GUI import BackgammonGUI
from Screen import LoginScreen, WinningScreen
from Files import Data
from copyright import Copyright
from JoystickMouse import start_local_mouse
from RingController import RingLightController
from SpeakerController import SpeakerController

class GameManager:
    def __init__(self):
        pygame.init()
        pygame.mouse.set_visible(True)
        start_local_mouse()
        self.ring = RingLightController()
        self.speaker = SpeakerController()
        self.login_screen = None
        self.game = None
        self.running = True
        self.data = Data()

    def run(self):
        Copyright.copyright()
        try:
            while self.running:
                self.login_screen = LoginScreen()
                self.login_screen.run()

                if self.login_screen.menu_screen.game_started:
                    try:
                        self.speaker.play_start()
                        self.ring.start_game()
                        self.speaker.start_background()

                        self.game = BackgammonGUI()
                        winner_player = self.game.run()

                        self.speaker.play_end()
                        self.ring.end_game()

                        WinningScreen(self.game.screen, winner_player).draw()
                        self.login_screen.menu_screen.game_started = False

                        winner, loser = self.data.match_usernames(winner_player, self.login_screen.users.values())
                        self.data.structure_data()
                        self.data.update_users_stats(winner, loser)
                    except Exception as e:
                        print("An error occurred during gameplay:", e)
                        self.running = False

        except KeyboardInterrupt:
            print("KeyboardInterrupt: Game stopped by user.")
        finally:
            pygame.quit()
            sys.exit()


if __name__ == "__main__":
    game_manager = GameManager()
    game_manager.run()
