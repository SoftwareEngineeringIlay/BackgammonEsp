import sys
import pygame
import time
from Files import Data

BASE_PATH = 'C:\\Users\\Magshimim\\PycharmProjects\\BackgammonProject\\img\\'
SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700
WHITE = (255, 255, 255)
RED = (200, 30, 50)


class BackButton:
    RADIUS = 10
    DEBOUNCE_MS = 150

    def __init__(self, screen):
        self.screen = screen
        self.center = (SCREEN_WIDTH - self.RADIUS - 10, self.RADIUS + 10)
        self.rect = pygame.Rect(self.center[0] - self.RADIUS,
                                self.center[1] - self.RADIUS,
                                self.RADIUS * 2, self.RADIUS * 2)
        self._last_click = 0.0

    def draw(self):
        pygame.draw.circle(self.screen, RED, self.center, self.RADIUS)
        arm = self.RADIUS // 2
        pygame.draw.line(self.screen, WHITE,
                         (self.center[0] - arm, self.center[1] - arm),
                         (self.center[0] + arm, self.center[1] + arm), 3)
        pygame.draw.line(self.screen, WHITE,
                         (self.center[0] - arm, self.center[1] + arm),
                         (self.center[0] + arm, self.center[1] - arm), 3)

    def is_clicked(self, event):
        if event.type != pygame.MOUSEBUTTONDOWN or not self.rect.collidepoint(event.pos):
            return False
        now = time.time() * 1000
        if now - self._last_click < self.DEBOUNCE_MS:
            return False            # too soon → treat as same click
        self._last_click = now
        return True


class Screen:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.back_button = BackButton(screen)

    def draw(self):
        pass


class ImageLoader:
    @staticmethod
    def load_image(file_path):
        try:
            return pygame.image.load(file_path)
        except pygame.error as e:
            print('Unable to load image:', file_path)
            raise SystemExit(e)


