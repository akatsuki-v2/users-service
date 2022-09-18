from __future__ import annotations

from typing import Any
from typing import Mapping

from app.common.context import Context


class Statistics:
    READ_PARAMS = """\
        account_id, game_mode, total_score, ranked_score, performance,
        play_count, play_time, accuracy, max_combo, total_hits, replay_views,
        xh_count, x_count, sh_count, s_count, a_count
    """

    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def create(self,
                     account_id: int,
                     game_mode: int,
                     total_score: int,
                     ranked_score: int,
                     performance: int,
                     play_count: int,
                     play_time: int,
                     accuracy: float,
                     max_combo: int,
                     total_hits: int,
                     replay_views: int,
                     xh_count: int,
                     x_count: int,
                     sh_count: int,
                     s_count: int,
                     a_count: int) -> Mapping[str, Any]:
        query = f"""\
            INSERT INTO statistics (account_id, game_mode, total_score,
                                    ranked_score, performance, play_count,
                                    play_time, accuracy, max_combo,
                                    total_hits, replay_views, xh_count,
                                    x_count, sh_count, s_count, a_count)
                 VALUES (:account_id, :game_mode, :total_score, :ranked_score,
                         :performance, :play_count, :play_time, :accuracy,
                         :max_combo, :total_hits, :replay_views, :xh_count,
                         :x_count, :sh_count, :s_count, :a_count)
              RETURNING {self.READ_PARAMS}
        """
        params = {
            "account_id": account_id,
            "game_mode": game_mode,
            "total_score": total_score,
            "ranked_score": ranked_score,
            "performance": performance,
            "play_count": play_count,
            "play_time": play_time,
            "accuracy": accuracy,
            "max_combo": max_combo,
            "total_hits": total_hits,
            "replay_views": replay_views,
            "xh_count": xh_count,
            "x_count": x_count,
            "sh_count": sh_count,
            "s_count": s_count,
            "a_count": a_count,
        }
        statistics = await self.ctx.db.fetch_one(query, params)
        assert statistics is not None
        return statistics

    async def fetch_one(self, account_id: int, game_mode: int) -> Mapping[str, Any] | None:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM statistics
             WHERE account_id = :account_id
               AND game_mode = :game_mode
        """
        params = {
            "account_id": account_id,
            "game_mode": game_mode,
        }
        statistics = await self.ctx.db.fetch_one(query, params)
        return statistics

    async def fetch_all(self, account_id: int | None = None,
                        game_mode: int | None = None) -> list[Mapping[str, Any]]:
        query = f"""\
            SELECT {self.READ_PARAMS}
              FROM statistics
             WHERE COALESCE(:account_id, account_id),
                   COALESCE(:game_mode, game_mode)
        """
        params = {
            "account_id": account_id,
            "game_mode": game_mode,
        }
        statistics = await self.ctx.db.fetch_all(query, params)
        return statistics

    async def partial_update(self, account_id: int, game_mode: int,
                             **updates: Any) -> Mapping[str, Any] | None:
        if not updates:
            return None

        query = f"""\
            UPDATE statistics
               SET {", ".join(f"{k} = :{k}" for k in updates)},
                   updated_at = CURRENT_TIMESTAMP
             WHERE account_id = :account_id
               AND game_mode = :game_mode
         RETURNING {self.READ_PARAMS}
        """
        params = {
            "account_id": account_id,
            "game_mode": game_mode,
            **updates,
        }
        statistics = await self.ctx.db.fetch_one(query, params)
        return statistics

    async def delete(self, account_id: int, game_mode: int) -> Mapping[str, Any] | None:
        query = f"""\
            UPDATE statistics
               SET status = 'deleted',
                   updated_at = CURRENT_TIMESTAMP,
             WHERE account_id = :account_id
               AND game_mode = :game_mode
         RETURNING {self.READ_PARAMS}
        """
        params = {
            "account_id": account_id,
            "game_mode": game_mode,
        }
        statistics = await self.ctx.db.fetch_one(query, params)
        return statistics