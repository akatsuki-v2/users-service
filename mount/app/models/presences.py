from enum import IntEnum
from uuid import UUID

from app.models import BaseModel


class Action(IntEnum):
    IDLE = 0
    AFK = 1
    PLAYING = 2
    EDITING = 3
    MODDING = 4
    MULTIPLAYER = 5
    WATCHING = 6
    UNKNOWN = 7
    TESTING = 8
    SUBMITTING = 9
    PAUSED = 10
    LOBBY = 11
    MULTIPLAYING = 12
    OSU_DIRECT = 13


class Presence(BaseModel):
    session_id: UUID
    game_mode: int
    account_id: int
    username: str
    country_code: int  # TODO: is the number an osu-specific thing? should we use iso3166?
    privileges: int
    latitude: float
    longitude: float
    action: Action
    info_text: str
    map_md5: str
    map_id: int
    mods: int

    osu_version: str
    utc_offset: int
    display_city: bool
    pm_private: bool


class PresenceInput(BaseModel):
    session_id: UUID
    game_mode: int
    account_id: int
    username: str
    country_code: int
    privileges: int
    latitude: float
    longitude: float
    action: Action
    info_text: str
    map_md5: str
    map_id: int
    mods: int

    osu_version: str
    utc_offset: int
    display_city: bool
    pm_private: bool


class PresenceUpdate(BaseModel):
    game_mode: int | None
    username: str | None
    country_code: int | None
    privileges: int | None
    latitude: float | None
    longitude: float | None
    action: Action | None
    info_text: str | None
    map_md5: str | None
    map_id: int | None
    mods: int | None

    osu_version: str | None
    utc_offset: int | None
    display_city: bool | None
    pm_private: bool | None
