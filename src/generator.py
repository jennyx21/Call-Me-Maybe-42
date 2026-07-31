from src.parse import Definition, Prompt
from typing import Any
from llm_sdk import Small_LLM_Model
import json
import math
from src.llm_prompt import llm_prompt_names, llm_prompt_params
import re


SIMPLE_ESCAPES = frozenset('"\\/bfnrt')


class ParameterExtractionError(ValueError):
    """Raised when a parameter cannot be extracted under its constraints."""


def find_function_name(instruc: list[int],
                       definitions: list[Definition],
                       llm: Small_LLM_Model) -> str:
    generated = []
    i = 0
    while i < 100:
        allowed = []
        for defi in definitions:
            name = defi.name
            name_encoded = llm.encode(name)
            name_list = name_encoded[0].tolist()
            if len(name_list) > i:
                allowed.append(name_list[i])
        logit = llm.get_logits_from_input_ids(instruc)
        for tokenid, value in enumerate(logit):
            if tokenid not in allowed:
                logit[tokenid] = float("-inf")
        next_token = logit.index(max(logit))
        instruc.append(next_token)
        generated.append(next_token)
        for defi in definitions:
            if llm.decode(generated) == defi.name:
                return str(llm.decode(generated))
        i += 1
    return str(llm.decode(generated))


def generate_number_param(instruc: list[int], llm: Small_LLM_Model,
                          numbers: list[Any]) -> str:
    generated: list[int] = []

    while 1:
        allowed = []
        for element in numbers:
            allowed.extend(llm.encode(element)[0].tolist())
        allowed.append(llm.encode(",")[0].tolist())
        logit = llm.get_logits_from_input_ids(instruc)
        for tokenid, value in enumerate(logit):
            if tokenid not in allowed:
                logit[tokenid] = float("-inf")
        next_token = logit.index(max(logit))
        try:
            float(llm.decode(next_token))
        except ValueError:
            return str(llm.decode(generated))
        if llm.decode(generated) in numbers:
            return str(llm.decode(generated))

        instruc.append(next_token)
        generated.append(next_token)


def generate_integer_param(instruc: list[int], llm: Small_LLM_Model,
                           numbers: list[Any]) -> str:
    generated: list[int] = []

    while 1:
        allowed = []
        for element in numbers:
            allowed.extend(llm.encode(element)[0].tolist())
        allowed.append(llm.encode(",")[0].tolist())
        logit = llm.get_logits_from_input_ids(instruc)
        for tokenid, value in enumerate(logit):
            if tokenid not in allowed:
                logit[tokenid] = float("-inf")
        next_token = logit.index(max(logit))
        try:
            int(llm.decode(next_token))
        except ValueError:
            return str(llm.decode(generated))
        if llm.decode(generated) in numbers:
            return str(llm.decode(generated))

        instruc.append(next_token)
        generated.append(next_token)


def json_string_prefix_state(raw_value: str) -> tuple[bool, bool]:
    """Return (valid_prefix, complete) for a JSON string scalar."""
    if not raw_value.startswith('"'):
        return False, False

    state = "normal"

    for index, character in enumerate(raw_value[1:], start=1):
        if state == "normal":
            if character == '"':
                complete = index == len(raw_value) - 1
                return complete, complete
            if character == "\\":
                state = "escape"
            elif ord(character) < 32:
                return False, False
        elif state == "escape":
            if character in SIMPLE_ESCAPES:
                state = "normal"

    return True, False


def highest_valid_string_token(input_tokens: list[int],
                               generated_tokens: list[int],
                               llm: Small_LLM_Model) -> tuple[int, str, bool]:
    logits = llm.get_logits_from_input_ids(input_tokens)
    previous_raw_value = llm.decode(generated_tokens)

    for _ in range(len(logits)):
        token_id = max(range(len(logits)), key=logits.__getitem__)
        if math.isinf(logits[token_id]) and logits[token_id] < 0:
            break
        raw_value = llm.decode(generated_tokens + [token_id])
        is_valid, is_complete = json_string_prefix_state(raw_value)
        if raw_value != previous_raw_value and is_valid:
            return token_id, raw_value, is_complete

        logits[token_id] = float("-inf")

    raise ParameterExtractionError(
        "the model has no valid token for the JSON string"
    )


def generate_string_param(prompt_text: list[int], llm: Small_LLM_Model,
                          max_tokens: int = 128) -> str:
    """Generate and decode one constrained JSON string scalar."""
    if max_tokens <= 0:
        raise ParameterExtractionError("max_tokens must be greater than zero")

    generated_tokens = llm.encode('"')[0].tolist()
    if llm.decode(generated_tokens) != '"':
        raise ParameterExtractionError(
            "the tokenizer cannot encode the JSON opening quote exactly"
        )

    input_tokens = prompt_text + generated_tokens
    raw_value = '"'

    for _ in range(max_tokens):
        token_id, raw_value, is_complete = highest_valid_string_token(
            input_tokens,
            generated_tokens,
            llm,
        )
        generated_tokens.append(token_id)
        input_tokens.append(token_id)

        if is_complete:
            try:
                value = json.loads(raw_value)
            except json.JSONDecodeError as exc:
                raise ParameterExtractionError(
                    "the generated string is not valid JSON"
                ) from exc
            if not isinstance(value, str):
                raise ParameterExtractionError(
                    "the generated JSON value is not a string"
                )
            return value

    raise ParameterExtractionError(
        f"JSON string did not finish within {max_tokens} tokens"
    )


def find_parameter(llm: Small_LLM_Model,
                   definition: Definition,
                   prompt: Prompt) -> dict[str, str | float | int]:
    result_list: dict[str, str | float | int] = {}
    numbers = re.findall(r"\d+", prompt.prompt)
    parameter: str | float | int

    for param in definition.parameters:
        text_params = llm_prompt_params(definition, prompt, param, result_list)
        p_param = llm.encode(text_params)
        instruc = p_param[0].tolist()
        if definition.parameters[param].type == "number":
            res = generate_number_param(instruc, llm, numbers)
            try:
                parameter = float(res)
                numbers.remove(res)
            except Exception:
                continue
        elif definition.parameters[param].type == "integer":
            res = generate_integer_param(instruc, llm, numbers)
            try:
                parameter = int(res)
                numbers.remove(res)
            except Exception:
                continue
        elif definition.parameters[param].type == "string":
            parameter = generate_string_param(instruc, llm)
        result_list[param] = parameter

    return result_list


def generator(definitions: list[Definition], llm: Small_LLM_Model,
              prompt: Prompt) -> tuple[str, dict[str, Any]]:
    text_names = llm_prompt_names(definitions, prompt)
    final_defi: Definition
    p_name = llm.encode(text_names)
    token_name = p_name[0].tolist()
    name = find_function_name(token_name, definitions, llm)
    for defi in definitions:
        if name == defi.name:
            final_defi = defi
    params = find_parameter(llm, final_defi, prompt)
    print(params)
    return name, params
