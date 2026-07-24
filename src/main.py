from llm_sdk import Small_LLM_Model
from parse import JsonLoader, Prompt, Definitions
import json

prompts = "/goinfre/jtruckse/Call-Me-Maybe/data/input/function_calling_tests.json"
definitions = "/goinfre/jtruckse/Call-Me-Maybe/data/input/functions_definition.json"


def main():
    prompt: list = JsonLoader(prompts, "prompt")
    definition: list = JsonLoader(definitions, "definitions")
    print(prompt)
    print(definitions)

# def main():
#     llm = Small_LLM_Model()
#     promt = "welche funktion rechent 1 + 1? die antwort ist"
#     ausgabe = []
#     encodet = llm.encode(promt)
#     logit = encodet[0].tolist()
#     # logits = llm.get_logits_from_input_ids(encodet[0].tolist())
#     i = 0
#     while (i < 50):
#         logits = llm.get_logits_from_input_ids(logit)
#         next_token = logits.index(max(logits))
#         logit.append(next_token)
#         i += 1
#     # print(logits)
#     print(llm.get_path_to_tokenizer_file())
#     with open(llm.get_path_to_tokenizer_file(), encoding="utf=8") as f:
#         print(f)
#         tokenizer = json.load(f)
#         print(tokenizer)
#     print(llm.get_path_to_vocab_file())
#     # with open(llm.get_path_to_vocab_file()) as f:
#     #     print(f)
#     #     vocab = json.load(f)
#     #     print(vocab)
#     print(llm.get_path_to_merges_file())
#     print(llm.decode(logit))
#     decodet = llm.decode(encodet)
#     print(decodet)


if __name__ == "__main__":
    main()