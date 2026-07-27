from pydantic import BaseModel
from typing import Any


class FunctionCall(BaseModel):
    name: str
    arguments: dict[str, Any]
