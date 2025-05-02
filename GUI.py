import pygame
from BackgammonGame import Backgammon

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 700


class BackgammonGUI:
    def __init__(self):
        super().__init__()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Backgammon Game")
        self.clock = pygame.time.Clock()
        self.backgammon = Backgammon()
        self.running = True
        self.roll_dice_button = pygame.Rect(350, 340, 200, 100)  # Rect(left, top, width, height)
        self.selected_checker = None
        self.rolled_this_turn = False
        self.message_box = ["", "", "", "", ""]  # List to store last 5 messages

    def reset_selected_positions(self):
        self.selected_checker = None
        self.rolled_this_turn = False

    def draw_players_information(self):
        # Draw player information box
        pygame.draw.rect(self.screen, (200, 200, 200), (10, 10, 200, 60))  # Light gray box
        font = pygame.font.Font(None, 24)
        player1_text = font.render("Player 1: Black", True, (0, 0, 255 if self.backgammon.current_player == 1 else 0))
        player2_text = font.render("Player 2: Red", True, (0, 0, 255 if self.backgammon.current_player == -1 else 0))

        self.screen.blit(player1_text, (20, 20))
        self.screen.blit(player2_text, (20, 45))

    def draw_checkers_and_cells(self):
        cell_width = 60  # cell width
        gap = 10  # Space between cells

        for i in range(24):
            x = (i % 12) * (cell_width + gap) + 40 if i < 12 else (23 - i) * (cell_width + gap) + 40
            y = 600 if i < 12 else 100
            pygame.draw.rect(self.screen, (169, 169, 169), (x, y, cell_width, 80))  # light gray rectangle
            checker_count = abs(self.backgammon.board[i])
            # draw the checkers
            for j in range(min(checker_count, 5)):
                color = (255, 0, 0) if self.backgammon.board[i] < 0 else (0, 0, 0)
                pygame.draw.ellipse(self.screen, color, (x + 10, y + (4 - j) * 16, cell_width - 20, 16))  # Adjust y coordinate

            # Draw the number in the cell
            font = pygame.font.Font(None, 24)
            number_text = font.render(str(i), True, (0, 0, 0))
            number_rect = number_text.get_rect(center=(x + cell_width // 2, y + 40))
            self.screen.blit(number_text, number_rect)

    def draw_roll_dice_button(self):
        # Draw a grey "Roll Dice" button
        pygame.draw.rect(self.screen, (169, 169, 169), self.roll_dice_button)
        font = pygame.font.Font(None, 36)
        text = font.render("Roll Dice", True, (0, 0, 0))
        text_rect = text.get_rect(center=self.roll_dice_button.center)
        self.screen.blit(text, text_rect)

    def draw_eaten_checkers(self, value, color, y):
        if value:   # number of eaten players of each player
            ellipse_rect = pygame.draw.ellipse(self.screen, color, (SCREEN_WIDTH // 2 - 20, 390 + y, 40, 16))

            font = pygame.font.Font(None, 18)
            number_text = font.render(str(value), True, (255, 255, 255))
            number_rect = number_text.get_rect(center=ellipse_rect.center)
            self.screen.blit(number_text, number_rect)

    def draw_eaten_checkers_score(self):
        # Print just if there is an eaten checker
        if self.backgammon.has_eaten_checkers():
            # Draw eaten checkers score box
            pygame.draw.rect(self.screen, (200, 200, 200), (510, 10, 200, 60))  # Light gray box
            font = pygame.font.Font(None, 22)
            description_text = font.render("Eaten checkers:", True, (0, 0, 0))
            player1_text = font.render(f"Player 1 (Black): {self.backgammon.eaten_checkers[1]}", True, (0, 0, 0))
            player2_text = font.render(f"Player 2: (Red): {self.backgammon.eaten_checkers[-1]}", True, (0, 0, 0))
            self.screen.blit(description_text, (520, 15))
            self.screen.blit(player1_text, (520, 32.5))
            self.screen.blit(player2_text, (520, 50))

    def draw_finished_checkers_score(self):
        # Print just if a checker is finished
        if any(value != 0 for value in self.backgammon.finished_checkers.values()):
            # Draw finished checkers score box
            pygame.draw.rect(self.screen, (200, 200, 200), (260, 10, 200, 60))  # Light gray box
            font = pygame.font.Font(None, 22)
            description_text = font.render("Finished checkers:", True, (0, 0, 0))
            player1_text = font.render(f"Player 1 (Black): {self.backgammon.finished_checkers[1]}", True, (0, 0, 0))
            player2_text = font.render(f"Player 2: (Red): {self.backgammon.finished_checkers[-1]}", True, (0, 0, 0))
            self.screen.blit(description_text, (270, 20))
            self.screen.blit(player1_text, (270, 35))
            self.screen.blit(player2_text, (270, 50))

    def draw_dices(self):
        # Draw eaten checkers score box
        pygame.draw.rect(self.screen, (200, 200, 200), (760, 10, 70, 60))  # Light gray box
        font = pygame.font.Font(None, 22)
        description_text = font.render("Dices", True, (0, 0, 0))

        color_mapping = {
            2: ((0, 0, 0), (0, 0, 0)),
            1: ((128, 128, 128), (0, 0, 0)),
            0: ((128, 128, 128), (128, 128, 128))
        }

        first_dice_color, second_dice_color = color_mapping.get(self.backgammon.moves_remaining, ((0, 0, 0), (0, 0, 0)))  # (0, 0, 0) is default values

        first_dice_number = font.render(f"{self.backgammon.dice[0]}", True, first_dice_color)
        second_dice_number = font.render(f"{self.backgammon.dice[1]}", True, second_dice_color)

        self.screen.blit(first_dice_number, (778.5, 45))
        self.screen.blit(second_dice_number, (803.5, 45))
        self.screen.blit(description_text, (773, 20))

    def draw_message_box(self):
        # Draw the message box
        pygame.draw.rect(self.screen, (200, 200, 200), (20, 200, 300, 110))  # Light gray box

    def render_and_blit_message(self, message, position):
        font = pygame.font.Font(None, 18)
        text = font.render(message, True, (0, 0, 0))
        text_rect = text.get_rect(topleft=position)
        self.screen.blit(text, text_rect)

    def draw_message(self, message):
        # Add the new message to the message box
        self.message_box.pop(0)  # Remove the oldest message
        self.message_box.append(message)  # Add the new message to the end

        # Render and blit each message in the message box
        for i, msg in enumerate(self.message_box):
            self.render_and_blit_message(msg, (30, 210 + i * 20))

    def draw_messages(self):
        # Render and blit each message in the message box
        for i, msg in enumerate(self.message_box):
            self.render_and_blit_message(msg, (30, 210 + i * 20))

    def draw_board(self):
        # Draw the backgammon board on the screen
        middle_border_width = 20  # width of middle border

        self.screen.fill((130, 210, 255))  # background color

        self.draw_players_information()

        self.draw_checkers_and_cells()

        # Draw a wider middle border
        pygame.draw.rect(self.screen, (75, 75, 75), (SCREEN_WIDTH // 2 - middle_border_width // 2, 100, middle_border_width, 580))  # (surface, color, (left, top, width, height))

        self.draw_roll_dice_button()

        # Draw for player 1 (Black)
        self.draw_eaten_checkers(self.backgammon.eaten_checkers[1], (0, 0, 0), -138)

        # Draw for player 2 (Red)
        self.draw_eaten_checkers(self.backgammon.eaten_checkers[-1], (255, 0, 0), 138)

        # Draw eaten checkers box
        self.draw_eaten_checkers_score()

        # Draw finished checkers box
        self.draw_finished_checkers_score()

        self.draw_dices()

        self.draw_message_box()
        self.draw_messages()

        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = pygame.mouse.get_pos()
                if self.roll_dice_button.collidepoint(x, y) and not self.rolled_this_turn and not self.backgammon.moves_remaining:
                    self.reset_selected_positions()  # Reset selected positions
                    self.backgammon.roll_dice()
                    self.draw_message(f"Player {1 if self.backgammon.current_player == 1 else 2}, Roll Dice: {self.backgammon.dice}")
                    self.rolled_this_turn = True
                elif self.selected_checker is None:
                    self.check_select_checker(x, y)

    def check_select_checker(self, x, y):
        # Check if the player clicks on a checker to select it for movement
        if self.backgammon.has_eaten_checkers():
            if self.backgammon.current_player == 1 and self.is_in_eaten_range(x, y, 390 - 138):
                # print("Eaten black player pressed")
                self.selected_checker = 24
            elif self.backgammon.current_player == -1 and self.is_in_eaten_range(x, y, 390 + 138):
                # print("Eaten red player pressed")
                self.selected_checker = -1

            self.play_turn()

        # Check on which cell the player clicked
        else:
            for i in range(24):
                if self.is_in_board_range(x, y, i):
                    self.selected_checker = i
                    self.play_turn()
                    break

    @staticmethod
    def is_in_eaten_range(x, y, center_y):
        x_range = range(SCREEN_WIDTH // 2 - 20, SCREEN_WIDTH // 2 + 20)
        y_range = range(center_y, center_y + 16)
        return x in x_range and y in y_range

    def is_in_board_range(self, x, y, i):
        cell_width = 60
        gap = 10
        if i < 12:
            x_range = range((i % 12) * (cell_width + gap) + gap, (i % 12) * (cell_width + gap) + cell_width + gap)
        else:
            x_range = range((23 - i) * (cell_width + gap) + gap, (23 - i) * (cell_width + gap) + cell_width + gap)
        y_range = range(600, 680) if i < 12 else range(100, 180)
        return x in x_range and y in y_range and abs(self.backgammon.board[i]) > 0 and self.backgammon.board[i] * self.backgammon.current_player > 0

    def print_eaten_checkers(self):
        # Print the current player eaten checkers amount
        if self.backgammon.has_eaten_checkers():
            player_num, color = (1, "Black") if self.backgammon.current_player == 1 else (2, "Red")
            self.draw_message(f"Player {player_num} ({color}) eaten checkers: {self.backgammon.eaten_checkers[self.backgammon.current_player]}")

    def print_finished_checkers(self):
        player_num, color = (1, "Black") if self.backgammon.current_player == 1 else (2, "Red")
        self.draw_message(f"Player {player_num} ({color}) finished checkers: {self.backgammon.finished_checkers[self.backgammon.current_player]}")

    def handle_turn_end(self):
        # Check for player win
        if self.backgammon.player_won():
            self.running = False
            return

        if self.backgammon.has_moves_remaining():
            self.reset_selected_positions()
        else:
            self.draw_message("No more moves remaining for the current player.")
            self.draw_message("Switching to the next player.")
            self.backgammon.switch_player()
            self.reset_selected_positions()

    def play_turn(self):
        # Move checkers based on the dice values and according to backgammon rules - logic
        if self.backgammon.has_moves_remaining() and self.selected_checker is not None:
            steps = self.backgammon.dice[0] if self.backgammon.moves_remaining == 2 else self.backgammon.dice[1]  # Use the match dice for the move
            start_point = self.selected_checker
            end_point = start_point - steps * self.backgammon.current_player

            # Checking if all checkers of a player at their home position
            self.backgammon.can_remove_checker()

            if self.backgammon.is_valid_move(start_point, steps):
                self.backgammon.move_checker(start_point, steps)
                self.draw_message(f"Player {1 if self.backgammon.current_player == 1 else 2}, Moved checker from point {start_point} to point {end_point}")
                self.backgammon.decrement_moves_remaining()  # Decrement the remaining moves

                self.print_eaten_checkers()
                self.handle_turn_end()

            elif self.backgammon.has_eaten_checkers():
                self.draw_message("Invalid move. You can't play with this dice.")
                self.backgammon.decrement_moves_remaining()  # Decrement the remaining moves
                self.handle_turn_end()

            # Take a checker off the board
            elif self.backgammon.can_take_off_checker(start_point, steps):
                self.backgammon.move_end_checker(start_point)
                self.draw_message(
                    f"Player {1 if self.backgammon.current_player == 1 else 2}, Taken checker from point {start_point} out of board")
                self.backgammon.decrement_moves_remaining()  # Decrement the remaining moves

                self.print_finished_checkers()
                self.handle_turn_end()

            elif not self.backgammon.can_make_move(steps):
                self.draw_message("You can't make a move.")
                self.backgammon.decrement_moves_remaining()  # Decrement the remaining moves
                self.handle_turn_end()

            else:
                self.draw_message("Invalid move. Try again.")
                self.reset_selected_positions()

    def run(self):
        try:
            while self.running:
                self.handle_events()
                self.draw_board()
                self.clock.tick(30)  # Standard frame rate -> 1000/30 mls -> 33.33 fps
            return self.backgammon.current_player  # winner

        except KeyboardInterrupt:
            self.running = False
