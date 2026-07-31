from src.parse import Definition, Prompt
from typing import Any
import json


def llm_prompt_names(definitions: list[Definition], prompt: Prompt) -> str:
    instructions = """\
<|im_start|>system
You are a function calling AI.

Your task:
Chose exactly one funtion from <tools></tools>.
a function STARTS with "fn"
Example:

"name" = FN_ADD_NUMBER

<tools>
"""
    for definition in definitions:
        instructions += f"""
Function:
{definition.name}
Description:
{definition.description}
<|im_end|>\n
</tools>

User:
"""

    instructions += prompt.prompt

    return instructions


def llm_prompt_params(definition: Definition, prompt: Prompt,
                      parameter_name: str,
                      known_arguments: dict[str, Any]) -> str:
    parameter = definition.parameters[parameter_name]
    parameters = "\n".join(
        f"- {name}: {info.type}"
        for name, info in definition.parameters.items()
    )
    hints = {
        "source_string": "Return the complete input text to modify.",
        "regex": "Return the regex matching what should be replaced.",
        "replacement": "Return the replacement text or symbol.",
        "name": "Return only the person's name.",
        "s": "Return only the input string.",
    }
    hint = hints.get(parameter_name, "Return this parameter's value.")

    return (
        "<|im_start|>system\n"
        "Extract exactly one raw function argument. Do not execute the "
        "function and do not return its result.\n"
        "For strings, output one valid JSON string scalar.\n"
        "Example: Replace all numbers in \"Room 42\" with NUMBERS\n"
        "source_string -> \"Room 42\"\n"
        "regex -> \"\\\\d+\"\n"
        "replacement -> \"NUMBERS\"\n"
        "<|im_end|>\n"
        "<|im_start|>user\n"
        f"Function: {definition.name}\n"
        f"Description: {definition.description}\n"
        f"Parameters:\n{parameters}\n"
        f"User request: {prompt.prompt}\n"
        "Already extracted arguments: "
        f"{json.dumps(known_arguments, ensure_ascii=False)}\n"
        f"Extract parameter: {parameter_name}\n"
        f"Parameter type: {parameter.type}\n"
        f"Parameter meaning: {hint}\n"
        "Output only its value.\n"
        "<|im_end|>\n"
        "<|im_start|>assistant\n"
        f"{{\"{parameter_name}\": "
    )
