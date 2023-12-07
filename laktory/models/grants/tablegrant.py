from typing import Literal
from laktory.models.basemodel import BaseModel

PRIVILEGES = [
    "ALL_PRIVILEGES",
    "SELECT",
    "MODIFY",
]


class TableGrant(BaseModel):
    principal: str
    privileges: list[Literal[tuple(PRIVILEGES)]]


t = TableGrant(principal="a", privileges=["SELECT"])
