from src.parse import Definition, Prompt
from typing import Any
from llm_sdk import Small_LLM_Model
from src.llm_prompt import llm_prompt_names, llm_prompt_params
import re


def find_function_name(instruc: list[int],
                       definitions: list[Definition],
                       llm: Small_LLM_Model):
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
                return llm.decode(generated)
        i += 1
    return llm.decode(generated)


def generate_number_param(instruc: list[int], llm: Small_LLM_Model,
                          numbers: list[Any]):
    generated = []

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
        print(llm.decode(next_token))
        try:
            float(llm.decode(next_token))
        except ValueError:
            return llm.decode(generated)
        if llm.decode(generated) in numbers:
            return llm.decode(generated)

        instruc.append(next_token)
        generated.append(next_token)


def generate_integer_param(instruc: list[int], llm: Small_LLM_Model,
                           numbers: list[Any]):
    generated = []

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
        print(llm.decode(next_token))
        try:
            int(llm.decode(next_token))
        except ValueError:
            return llm.decode(generated)
        if llm.decode(generated) in numbers:
            return llm.decode(generated)

        instruc.append(next_token)
        generated.append(next_token)


def find_parameter(instruc: list[int], llm: Small_LLM_Model,
                   definition: Definition, prompt: Prompt):
    result_list = {}
    numbers = re.findall(r"\d+", prompt.prompt)

    result = ""
    parameter = ""

    for param in definition.parameters:
        instruc_cp = instruc
        print(param)
        print(definition.parameters[param].type)
        if definition.parameters[param].type == "number":
            print("this needs to be a number")
            res = generate_number_param(instruc_cp, llm, numbers)
            try:
                parameter = float(res)
            except Exception:
                continue
        elif definition.parameters[param].type == "integer":
            print("this needs to be a number")
            res = generate_integer_param(instruc_cp, llm, numbers)
            try:
                parameter = int(res)
            except Exception:
                continue
        elif definition.parameters[param].type == "string":
            print("this needs to be a string")
            parameter = "hallo"
        result = f"'{param}': {parameter}"
        result_list[param] = parameter
        print(result)

    return result_list


def generator(definitions: list[Definition], llm: Small_LLM_Model,
              prompt: Prompt):
    text_names = llm_prompt_names(definitions, prompt)
    final_defi: Definition
    p_name = llm.encode(text_names)
    token_name = p_name[0].tolist()
    name = find_function_name(token_name, definitions, llm)
    for defi in definitions:
        if name == defi.name:
            text_params = llm_prompt_params(defi, prompt)
            p_param = llm.encode(text_params)
            token_params = p_param[0].tolist()
            final_defi = defi
    params = find_parameter(token_params, llm, final_defi, prompt)
    print(params)
    return name, params