class Button:
    def __init__(self, screen, text, position, width=300, height=100):
        self.screen = screen
        self.text = text
        self.position = position
        self.width = width
        self.height = height
        self.rect = pygame.Rect((SCREEN_WIDTH - width) // 2,
                                position, width, height)

    def draw(self):
        pygame.draw.rect(self.screen, WHITE, self.rect, 2)
        font = pygame.font.Font(None, 36)
        txt = font.render(self.text, True, WHITE)
        self.screen.blit(txt, (self.rect.x + (self.rect.width - txt.get_width()) // 2,
                               self.rect.y + (self.rect.height - txt.get_height()) // 2))

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)


class WinningScreen(Screen):
    def __init__(self, screen, winner):
        super().__init__(screen)
        self.loader = ImageLoader()
        self.winner = winner

    def draw(self):
        path = f'{BASE_PATH}Player_{self.winner}_won.png'
        pygame.display.set_caption(f'Player {1 if self.winner == 1 else 2} won')
        img = self.loader.load_image(path)
        img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(img, (0, 0))
        self.back_button.draw()
        pygame.display.flip()
        pygame.time.delay(3000)


class InstructionScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.running = True

    def draw(self):
        img = ImageLoader.load_image(f'{BASE_PATH}instructions.png')
        img = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(img, (0, 0))
        self.back_button.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT or self.back_button.is_clicked(e):
                    self.running = False
            self.draw()


class ScoreBoardScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        self.running = True

    def draw_scoreboard(self):
        MainMenuScreen.draw_message(self.screen, 'SCORE BOARD', 72,
                                    (SCREEN_WIDTH // 2, 100))

    def draw(self):
        bg = ImageLoader.load_image(f'{BASE_PATH}background.png')
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(bg, (0, 0))
        self.draw_scoreboard()
        self.draw_headers()
        self.draw_players_stats()
        self.back_button.draw()
        pygame.display.flip()

    def draw_headers(self):
        font = pygame.font.Font(None, 36)
        headers = ['Username', 'Wins', 'Loses', 'Ratio']
        y = 150
        x = (SCREEN_WIDTH - (len(headers) * 150 + 3 * 20)) // 2
        for h in headers:
            txt = font.render(h, True, WHITE)
            self.screen.blit(txt, (x + 45 - (40 if h == 'Username' else 0), y))
            if h != 'Ratio':
                pygame.draw.line(self.screen, WHITE, (x + 150, y), (x + 150, y + 30))
            x += 170
        pygame.draw.line(self.screen, WHITE, (80, y + 30), (SCREEN_WIDTH - 80, y + 30))

    def draw_players_stats(self):
        data = Data()
        data.structure_data()
        font = pygame.font.Font(None, 36)
        y = 230
        for p, (w, l) in data.data.items():
            x = (SCREEN_WIDTH - (4 * 150 + 3 * 20)) // 2
            stats = [p, str(w), str(l), f'{w / (w + l) * 100:.1f}%' if w + l else '0%']
            for i, s in enumerate(stats):
                txt = font.render(s, True, WHITE)
                self.screen.blit(txt, (x + 60 - (50 if i == 0 else 0) -
                                       (15 if i == 3 else 0), y))
                if i < 3:
                    pygame.draw.line(self.screen, WHITE,
                                     (x + 150, y), (x + 150, y + 30))
                x += 170
            pygame.draw.line(self.screen, WHITE, (80, y + 30), (SCREEN_WIDTH - 80, y + 30))
            y += 40

    def run(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT or self.back_button.is_clicked(e):
                    self.running = False
            self.draw()


class MainMenuScreen(Screen):
    def __init__(self, screen):
        super().__init__(screen)
        pygame.display.set_caption('Menu')
        self.loader = ImageLoader()
        self.running = True
        self.game_started = False
        self.buttons = [Button(screen, 'START', 200),
                        Button(screen, 'INSTRUCTIONS', 350),
                        Button(screen, 'SCORE BOARD', 500)]

    def draw_background(self):
        bg = self.loader.load_image(f'{BASE_PATH}background.png')
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(bg, (0, 0))

    @staticmethod
    def draw_message(screen, text, size, pos):
        font = pygame.font.Font(None, size)
        txt = font.render(text, True, WHITE)
        screen.blit(txt, txt.get_rect(center=pos).topleft)

    def draw_backgammon(self):
        self.draw_message(self.screen, 'BACKGAMMON', 72, (SCREEN_WIDTH // 2, 100))

    def draw_buttons(self):
        for b in self.buttons:
            b.draw()

    def draw(self):
        self.draw_background()
        self.draw_backgammon()
        self.draw_buttons()
        self.back_button.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT or self.back_button.is_clicked(e):
                    self.running = False
                elif any(b.is_clicked(e) for b in self.buttons):
                    if self.buttons[0].is_clicked(e):
                        self.game_started = True
                    elif self.buttons[1].is_clicked(e):
                        InstructionScreen(self.screen).run()
                    elif self.buttons[2].is_clicked(e):
                        ScoreBoardScreen(self.screen).run()
            if self.game_started:
                break
            self.draw()
            self.clock.tick(30)


class LoginScreen:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Login')
        self.clock = pygame.time.Clock()
        self.running = True
        self.loader = ImageLoader()
        self.menu_screen = None
        self.users = {1: '', -1: ''}
        self.login_button = Button(self.screen, 'Login', 500)
        self.back_button = BackButton(self.screen)
        self.input_boxes = [pygame.Rect(300, 350, 300, 40),
                            pygame.Rect(300, 425, 300, 40)]
        self.active_box = 0
        self.font = pygame.font.Font(None, 36)

    def draw_background(self):
        bg = self.loader.load_image(f'{BASE_PATH}background.png')
        bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(bg, (0, 0))

    def draw_login(self):
        MainMenuScreen.draw_message(self.screen, 'LOGIN', 72,
                                    (SCREEN_WIDTH // 2, 100))

    def draw_input_boxes(self):
        for i, box in enumerate(self.input_boxes):
            pygame.draw.rect(self.screen, WHITE, box, 2)
            txt = self.users[1 if i == 0 else -1]
            self.screen.blit(self.font.render(txt, True, WHITE),
                             (box.x + 10, box.y + 10))

    def draw(self):
        self.draw_background()
        self.draw_login()
        self.draw_input_boxes()
        self.login_button.draw()
        self.back_button.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            for e in pygame.event.get():
                if e.type == pygame.QUIT or self.back_button.is_clicked(e):
                    pygame.quit()
                    sys.exit()
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_RETURN:
                        self.active_box = (self.active_box + 1) % 2
                    elif e.key == pygame.K_BACKSPACE:
                        k = 1 if self.active_box == 0 else -1
                        self.users[k] = self.users[k][:-1]
                    else:
                        k = 1 if self.active_box == 0 else -1
                        self.users[k] += e.unicode
                if e.type == pygame.MOUSEBUTTONDOWN:
                    if self.input_boxes[0].collidepoint(e.pos):
                        self.active_box = 0
                    elif self.input_boxes[1].collidepoint(e.pos):
                        self.active_box = 1
                    elif self.login_button.is_clicked(e):
                        self.menu_screen = MainMenuScreen(self.screen)
                        self.menu_screen.run()
            if self.menu_screen and self.menu_screen.game_started:
                break
            self.draw()
            self.clock.tick(30)
