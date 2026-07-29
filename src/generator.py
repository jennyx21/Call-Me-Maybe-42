from src.parse import Definition
from typing import Any
from llm_sdk import Small_LLM_Model
from enum import Enum
#  -> tuple[str, dict[str, Any]]

def find_function_name(instruc: list[int],
                       definitions: list[Definition],
                       llm: Small_LLM_Model):
    allowed = []
    name = []
    for defi in definitions:
        name = llm.encode(defi.name)
        name_list = name[0].tolist()
        allowed.append(name_list[1])
        allowed.append(name_list[2])
    for _ in range(2):
        logit = llm.get_logits_from_input_ids(instruc)
        for tokenid, value in enumerate(logit):
            if tokenid not in allowed:
                logit[tokenid] = float("-inf")
        next_token = logit.index(max(logit))
        instruc.append(next_token)
        print(llm.decode(next_token), end="")
    print()




def generator(text: str, definitions: list[Definition], llm: Small_LLM_Model) -> str:
    p = llm.encode(text)
    token = p[0].tolist()
    name = find_function_name(token, definitions, llm)

# def generator(text: str, prompt: str, a_ids: list[str], llm: Small_LLM_Model):
#     p = llm.encode(text) token = p[0].tolist() generated = []
#     logits = [] 
#     for _ in range(20):
#         
#         for tokenid, value in enumerate(logit):
             # print(tokenid) # print(value)
             #  if tokenid not in a_ids:
             #  logit[tokenid] = float("-inf")
             #  next_token = logit.index(max(logit))
             #  logits.append(next_token)
             #  generated.append(next_token)
             #  token.append(next_token) 
             # # print(llm.decode(p))
             #  print(llm.decode(next_token), end="") 
             # # print(llm.decode(logits)) print()
             # return llm.decode(generated)