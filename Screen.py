import pygame
import sys
from Files import Data

BASE_PATH = 'C:\\Users\\Magshimim\\PycharmProjects\\BackgammonProject\\img\\'

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)


class Screen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()

    def draw(self):
        pass

    @staticmethod
    def handle_event():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()


class ImageLoader:
    @staticmethod
    def load_image(file_path):
        try:
            image = pygame.image.load(file_path)
        except pygame.error as e:
            print("Unable to load image:", file_path)
            raise SystemExit(e)
        return image


class Button:
    def __init__(self, screen, text, position, width=300, height=100):
        self.screen = screen
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.rect = pygame.Rect((SCREEN_WIDTH - self.width) // 2, self.position, self.width, self.height)

    def draw(self):
        pygame.draw.rect(self.screen, WHITE, self.rect, 2)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(self.text, True, WHITE)
        text_x = (SCREEN_WIDTH - text_surface.get_width()) // 2
        text_y = self.position + (self.rect.height - text_surface.get_height()) // 2
        self.screen.blit(text_surface, (text_x, text_y))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


class WinningScreen(Screen):
    def __init__(self, screen, winner):
        super().__init__(screen)
        self.image_loader = ImageLoader()
        self.winner = winner

    def draw(self):
        winner_image_path = f"{BASE_PATH}Player_{self.winner}_won.png"
        pygame.display.set_caption(f"Player {1 if self.winner == 1 else 2} won")
        winner_image = self.image_loader.load_image(winner_image_path)
        winner_image = pygame.transform.scale(winner_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        self.screen.blit(winner_image, (0, 0))
        pygame.display.flip()
        pygame.time.delay(3000)


class InstructionScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.running = True

    def draw(self):
        instructions_path = ImageLoader().load_image(f'{BASE_PATH}instructions.png')
        instructions_image = pygame.transform.scale(instructions_path, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(instructions_image, (0, 0))
        pygame.display.flip()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        while self.running:
            self.handle_event()
            self.draw()


class ScoreBoardScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.running = True

    def draw_scoreboard(self):
        MainMenuScreen.draw_message(self.screen, 'SCORE BOARD', 72, (SCREEN_WIDTH // 2, 100))

    def draw(self):
        scoreboard_path = ImageLoader().load_image(f'{BASE_PATH}background.png')
        scoreboard_image = pygame.transform.scale(scoreboard_path, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(scoreboard_image, (0, 0))
        self.draw_scoreboard()
        self.draw_headers()
        self.draw_players_stats()

        pygame.display.flip()

    def draw_headers(self):
        font = pygame.font.Font(None, 36)

        headers = ["Username", "Wins", "Loses", "Ratio"]
        y_offset = 150

        # Center the headers in the middle of the board
        x_offset = (SCREEN_WIDTH - (len(headers) * 150 + (len(headers) - 1) * 20)) // 2
        for header in headers:
            header_text = font.render(header, True, WHITE)
            self.screen.blit(header_text, (x_offset + 45 - (40 if header == "Username" else 0), y_offset))
            x_offset += 170  # Gap between the headers
            if header != "Ratio":
                pygame.draw.line(self.screen, WHITE, (x_offset - 10, y_offset), (x_offset - 10, y_offset + 30))

        # Draw the final row separator
        pygame.draw.line(self.screen, WHITE, (80, y_offset + 30), (SCREEN_WIDTH - 80, y_offset + 30))

    def draw_players_stats(self):
        data = Data()
        data.structure_data()
        font = pygame.font.Font(None, 36)

        # Draw the row separators
        y_offset = 230

        for player, (wins, loses) in data.data.items():
            # Center the stats in the middle of the board
            x_offset = (SCREEN_WIDTH - (4 * 150 + (4 - 1) * 20)) // 2  # 4 is len(headers)

            # Draw player stats
            stats = [player, str(wins), str(loses), "{:.1f}%".format(wins / (wins + loses) * 100 if (wins + loses) != 0 else 0)]
            for i, stat in enumerate(stats):
                stat_text = font.render(stat, True, WHITE)
                self.screen.blit(stat_text, (x_offset + 60 - (50 if i == 0 else 0) - (15 if i == 3 else 0), y_offset))
                x_offset += 170  # Move to the next column

                # Draw column separator except for the last column
                if i < len(stats) - 1:
                    pygame.draw.line(self.screen, WHITE, (x_offset - 10, y_offset), (x_offset - 10, y_offset + 30))

            # Draw the row separator
            pygame.draw.line(self.screen, WHITE, (80, y_offset + 30), (SCREEN_WIDTH - 80, y_offset + 30))
            y_offset += 40  # Move to the next row

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def run(self):
        while self.running:
            self.handle_event()
            self.draw()


class MainMenuScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        pygame.display.set_caption("Menu")
        self.image_loader = ImageLoader()
        self.running = True
        self.game_started = False
        self.button_width, self.button_height = 300, 100
        self.buttons = [Button(screen, 'START', 200),
                        Button(screen, 'INSTRUCTIONS', 350),
                        Button(screen, 'SCORE BOARD', 500)]  # y coordinates of the buttons

    def draw_background(self):
        menu_image_path = f"{BASE_PATH}background.png"
        menu_image = self.image_loader.load_image(menu_image_path)
        menu_image = pygame.transform.scale(menu_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(menu_image, (0, 0))

    @staticmethod
    def draw_message(screen, text, font_size, position):
        font = pygame.font.Font(None, font_size)
        text = font.render(text, True, WHITE)
        text_rect = text.get_rect(center=position)
        screen.blit(text, text_rect)

    def draw_backgammon(self):
        self.draw_message(self.screen, 'BACKGAMMON', 72, (SCREEN_WIDTH // 2, 100))

    def draw_buttons(self):
        for button in self.buttons:
            button.draw()

    def draw(self):
        self.draw_background()
        self.draw_backgammon()
        self.draw_buttons()

        pygame.display.flip()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif any(button.is_clicked(event) for button in self.buttons):
                if self.buttons[0].is_clicked(event):
                    self.game_started = True
                elif self.buttons[1].is_clicked(event):
                    InstructionScreen(self.screen).run()
                elif self.buttons[2].is_clicked(event):
                    ScoreBoardScreen(self.screen).run()

    def run(self):
        while self.running:
            self.handle_event()
            if self.game_started:
                break
            self.draw()
            self.clock.tick(30)


class LoginScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Login")
        self.running = True
        self.image_loader = ImageLoader()
        self.menu_screen = None
        self.button_width, self.button_height = 300, 100
        self.users = {1: '', -1: ''}
        self.login_button = Button(self.screen, 'Login', 500)
        self.input_boxes = [
            pygame.Rect(300, 350, 300, 40),  # Input box for Player 1
            pygame.Rect(300, 425, 300, 40),  # Input box for Player 2
        ]
        self.active_input_box = 0  # Track which box is active
        self.font = pygame.font.Font(None, 36)

    def draw_background(self):
        background_path = f"{BASE_PATH}background.png"
        background_image = self.image_loader.load_image(background_path)
        background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(background_image, (0, 0))

    def draw_login(self):
        MainMenuScreen.draw_message(self.screen, 'LOGIN', 72, (SCREEN_WIDTH // 2, 100))

    def draw_input_boxes(self):
        for i, box in enumerate(self.input_boxes):
            pygame.draw.rect(self.screen, WHITE, box, 2)
            input_text = self.users[1 if i == 0 else -1]
            self.screen.blit(
                self.font.render(input_text, True, WHITE),
                (box.x + 10, box.y + 10),
            )

    def draw(self):
        self.draw_background()
        self.draw_login()
        self.draw_input_boxes()
        self.login_button.draw()

        pygame.display.flip()

    def users_connected(self):
        return all(value != '' for value in self.users.values())

    def handle_event(self):
        for event in pygame.event.get():
            # Early exit on quit
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Switch between input boxes
                    self.active_input_box = (self.active_input_box + 1) % len(self.input_boxes)
                elif event.key == pygame.K_BACKSPACE:
                    # Remove last character from active input box
                    current_user_key = 1 if self.active_input_box == 0 else -1
                    self.users[current_user_key] = self.users[current_user_key][:-1]
                else:
                    # Add typed character to active input box
                    current_user_key = 1 if self.active_input_box == 0 else -1
                    self.users[current_user_key] += event.unicode

            # Mouse events
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Determine which box is clicked to set the active input box
                if self.input_boxes[0].collidepoint(event.pos):
                    self.active_input_box = 0
                elif self.input_boxes[1].collidepoint(event.pos):
                    self.active_input_box = 1

                # Check if the login button is clicked
                if self.login_button.is_clicked(event):
                    self.menu_screen = MainMenuScreen(self.screen)
                    self.menu_screen.run()

    def run(self):
        while self.running:
            self.handle_event()
            if self.menu_screen and self.menu_screen.game_started:
                break
            self.draw()
