from src.parse import Definition, Prompt


def llm_prompt(definitions: list[Definition], prompt: Prompt):
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
Parameters:
"""
        for param, info in definition.parameters.items():
            instructions += f"- {param}: {info.type}\n"
    instructions += """
<|im_end|>\n
</tools>

User:
"""

    instructions += prompt.prompt

    return instructions
