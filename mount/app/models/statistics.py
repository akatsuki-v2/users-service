from datetime import datetime

from . import BaseModel
from . import Status


class Statistics(BaseModel):
    account_id: int
    game_mode: int
    total_score: int
    ranked_score: int
    performance: int
    play_count: int
    play_time: int
    accuracy: float
    max_combo: int
    total_hits: int
    replay_views: int
    xh_count: int
    x_count: int
    sh_count: int
    s_count: int
    a_count: int

    status: Status
    created_at: datetime
    updated_at: datetime


class StatisticsInput(BaseModel):
    game_mode: int
    total_score: int
    ranked_score: int
    performance: int
    play_count: int
    play_time: int
    accuracy: float
    max_combo: int
    total_hits: int
    replay_views: int
    xh_count: int
    x_count: int
    sh_count: int
    s_count: int
    a_count: int


class StatisticsUpdate(BaseModel):
    total_score: int | None
    ranked_score: int | None
    performance: int | None
    play_count: int | None
    play_time: int | None
    accuracy: float | None
    max_combo: int | None
    total_hits: int | None
    replay_views: int | None
    xh_count: int | None
    x_count: int | None
    sh_count: int | None
    s_count: int | None
    a_count: int | None

    status: Status | None
