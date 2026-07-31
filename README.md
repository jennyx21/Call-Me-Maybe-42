*This project has been created as part of the 42 curriculum by jtruckse.*

# Call-Me-Maybe

## Description

Call-Me-Maybe is a function calling AI project developed as part of the 42 curriculum.

The goal of this project is to build a lightweight function-calling system using a Small Language Model (LLM). Given a natural language user request and a list of available functions, the program must identify the correct function and extract the required parameters.

The project implements constrained decoding techniques to guide the LLM output and improve reliability. Instead of allowing the model to freely generate text, the generation process is restricted according to available functions, parameter types, and expected outputs.

The system is able to:
- Select the most appropriate function from a dynamic function list.
- Extract parameters from user prompts.
- Handle different parameter types such as strings, integers, and numbers.
- Produce structured outputs compatible with function execution.

---

## Instructions

### Installation

#### Clone the repository:

```bash
make install #to install the requirements
```
#### execution: 

```bash
make run # for default input and output
uv run -m src --input <file_path> --functions_definitions <file_path> --output <file_path> # to run on costum file input and output 
```

#### make command explainaition:
```bash
make clean # to remove all generatet files
make debug # to run the program with a debugger
make lint # mypy and flake8 
make lint-strict # mypy strict and flake8
```

## algorithm explaination and Design decsision

#### Funktion name extraction

The first step is selecting the correct function. 

The LLM resives a prompt string wich tells the LLM to only extract the function name by the given funktions. The model choose the function that is represented the best by the user_input

To avoid invalid function names constrained decoding is used: 

- Each available function name is tokenized
- the llm can only choose from the available tokens 
- tokens that are not contained in the function name get to -inf so the LLM does not consider them

#### Parameter extraktion

After selecting the Funktion, only the parameters belonging to this funktion are processed. 

For this a second LLM instruction Prompt is implemented.

depending on the parameter type, differen constraints are applied: 

##### Numbers/Integers

Posible Numbers get extracted from the user input. 
the LLM can only choose one of the extracted values. 

if the llm generated token sequence matches the required values the loop stops. if there are more than one value contained in the user input, the createt value gets removed form the exteactd value list, so the Modle can only choose from the ones left in the list. 

this prevents the model from inventig incorrect values.

##### Strings

To extract string parameters from the LLM output, the project uses a constrained decoding approach to ensure that generated values always follow JSON string syntax.

Instead of generating arbitrary text and validating it afterwards, the decoder restricts the possible next tokens during generation. After every generated token, the current output is checked by a small JSON string state machine.

The state machine validates:
- the opening and closing quotation marks (`"`)
- valid escape sequences (`\"`, `\\`, `\n`, `\t`, etc.)
- invalid control characters inside strings

Unicode escape sequences are not handled because they are unnecessary for the current use case.

The generation process works as follows:

1. Start generation with an opening quotation mark (`"`).
2. Retrieve the model logits for the next token.
3. Select the highest probability token that keeps the current output as a valid JSON string prefix.
4. Reject invalid tokens by assigning them a probability of negative infinity.
5. Continue until a valid closing quotation mark is generated.
6. Parse the final result using Python's JSON parser to ensure the generated value is a valid string.

This approach reduces invalid outputs and allows the small language model to reliably generate structured parameters required by the application.

## Performance Analysis

#### Accuracy
The accuracy of the solution mainly depends on the quality of the function descriptions and the ability of the language model to understand the user's request.

To improve accuracy, constrained decoding is used instead of allowing unrestricted text generation. The model is only allowed to generate valid function names and parameter values according to the available definitions.

#### Speed

The main performance cost comes from the constrained decoding process because possible tokens must be checked during generation.

Several optimizations were applied:
- Function definitions are processed dynamically only when needed.
- Token sequences are reused instead of repeatedly rebuilding them.
- The generation process stops as soon as a valid output is found.
- Invalid tokens are removed before selecting the next token.

#### Reliability

The reliability of the system is improved by combining LLM reasoning with deterministic validation.

The model is responsible for understanding the user's intention, while the program guarantees that:
- Only existing functions can be selected.
- Parameters follow their expected types.
- Generated strings are valid JSON strings.
- The final output format remains consistent.

This hybrid approach reduces hallucinations and makes the output predictable.
But in the end it still needs improvement to be 100% realiable


## Challenges Faced

#### Understanding Token-Based Generation

One of the main challenges was understanding how language models generate text internally.

Function names and parameter values are not always represented as complete words. A single function name can be split into multiple tokens.
The solution was to work with token sequences and restrict the model generation step by step instead of comparing complete strings only.

#### Implementing Constrained Decoding

Building a constrained decoder was challenging because the model normally chooses from the entire vocabulary.

The solution was to filter the logits before every generation step and set invalid token probabilities to negative infinity. This forces the model to stay inside the allowed output space.

#### Extracting Parameters Correctly

Another challenge was extracting parameters from natural language prompts.

The model could sometimes:
- Change the order of parameters.
- Repeat values.
- Select incorrect numbers.
- Stop generating at the wrong position.

This was solved by using parameter type information from the function definition and applying different extraction strategies for numbers, integers, and strings.

#### Handling String Parameters

Strings were difficult because the model must know when a string value is complete.

A JSON string validation system was implemented to check generated tokens continuously and only accept valid string states.

## Testing Strategy

The implementation was validated using multiple testing approaches.

- input data from subject
- own costum input with ambigous function names

#### Edge Cases

The system was also tested with:
- Multiple numbers in a prompt.
- Strings containing special characters.
- Different function definitions.
- Functions with different parameter counts.

The goal was to ensure that the implementation works dynamically and does not depend on hardcoded function names.

## Example Usage

#### Running the Program

The program can be executed with:

```bash
make run
```

or directly:
``` bash
uv run python -m src \
    --input data/input/function_calling_tests.json \
    --functions_definition data/input/functions_definition.json \
    --output data/output/result.json
```

#### Example Input

```json
User prompt: "Calculate the sum of 15 and 27"
```
in the json file 

#### Function definition:
```json
{
    "name": "fn_add_numbers",
    "parameters": {
        "a": {
            "type": "number"
        },
        "b": {
            "type": "number"
        }
    }
}
```
#### Example Output
```json
{
    "name": "fn_add_numbers",
    "parameters": {
        "a": 15.0,
        "b": 27.0
    }
}
```

## Resources

- https://medium.com/@albersj66/part-6-implementing-constrained-decoding-for-phi-3-vision-2c72a1be6a17
- https://medium.com/@newlearner1995/llm-wrapper-351bd8dd2433

#### Ai usage 
Ai was used as a learning tool. 

usage for: 
- Understanding concepts related to Large Language Models (LLMs), tokenization, and constrained decoding.
- Debugging Python errors and improving code quality.
- Improving the structure and clarity of the project documentation.

AI was used as a support tool for learning, problem solving, and reviewing ideas. The implementation, architecture decisions and final code were developed and validated by the project author.