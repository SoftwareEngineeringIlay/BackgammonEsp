# ── StatsRepository.py ────────────────────────────────────────────────────
from __future__ import annotations
from typing import Dict, Tuple
from pymongo import MongoClient
from pymongo.collection import Collection


class StatsRepository:
    """
    Unit‑tested gateway for MongoDB.
    The username itself is saved as _id, so no extra field is added.
      { _id: "<username>", wins: 3, loses: 1 }
    """

    def __init__(
        self,
        uri: str = "mongodb://localhost:27017",
        db_name: str = "backgammon",
        coll_name: str = "stats",
    ) -> None:
        self._col: Collection = MongoClient(uri)[db_name][coll_name]

    # ---------- CRUD ----------
    def get_all(self) -> Dict[str, Tuple[int, int]]:
        return {
            d["_id"]: (d["wins"], d["loses"])
            for d in self._col.find(
                {}, projection={"_id": 1, "wins": 1, "loses": 1}
            )
        }

    def inc(self, user: str, win: int, lose: int) -> None:
        self._col.update_one(
            {"_id": user},
            {"$inc": {"wins": win, "loses": lose}},
            upsert=True,
        )
