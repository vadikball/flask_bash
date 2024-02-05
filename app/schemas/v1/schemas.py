"""API Schemas"""

from pydantic import BaseModel, Field


class OkStatus(BaseModel):
    status: str = "ok"


class PathBase(BaseModel):
    path: str


class RmIn(BaseModel):
    object_name: str


class ChmodIn(RmIn):
    mask: int = Field(ge=0, le=777)


class ChownIn(RmIn):
    owner: str


class TouchIn(PathBase):
    file_name: str


class MkdirIn(PathBase):
    dir_name: str


class LsOut(BaseModel):
    dir_items: list[str]


class ClientError(BaseModel):
    code: int = 400
    name: str
    description: str
