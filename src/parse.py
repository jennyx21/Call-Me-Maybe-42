import json
from pydantic import BaseModel


class ValidatorError(Exception):
    pass


class Parameter(BaseModel):
    type: str


class ReturnType(BaseModel):
    type: str


class Prompt(BaseModel):
    prompt: str


class Definition(BaseModel):
    name: str
    description: str
    parameters: dict[str, Parameter]
    returns: ReturnType


class JsonLoader:
    def __init__(self, file_path: str):
        self.file = file_path
        self.data = self.load()

    def load(self) -> list[str]:
        try:
            with open(self.file) as f:
                daten = json.load(f)
                if not isinstance(daten, list):
                    raise ValidatorError("excpected JSON array")
                return daten
        except FileNotFoundError as e:
            raise ValidatorError(f"file could not be found: {e}")
        except json.JSONDecodeError as e:
            raise ValidatorError(f"not a correct Json format: {e}")

    def promt_validator(self) -> list[Prompt]:
        prompts: list[Prompt] = []
        if len(self.data) == 0:
            raise ValidatorError("no arguments in file")
        for item in self.data:
            try:
                promt = Prompt(**item)
                prompts.append(promt)
            except Exception as e:
                raise ValidatorError(f"couldn't validate prompts: {e}")

        return prompts

    def definitons_validator(self) -> list[Definition]:
        definitions: list[Definition] = []
        if len(self.data) == 0:
            raise ValidatorError("no data in definitons file")
        for item in self.data:
            try:
                definition = Definition(**item)
                definitions.append(definition)
            except Exception as e:
                raise ValidatorError(f"couldn't validate definitions: {e}")
        return definitions
