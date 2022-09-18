from __future__ import annotations

from app.api.rest.context import RequestContext
from app.common import responses
from app.common.errors import ServiceError
from app.common.responses import Success
from app.models.statistics import Statistics
from app.models.statistics import StatisticsInput
from app.models.statistics import StatisticsUpdate
from app.usecases import statistics
from fastapi import APIRouter
from fastapi import Depends

router = APIRouter()


@router.post("/v1/accounts/{account_id}/statistics",
             response_model=Success[Statistics])
async def create_statistics(args: StatisticsInput, ctx: RequestContext = Depends()):
    data = await statistics.create(ctx, args.account_id, args.game_mode,
                                   args.total_score, args.ranked_score,
                                   args.performance, args.play_count,
                                   args.play_time, args.accuracy, args.max_combo,
                                   args.total_hits, args.replay_views,
                                   args.xh_count, args.x_count, args.sh_count,
                                   args.s_count, args.a_count)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to create statistics")

    resp = Statistics.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/accounts/{account_id}/statistics/{game_mode}",
            response_model=Success[Statistics])
async def fetch_one_statistics(account_id: int, game_mode: int,
                               ctx: RequestContext = Depends()):
    data = await statistics.fetch_one(ctx, account_id, game_mode)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch statistics")

    resp = Statistics.from_mapping(data)
    return responses.success(resp)


@router.get("/v1/accounts/{account_id}/statistics",
            response_model=Success[list[Statistics]])
async def fetch_all_account_statistics(account_id: int,
                                       ctx: RequestContext = Depends()):
    data = await statistics.fetch_all(ctx, account_id)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to fetch statistics")

    resp = [Statistics.from_mapping(d) for d in data]
    return responses.success(resp)


@router.patch("/v1/accounts/{account_id}/statistics/{game_mode}",
              response_model=Success[Statistics])
async def partial_update_statistics(account_id: int, game_mode: int,
                                    args: StatisticsUpdate,
                                    ctx: RequestContext = Depends()):
    data = await statistics.partial_update(ctx, account_id, game_mode,
                                           total_score=args.total_score,
                                           ranked_score=args.ranked_score,
                                           performance=args.performance,
                                           play_count=args.play_count,
                                           play_time=args.play_time,
                                           accuracy=args.accuracy,
                                           max_combo=args.max_combo,
                                           total_hits=args.total_hits,
                                           replay_views=args.replay_views,
                                           xh_count=args.xh_count,
                                           x_count=args.x_count,
                                           sh_count=args.sh_count,
                                           s_count=args.s_count,
                                           a_count=args.a_count)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to update statistics")

    resp = Statistics.from_mapping(data)
    return responses.success(resp)


@router.delete("/v1/accounts/{account_id}/statistics/{game_mode}",
               response_model=Success[Statistics])
async def delete_statistics(account_id: int, game_mode: int,
                            ctx: RequestContext = Depends()):
    data = await statistics.delete(ctx, account_id, game_mode)
    if isinstance(data, ServiceError):
        return responses.failure(data, "Failed to delete statistics")

    resp = Statistics.from_mapping(data)
    return responses.success(resp)
