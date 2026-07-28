from src.parse import Definition
import json
from llm_sdk import Small_LLM_Model


def id_to_token(llm: Small_LLM_Model):
    id_to_token_var = {}
    with open(llm.get_path_to_vocab_file()) as f:
        vocab = json.load(f)
    for token, id in vocab.items():
        id_to_token_var[id] = token
    return id_to_token_var


def allow_ids(definition: list[Definition], llm: Small_LLM_Model):
    liste = ["{", "}", "[", "]", "function", "name", "arguments", ":", '"']
    allowed = []
    for defi in definition:
        name = llm.encode(defi.name)
        allowed.extend(name[0].tolist())

    for element in liste:
        elem = llm.encode(element)
        allowed.extend(elem[0].tolist())

    return allowed


def generator(text: str, prompt: str, a_ids: list[str], llm: Small_LLM_Model):
    p = llm.encode(text)
    token = p[0].tolist()

    logits = []
    for _ in range(20):
        logit = llm.get_logits_from_input_ids(token)
        for tokenid, value in enumerate(logit):
            # print(tokenid)
            # print(value)
            if tokenid not in a_ids:
                logit[tokenid] = float("-inf")

        next_token = logit.index(max(logit))
        logits.append(next_token)
        token.append(next_token)

        # print(llm.decode(p))
        print(llm.decode(next_token), end="")
        # print(llm.decode(logits))
    print()
    return
