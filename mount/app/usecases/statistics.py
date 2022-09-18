from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from app.common.context import Context
from app.common.errors import ServiceError
from app.repositories.statistics import StatisticsRepo


async def create(ctx: Context,
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
                 a_count: int) -> Mapping[str, Any] | ServiceError:
    repo = StatisticsRepo(ctx)

    statistics = await repo.fetch_one(account_id, game_mode)
    if statistics is not None:
        return ServiceError.STATISTICS_ALREADY_EXISTS

    statistics = await repo.create(account_id, game_mode, total_score,
                                   ranked_score, performance, play_count,
                                   play_time, accuracy, max_combo, total_hits,
                                   replay_views, xh_count, x_count, sh_count,
                                   s_count, a_count)

    return statistics


async def fetch_one(ctx: Context, account_id: int, game_mode: int
                    ) -> Mapping[str, Any] | ServiceError:
    repo = StatisticsRepo(ctx)

    statistics = await repo.fetch_one(account_id, game_mode)
    if statistics is None:
        return ServiceError.STATISTICS_NOT_FOUND

    return statistics


async def fetch_all(ctx: Context, account_id: int
                    ) -> list[Mapping[str, Any]] | ServiceError:
    repo = StatisticsRepo(ctx)

    statistics = await repo.fetch_all(account_id)

    return statistics


async def partial_update(ctx: Context,
                         account_id: int,
                         game_mode: int,
                         **kwargs: Any | None) -> Mapping[str, Any] | ServiceError:
    repo = StatisticsRepo(ctx)

    statistics = await repo.fetch_one(account_id, game_mode)
    if statistics is None:
        return ServiceError.STATISTICS_NOT_FOUND

    updates = {}

    new_total_score = kwargs.get("total_score")
    if new_total_score is not None and new_total_score != statistics["total_score"]:
        updates["total_score"] = new_total_score

    new_ranked_score = kwargs.get("ranked_score")
    if new_ranked_score is not None and new_ranked_score != statistics["ranked_score"]:
        updates["ranked_score"] = new_ranked_score

    new_performance = kwargs.get("performance")
    if new_performance is not None and new_performance != statistics["performance"]:
        updates["performance"] = new_performance

    new_play_count = kwargs.get("play_count")
    if new_play_count is not None and new_play_count != statistics["play_count"]:
        updates["play_count"] = new_play_count

    new_play_time = kwargs.get("play_time")
    if new_play_time is not None and new_play_time != statistics["play_time"]:
        updates["play_time"] = new_play_time

    new_accuracy = kwargs.get("accuracy")
    if new_accuracy is not None and new_accuracy != statistics["accuracy"]:
        updates["accuracy"] = new_accuracy

    new_max_combo = kwargs.get("max_combo")
    if new_max_combo is not None and new_max_combo != statistics["max_combo"]:
        updates["max_combo"] = new_max_combo

    new_total_hits = kwargs.get("total_hits")
    if new_total_hits is not None and new_total_hits != statistics["total_hits"]:
        updates["total_hits"] = new_total_hits

    new_replay_views = kwargs.get("replay_views")
    if new_replay_views is not None and new_replay_views != statistics["replay_views"]:
        updates["replay_views"] = new_replay_views

    new_xh_count = kwargs.get("xh_count")
    if new_xh_count is not None and new_xh_count != statistics["xh_count"]:
        updates["xh_count"] = new_xh_count

    new_x_count = kwargs.get("x_count")
    if new_x_count is not None and new_x_count != statistics["x_count"]:
        updates["x_count"] = new_x_count

    new_sh_count = kwargs.get("sh_count")
    if new_sh_count is not None and new_sh_count != statistics["sh_count"]:
        updates["sh_count"] = new_sh_count

    new_s_count = kwargs.get("s_count")
    if new_s_count is not None and new_s_count != statistics["s_count"]:
        updates["s_count"] = new_s_count

    new_a_count = kwargs.get("a_count")
    if new_a_count is not None and new_a_count != statistics["a_count"]:
        updates["a_count"] = new_a_count

    new_status = kwargs.get("status")
    if new_status is not None and new_status != statistics["status"]:
        updates["status"] = new_status

    if not updates:
        # return the statistics as-is
        return statistics

    statistics = await repo.partial_update(account_id, game_mode, **updates)
    assert statistics is not None
    return statistics


async def delete(ctx: Context, account_id: int, game_mode: int
                 ) -> Mapping[str, Any] | ServiceError:
    repo = StatisticsRepo(ctx)

    statistics = await repo.delete(account_id, game_mode)
    if statistics is None:
        return ServiceError.STATISTICS_NOT_FOUND

    return statistics
