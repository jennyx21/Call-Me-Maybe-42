from src.parse import Definition
import json
from llm_sdk import Small_LLM_Model
from enum import Enum


def generator(text: str, prompt: str, a_ids: list[str], llm: Small_LLM_Model):
    p = llm.encode(text)
    token = p[0].tolist()
    generated = []

    logits = []
    for _ in range(20):
        logit = llm.get_logits_from_input_ids(token)
        for tokenid, value in enumerate(logit):
            if tokenid not in a_ids:
                logit[tokenid] = float("-inf")

        next_token = logit.index(max(logit))
        logits.append(next_token)
        generated.append(next_token)
        token.append(next_token)

        print(llm.decode(next_token), end="")

    print()
    return llm.decode(generated)
