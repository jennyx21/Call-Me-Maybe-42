from llm_sdk import Small_LLM_Model
from parse import JsonLoader, ValidatorError
from generator import generator, allow_ids
# from funktiocall import FunctionCall
from llm_prompt import llm_prompt


prompts = ("/goinfre/jtruckse/Call-Me-Maybe-42/data/"
           "input/function_calling_tests.json")
definitions = ("/goinfre/jtruckse/Call-Me-Maybe-42/data/"
               "input/functions_definition.json")


# def main():
#     try:
#         prompt = JsonLoader(prompts).promt_validator()
#         definition = JsonLoader(definitions).definitons_validator()
#     except ValidatorError as e:
#         print(e)
#         return
# for element in definition:
#     print(element.name)
# print(type(prompt))
# print(type(definitions))

def main():
    llm = Small_LLM_Model()
    # id_token = {}
    try:
        prompt = JsonLoader(prompts).promt_validator()
        definition = JsonLoader(definitions).definitons_validator()
    except ValidatorError as e:
        print(e)
        return
    # id_token = id_to_token(llm)
    allowed_ids = allow_ids(definition, llm)
    for p in prompt:
        instructions = llm_prompt(definition, p)
        generator(instructions, p.prompt, allowed_ids, llm)

    # llm = Small_LLM_Model()
    # prompt1 = "what is the sum of 1 + 1, the answer is "
    # prompt2 = "how many letters has the word 'hello', the answer is "
    # prompt3 = "what color has the sky, the answer is "
    # prompt4 = "why do we have a nose, the answer is "

    # id1 = llm.encode(prompt1)
    # id2 = llm.encode(prompt2)
    # id3 = llm.encode(prompt3)
    # id4 = llm.encode(prompt4)

    # print(id1)
    # print(id2)
    # print(id3)
    # print(id4)

    # token1 = id1[0].tolist()
    # token2 = id2[0].tolist()
    # token3 = id3[0].tolist()
    # token4 = id4[0].tolist()

    # i = 0
    # logit_list1 = []
    # while i < 10:
    #     logit1 = llm.get_logits_from_input_ids(token1)
    #     next_token = logit1.index(max(logit1))
    #     logit_list1.append(next_token)
    #     token1.append(next_token)
    #     i += 1

    # print(llm.decode(id1))
    # print(logit_list1)
    # print(llm.decode(logit_list1))

    # i = 0
    # logit_list2 = []
    # while i < 10:
    #     logit2 = llm.get_logits_from_input_ids(token2)
    #     next_token = logit2.index(max(logit2))
    #     logit_list2.append(next_token)
    #     token2.append(next_token)
    #     i += 1

    # print(llm.decode(id2))
    # print(logit_list2)
    # print(llm.decode(logit_list2))

    # i = 0
    # logit_list3 = []
    # while i < 10:
    #     logit3 = llm.get_logits_from_input_ids(token3)
    #     next_token = logit3.index(max(logit3))
    #     logit_list3.append(next_token)
    #     token3.append(next_token)
    #     i += 1

    # print(llm.decode(id3))
    # print(logit_list3)
    # print(llm.decode(logit_list3))

    # i = 0
    # logit_list4 = []
    # while i < 10:
    #     logit4 = llm.get_logits_from_input_ids(token4)
    #     next_token = logit4.index(max(logit4))
    #     logit_list4.append(next_token)
    #     token4.append(next_token)
    #     i += 1

    # print(llm.decode(id4))
    # print(logit_list4)
    # print(llm.decode(logit_list4))

    # promt = "welche funktion rechent 1 + 1? die antwort ist"
    # ausgabe = []
    # encodet = llm.encode(promt)
    # logit = encodet[0].tolist()
    # # logits = llm.get_logits_from_input_ids(encodet[0].tolist())
    # i = 0
    # while (i < 50):
    #     logits = llm.get_logits_from_input_ids(logit)
    #     next_token = logits.index(max(logits))
    #     logit.append(next_token)
    #     i += 1
    # # print(logits)
    # print(llm.get_path_to_tokenizer_file())
    # with open(llm.get_path_to_tokenizer_file(), encoding="utf=8") as f:
    #     print(f)
    #     tokenizer = json.load(f)
    #     print(tokenizer)
    # print(llm.get_path_to_vocab_file())
    # # with open(llm.get_path_to_vocab_file()) as f:
    # #     print(f)
    # #     vocab = json.load(f)
    # #     print(vocab)
    # print(llm.get_path_to_merges_file())
    # print(llm.decode(logit))
    # decodet = llm.decode(encodet)
    # print(decodet)


if __name__ == "__main__":
    main()
