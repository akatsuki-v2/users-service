from app.models import BaseModel


# TODO: enum for action?


class Presence(BaseModel):
    game_mode: int
    country_code: str
    privileges: int
    latitude: float
    longitude: float
    action: int
    info_text: str
    map_md5: str
    map_id: int
    mods: int


class PresenceInput(BaseModel):
    game_mode: int
    country_code: str
    privileges: int
    latitude: float
    longitude: float
    action: int
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
    action: int | None
    info_text: str | None
    map_md5: str | None
    map_id: int | None
    mods: int | None
