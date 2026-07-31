from pydantic import BaseModel
from typing import Any


class FunctionCall(BaseModel):
    """Represents a generated function call."""
    name: str
    arguments: dict[str, Any]
