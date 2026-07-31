from src.parse import Definition, Prompt


def llm_prompt_names(definitions: list[Definition], prompt: Prompt):
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


def llm_prompt_params(definition: Definition, prompt: Prompt):
    instructions = """\
<|im_start|>system.

You are a function parameter extraction AI.

Your task:
Extract the parameters from the user request and fill the function arguments.
dont change them in anyway.

Rules:.
- Do not add extra parameters.
- Use the correct type for each parameter.
- Only use information from the user request.
- end every parameter with a ","\

Function:
"""
    for param in definition.parameters:
        instructions += f"""
type: {definition.parameters[param].type}
"""
    instructions += f"""
User request:
{prompt.prompt}

Output:
"""
    return instructions
