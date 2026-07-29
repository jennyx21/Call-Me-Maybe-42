from src.parse import Definition, Prompt


def llm_prompt(definitions: list[Definition], prompt: Prompt):
    instructions = """
You are a function calling AI.

Your task:
1. Choose exactly one function.
2. Extract the required arguments.
3. Return ONLY valid JSON.
Output format:
{
  "name": "function_name",
  "parameters": {
  }
}
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
</tools>

User:
"""

    instructions += prompt.prompt

    return instructions

