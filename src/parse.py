import json
from typing import Any
from pydantic import BaseModel


class ValidatorError(Exception):
    """Raised when input JSON cannot be validated."""
    pass


class Parameter(BaseModel):
    """Represents a function parameter definition."""
    type: str


class ReturnType(BaseModel):
    """Represents the return type of a function."""
    type: str


class Prompt(BaseModel):
    """Represents a user prompt."""
    prompt: str


class Definition(BaseModel):
    """Represents a function definition."""
    name: str
    description: str
    parameters: dict[str, Parameter]
    returns: ReturnType


class JsonLoader:
    """Loads and validates JSON input files."""
    def __init__(self, file_path: str):
        self.file = file_path
        self.data = self.load()

    def load(self) -> list[dict[str, Any]]:
        """Load the JSON file and ensure that it contains a JSON array."""
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
        """Validate and return all prompts from the input file."""
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
        """Validate and return all function definitions from the input file."""
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
