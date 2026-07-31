from llm_sdk import Small_LLM_Model
from src.parse import JsonLoader, ValidatorError
from src.funktiocall import FunctionCall
from src.generator import generator
from pathlib import Path
import argparse
import json


def pars_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument("--input", type=str, required=True,
                        help="path to prompt file")
    parser.add_argument("--functions_definition", type=str,
                        required=True, help="path to function definitions")
    parser.add_argument("--output", type=str, required=True,
                        help="path to output file")
    return parser.parse_args()


def main() -> None:
    llm = Small_LLM_Model()
    args = pars_args()

    try:
        prompt = JsonLoader(args.input).promt_validator()
        defi = JsonLoader(args.functions_definition).definitons_validator()
    except ValidatorError as e:
        print(e)
        return
    results = []
    for p in prompt:
        name: str = ""
        parameter: dict[str, str] = {}
        name, parameter = generator(defi, llm, p)
        funktion = FunctionCall(name=name,
                                arguments=parameter)
        name = funktion.name
        arguments = funktion.arguments

        results.append({"prompt": p.prompt, "name": name,
                        "parameters": arguments})
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()
