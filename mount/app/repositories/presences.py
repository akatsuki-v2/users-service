from __future__ import annotations

from datetime import datetime
from typing import Any
from typing import Literal
from typing import Mapping
from uuid import UUID

from app.common import json
from app.common.context import Context


def create_presence_key(session_id: UUID | Literal['*']) -> str:
    return f"users:presences:{session_id}"


class PresencesRepo:
    def __init__(self, ctx: Context) -> None:
        self.ctx = ctx

    async def create(self,
                     session_id: UUID,
                     game_mode: int,
                     account_id: int,
                     username: str,
                     country_code: int,
                     privileges: int,
                     latitude: float,
                     longitude: float,
                     action: int,  # TODO: enum
                     info_text: str,
                     map_md5: str,
                     map_id: int,
                     mods: int,
                     osu_version: str,
                     utc_offset: int,
                     display_city: bool,
                     pm_private: bool,
                     expires_at: datetime) -> Mapping[str, Any]:
        now = datetime.now()
        session = {
            "session_id": session_id,
            "game_mode": game_mode,
            "account_id": account_id,
            "username": username,
            "country_code": country_code,
            "privileges": privileges,
            "latitude": latitude,
            "longitude": longitude,
            "action": action,
            "info_text": info_text,
            "map_md5": map_md5,
            "map_id": map_id,
            "mods": mods,

            "osu_version": osu_version,
            "utc_offset": utc_offset,
            "display_city": display_city,
            "pm_private": pm_private,

            "created_at": now,
            "updated_at": now,
        }
        await self.ctx.redis.set(create_presence_key(session_id),
                                 json.dumps(session))
        await self.ctx.redis.expireat(create_presence_key(session_id),
                                      expires_at)
        return session

    async def fetch_one(self, session_id: UUID) -> Mapping[str, Any] | None:
        session = await self.ctx.redis.get(create_presence_key(session_id))
        if session is None:
            return None
        return json.loads(session)

    async def fetch_all(self,
                        game_mode: int | None = None,
                        account_id: int | None = None,
                        username: str | None = None,
                        country_code: str | None = None,
                        # privileges: int | None = None,

                        osu_version: str | None = None,
                        utc_offset: int | None = None,
                        display_city: bool | None = None,
                        pm_private: bool | None = None,
                        ) -> list[Mapping[str, Any]]:
        presence_keys = await self.ctx.redis.keys(create_presence_key("*"))
        if not presence_keys:
            return []

        raw_presences = await self.ctx.redis.mget(presence_keys)

        presences = []
        for raw_presence in raw_presences:
            presence = json.loads(raw_presence)

            if game_mode is not None and presence["game_mode"] != game_mode:
                continue

            if account_id is not None and presence["account_id"] != account_id:
                continue

            if username is not None and presence["username"] != username:
                continue

            if country_code is not None and presence["country_code"] != country_code:
                continue

            # if privileges is not None and presence["privileges"] != privileges:
            #     continue

            if osu_version is not None and presence["osu_version"] != osu_version:
                continue

            if utc_offset is not None and presence["utc_offset"] != utc_offset:
                continue

            if display_city is not None and presence["display_city"] != display_city:
                continue

            if pm_private is not None and presence["pm_private"] != pm_private:
                continue

            presences.append(presence)

        return presences

    async def partial_update(self, session_id: UUID, **kwargs: Any) -> Mapping[str, Any] | None:
        presence = await self.fetch_one(session_id)
        if presence is None:
            return None

        if not kwargs:
            return presence

        updates = {}

        new_game_mode = kwargs.get("game_mode")
        if new_game_mode is not None and new_game_mode != presence["game_mode"]:
            updates["game_mode"] = new_game_mode

        new_username = kwargs.get("username")
        if new_username is not None and new_username != presence["username"]:
            updates["username"] = new_username

        new_country_code = kwargs.get("country_code")
        if new_country_code is not None and new_country_code != presence["country_code"]:
            updates["country_code"] = new_country_code

        new_privileges = kwargs.get("privileges")
        if new_privileges is not None and new_privileges != presence["privileges"]:
            updates["privileges"] = new_privileges

        new_latitude = kwargs.get("latitude")
        if new_latitude is not None and new_latitude != presence["latitude"]:
            updates["latitude"] = new_latitude

        new_longitude = kwargs.get("longitude")
        if new_longitude is not None and new_longitude != presence["longitude"]:
            updates["longitude"] = new_longitude

        new_action = kwargs.get("action")
        if new_action is not None and new_action != presence["action"]:
            updates["action"] = new_action

        new_info_text = kwargs.get("info_text")
        if new_info_text is not None and new_info_text != presence["info_text"]:
            updates["info_text"] = new_info_text

        new_map_md5 = kwargs.get("map_md5")
        if new_map_md5 is not None and new_map_md5 != presence["map_md5"]:
            updates["map_md5"] = new_map_md5

        new_map_id = kwargs.get("map_id")
        if new_map_id is not None and new_map_id != presence["map_id"]:
            updates["map_id"] = new_map_id

        new_mods = kwargs.get("mods")
        if new_mods is not None and new_mods != presence["mods"]:
            updates["mods"] = new_mods

        new_osu_version = kwargs.get("osu_version")
        if new_osu_version is not None and new_osu_version != presence["osu_version"]:
            updates["osu_version"] = new_osu_version

        new_utc_offset = kwargs.get("utc_offset")
        if new_utc_offset is not None and new_utc_offset != presence["utc_offset"]:
            updates["utc_offset"] = new_utc_offset

        new_display_city = kwargs.get("display_city")
        if new_display_city is not None and new_display_city != presence["display_city"]:
            updates["display_city"] = new_display_city

        new_pm_private = kwargs.get("pm_private")
        if new_pm_private is not None and new_pm_private != presence["pm_private"]:
            updates["pm_private"] = new_pm_private

        if not updates:
            return presence

        presence = dict(presence)
        presence.update(updates)
        presence["updated_at"] = datetime.now()

        await self.ctx.redis.set(create_presence_key(session_id),
                                 json.dumps(presence))

        if expires_at := kwargs.get("expires_at"):  # maybe a bit weird?
            await self.ctx.redis.expireat(create_presence_key(session_id),
                                          expires_at)

        return presence

    async def delete(self, session_id: UUID) -> Mapping[str, Any] | None:
        presence_key = create_presence_key(session_id)

        session = await self.ctx.redis.get(presence_key)
        if session is None:
            return None

        await self.ctx.redis.delete(presence_key)

        return json.loads(session)
