from parse import Definition, Prompt


def llm_prompt(definitions: list[Definition], prompt: Prompt):
    instructions = '''
<|im_start|> you are a Function calling Ai tool.
Your job is to choose exactly the right function from the availble tools\
Read the user's request carefully.
Choose the function whose description best matches the request.
Extract all required arguments from the user's request.
<funktion_name> is one of the funktions in tools.
and the arguments are contained in the user pormpt string.

return ONLY valid JSON.

{
  "name": "fn_add_numbers",
  "arguments": {
    "a": 2,
    "b": 3
  }
}
Do not explain your answer.
Do not output any text before or after the JSON.

<tools>\n'''

    for definition in definitions:
        instructions += f'''
name: {definition.name}
description: {definition.description}

</tools>
'''
        for param, info in definition.parameters.items():
            instructions += f" - {param}: {info.type}"

    instructions += "</tools>\n"
    instructions += f'''
    user_input: {prompt.prompt}
'''

    return instructions
