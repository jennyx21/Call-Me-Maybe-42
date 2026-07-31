from llm_sdk import Small_LLM_Model
from src.parse import JsonLoader, ValidatorError
from src.funktiocall import FunctionCall
from src.generator import generator
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parent.parent

# prompts = str(ROOT / "data" / "input" / "function_calling_tests.json")
# definitions = str(ROOT / "data" / "input" / "functions_definition.json")

prompts = str(ROOT / "moulinette" / "data" / "input" / "function_calling_tests.json")
definitions = str(ROOT / "moulinette" / "data" / "input" / "functions_definition.json")


def main():
    llm = Small_LLM_Model()

    try:
        prompt = JsonLoader(prompts).promt_validator()
        definition = JsonLoader(definitions).definitons_validator()
    except ValidatorError as e:
        print(e)
        return
    results = []
    for p in prompt:
        name, parameter = generator(definition, llm, p)
        output_raw = {"name": name,
                      "parameters": parameter}
        funktion = FunctionCall(name=output_raw["name"],
                                arguments=output_raw["parameters"])
        name = funktion.name
        arguments = funktion.arguments

        results.append({"prompt": p.prompt, "name": name,
                        "parameters": arguments})

    output_path = ROOT / "moulinette" / "data" / "output" / "function_calling_result.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
