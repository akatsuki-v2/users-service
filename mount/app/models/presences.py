from enum import IntEnum
from uuid import UUID

from app.models import BaseModel


class Action(IntEnum):
    Idle = 0
    Afk = 1
    Playing = 2
    Editing = 3
    Modding = 4
    Multiplayer = 5
    Watching = 6
    Unknown = 7
    Testing = 8
    Submitting = 9
    Paused = 10
    Lobby = 11
    Multiplaying = 12
    OsuDirect = 13


class Presence(BaseModel):
    session_id: UUID
    game_mode: int
    country_code: str
    privileges: int
    latitude: float
    longitude: float
    action: Action
    info_text: str
    map_md5: str
    map_id: int
    mods: int


class PresenceInput(BaseModel):
    session_id: UUID
    game_mode: int
    country_code: str
    privileges: int
    latitude: float
    longitude: float
    action: Action
    info_text: str
    map_md5: str
    map_id: int
    mods: int


class PresenceUpdate(BaseModel):
    game_mode: int | None
    country_code: str | None
    privileges: int | None
    latitude: float | None
    longitude: float | None
    action: Action | None
    info_text: str | None
    map_md5: str | None
    map_id: int | None
    mods: int | None
