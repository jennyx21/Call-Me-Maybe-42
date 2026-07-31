from pydantic import BaseModel


class FunctionCall(BaseModel):
    name: str
    arguments: dict[str, str]
