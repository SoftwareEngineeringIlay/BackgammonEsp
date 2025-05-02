STATS_FILE_PATH = 'stats_file.txt'


class Read:
    @staticmethod
    def read():
        try:
            with open(STATS_FILE_PATH, 'r') as f:
                return f.read()
        except FileNotFoundError as e:
            print(e.strerror + ". Creating file.")
            with open(STATS_FILE_PATH, 'w'):
                pass
            return Read.read()


class Write:
    @staticmethod
    def write(data):
        with open(STATS_FILE_PATH, 'w') as f:
            for username, (wins, loses) in data.items():
                f.write(f'{username}:({wins},{loses})\n')


class Data:
    # Line = {username: (wins, loses), username2: (wins, loses)}
    def __init__(self):
        self.file_content = None
        self.data = {}

    def structure_data(self):
        self.file_content = Read().read()
        for line in self.file_content.splitlines():
            username, stats = line.strip().split(':')
            wins, loses = map(int, stats.strip()[1:-1].split(','))
            self.data[username] = (wins, loses)

    def print_data(self):
        for username, (wins, loses) in self.data.items():
            ratio = wins / (wins + loses)
            print(f'{username} has {wins} wins, {loses} loses and the winning ratio is {ratio}')

    def increment_stats(self, username, win, lose):
        if username in self.data:
            wins, loses = self.data[username]
            self.data[username] = (int(wins) + win, int(loses) + lose)
        else:
            self.data[username] = (win, lose)

    def update_users_stats(self, winner, loser):
        self.increment_stats(winner, 1, 0)
        self.increment_stats(loser, 0, 1)
        Write.write(self.data)  # save the changes.

    @staticmethod
    def match_usernames(winner, user_values):
        users_values = list(user_values)
        winner_username = users_values[0] if winner == 1 else users_values[1]
        loser_username = users_values[0] if winner == -1 else users_values[1]
        return winner_username, loser_username
