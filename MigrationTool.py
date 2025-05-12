from StatsRepository import StatsRepository

def migrate_textfile(path: str = "stats_file.txt") -> None:
    repo = StatsRepository()
    with open(path, "r") as f:
        for line in f:
            if not line.strip():
                continue  # skip completely empty lines

            username, stats = line.strip().split(":")
            wins, loses = map(int, stats.strip()[1:-1].split(","))
            repo.increment(username, wins, loses)

if __name__ == "__main__":
    migrate_textfile()
    print("Stats migrated to MongoDB")
