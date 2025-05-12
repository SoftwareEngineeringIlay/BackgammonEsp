# ── Data.py (replaces the old text‑file version) ─────────────────────────
from __future__ import annotations
from typing import Dict, Tuple
from StatsRepository import StatsRepository


class Data:
    """
    API stays exactly the same; storage is now MongoDB.
    """

    def __init__(self) -> None:
        self.repo = StatsRepository()
        self.data: Dict[str, Tuple[int, int]] = {}

    # ---------- keep legacy signatures ----------
    def structure_data(self) -> None:
        """Populate self.data from DB; identical call‑site semantics."""
        self.data = self.repo.get_all()

    def print_data(self) -> None:
        for username, (wins, loses) in self.data.items():
            total = wins + loses
            ratio = wins / total if total else 0
            print(
                f"{username} has {wins} wins, {loses} loses "
                f"and the winning ratio is {ratio:.2%}"
            )

    def increment_stats(self, username: str, win: int, lose: int) -> None:
        self.repo.inc(username, win, lose)
        # keep the in‑memory mirror up‑to‑date
        w, l = self.data.get(username, (0, 0))
        self.data[username] = (w + win, l + lose)

    def update_users_stats(self, winner: str, loser: str) -> None:
        self.increment_stats(winner, 1, 0)
        self.increment_stats(loser, 0, 1)

    @staticmethod
    def match_usernames(
        winner_flag: int, user_values
    ) -> Tuple[str, str]:
        """
        winner_flag:  1  -> first user won
                     -1  -> second user won
        """
        users = list(user_values)
        winner = users[0] if winner_flag == 1 else users[1]
        loser  = users[1] if winner_flag == 1 else users[0]
        return winner, loser
