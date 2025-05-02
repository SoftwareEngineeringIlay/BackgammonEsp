from random import randint


class Backgammon:
    def __init__(self):
        self.board = [0] * 24  # Represents the backgammon board
        self.current_player = 1  # 1 for Player 1 (Black), -1 for Player 2 (Red)
        self.dice = [0, 0]
        self.selected_checker = None
        self.selected_end_position = None
        self.moves_remaining = 0
        self.eaten_checkers = {1: 0, -1: 0}  # Number of eaten checkers for each player
        self.can_remove_checkers = {1: 0, -1: 0}
        self.finished_checkers = {1: 0, -1: 0}
        self.init_board()

    def init_board(self):
        # Set up the initial position of checkers on the board
        self.board[0] = -2
        self.board[5] = 5
        self.board[7] = 3
        self.board[11] = -5
        self.board[12] = 5
        self.board[16] = -3
        self.board[18] = -5
        self.board[23] = 2

    def roll_dice(self):
        self.dice = [randint(1, 6), randint(1, 6)]
        self.moves_remaining = 2  # Set the number of moves for the current turn
        return self.dice

    def move_checker(self, start, steps):
        # Move a checker on the board
        if start != -1 and start != 24:  # If it's not an eaten checker
            self.board[start] -= self.current_player
        else:
            self.eaten_checkers[self.current_player] -= 1  # Decrement the eaten players
        end = start - steps * self.current_player

        # Check if there is opponent's checker at the end position
        if self.board[end] * self.current_player == -1:
            self.board[end] = 0  # Remove opponent's checker
            self.eaten_checkers[-self.current_player] += 1  # Increase opponent's checker
            self.can_remove_checkers[self.current_player] = 0  # Set the can_remove_checkers flag to 0

        self.board[end] += self.current_player

    def move_end_checker(self, start):
        # Move a checker on the board
        self.board[start] -= self.current_player
        self.finished_checkers[self.current_player] += 1

    def switch_player(self):
        # Switch the current player
        self.current_player *= -1

    def is_valid_move(self, start, steps, is_end_move=False):
        # Check for moving to off board point or a point with the player's checkers
        end = start - steps * self.current_player

        if not is_end_move and 0 <= end < 24:
            return self.board[end] * self.current_player >= -1
        elif is_end_move:
            return end < 0 or 24 <= end

    def has_moves_remaining(self):
        return self.moves_remaining > 0

    def decrement_moves_remaining(self):
        self.moves_remaining -= 1

    def has_eaten_checkers(self):
        return self.eaten_checkers[self.current_player]

    def can_remove_checker(self):
        # Checking if there is a checker of the current player that are not in his home position
        player = self.current_player
        self.can_remove_checkers[player] = 0  # reset it
        start, end = (6, 24) if player == 1 else (0, 18)

        # The sum of the current_player checkers needs to be equals to zero
        if sum(cell_count for cell_count in self.board[start:end] if cell_count * self.current_player > 0) == 0:
            self.can_remove_checkers[player] = 1

    def can_make_move(self, steps):
        # Check if the player can move a checker from any point
        for start_point in range(24):
            # Check if there is a checker at the point and is valid move
            if self.board[start_point] * self.current_player >= 1 and self.is_valid_move(start_point, steps):
                return True
        return False

    def can_take_off_checker(self, start_point, steps):
        return (not self.has_eaten_checkers() and self.can_remove_checkers[self.current_player] and
                self.is_valid_move(start_point, steps, True))

    def player_won(self):
        return self.finished_checkers[self.current_player] == 15
