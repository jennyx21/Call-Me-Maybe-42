import json
from dataclasses import dataclass
from pydantic import BaseModel

class ValidatorError(Exception):
    pass

class Prompt(BaseModel):
    promt: str

class Definitions(BaseModel):
    name: str
    description: str
    parameter1: str
    type_p1: str
    parameter2: str
    type_p2: str
    returns: str
    type_r: str


class JsonLoader:
    def __init__(self, file_path: str, m: str):
        self.file = file_path
        self.mode = m
        self.data = self.load()

        if self.mode == "prompt":
            self.promt_validator()

        elif self.mode == "definitions":
            self.definitons_validator()

    def load(self):
        try:
            with open(self.file) as f:
                daten = json.load(f)
                return daten
        except FileNotFoundError as e:
            raise ValidatorError(f"file could not be found: {e}")
        except json.JSONDecodeError as e:
            raise ValidatorError(f"not a correct Json format {e}")

    def promt_validator(self):
        prom
        if len(self.data) == 0:
            raise ValidatorError("no arguments in file")
        for line in self.data:


    def definitons_validator(self):



# def parser():
#     with open("/goinfre/jtruckse/Call-Me-Maybe/data/input/function_calling_tests.json", encoding="utf=8") as f:
#         print(f)
#         inhalt = json.load(f)
#         print(inhalt)
#         print(type(inhalt))
#         for item in inhalt:
#             print(item['prompt'])
#             print(item)
