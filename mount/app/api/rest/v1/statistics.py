from __future__ import annotations

from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models.stats import Stats
from app.models.stats import StatsInput
from app.models.stats import StatsUpdate
from app.usecases import stats
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


@router.post("/v1/accounts/{account_id}/stats",
             response_model=Success[Stats])
async def create_stats(account_id: int, args: StatsInput, ctx: RequestContext = Depends()):
    data = await stats.create(ctx, account_id, args.game_mode,
                              args.total_score, args.ranked_score,
                              args.performance, args.play_count,
                              args.play_time, args.accuracy, args.max_combo,
                              args.total_hits, args.replay_views,
                              args.xh_count, args.x_count, args.sh_count,
                              args.s_count, args.a_count)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to create stats")

    resp = Stats.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/accounts/{account_id}/stats/{game_mode}",
            response_model=Success[Stats])
async def fetch_stats(account_id: int, game_mode: int,
                      ctx: RequestContext = Depends()):
    data = await stats.fetch_one(ctx, account_id, game_mode)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch stats")

    resp = Stats.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/accounts/{account_id}/stats",
            response_model=Success[list[Stats]])
async def fetch_all_account_stats(account_id: int,
                                  ctx: RequestContext = Depends()):
    data = await stats.fetch_all(ctx, account_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch stats")

    resp = [Stats.from_mapping(d) for d in data]
    return responses.success(resp)


@router.patch("/v1/accounts/{account_id}/stats/{game_mode}",
              response_model=Success[Stats])
async def partial_update_stats(account_id: int, game_mode: int,
                               args: StatsUpdate,
                               ctx: RequestContext = Depends()):
    data = await stats.partial_update(ctx, account_id, game_mode,
                                      **args.dict())
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to update stats")

    resp = Stats.from_mapping(data)
    return responses.success(resp)


@router.delete("/v1/accounts/{account_id}/stats/{game_mode}",
               response_model=Success[Stats])
async def delete_stats(account_id: int, game_mode: int,
                       ctx: RequestContext = Depends()):
    data = await stats.delete(ctx, account_id, game_mode)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to delete stats")

    resp = Stats.from_mapping(data)
    return responses.success(resp)
