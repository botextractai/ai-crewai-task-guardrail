# Implementing quality standards with function-based CrewAI Guardrails

In the [CrewAI](https://www.crewai.com/) framework, a "Task" is a specific assignment completed by an "Agent".

Task Guardrails provide a way to validate and auto-correct Task outputs before they are passed on to the next Task. This feature helps ensure data quality and provides feedback to Agents when their output doesn't meet specific criteria.

In CrewAI, Task Guardrails can be defined in two ways:

1. **Function-based Guardrails:** Python functions that implement any custom validation logic. This example shows a function-based CrewAI Guardrail.

2. **String-based Guardrails:** Natural language descriptions that are automatically converted to Large Language Model (LLM) powered validations. This approach automatically generates a `LLMGuardrail` instance using the string as validation criteria, and uses the Task's Agent LLM for validation through a temporary validation Agent that checks the output against the criteria. It returns detailed feedback if the validation fails. String-based Guardrails can use natural language to describe validation rules against harmful content including hate speech, harassment, sexual content, illegal activities, Personally Identifiable Information (PII) exposure, hallucinations, and prompt attacks, all without writing custom validation functions.

## This function-based CrewAI Guardrail example

CrewAI Guardrails are a powerful way to add custom validation logic to agentic workflows.

This example shows an Agent that writes a blog for a specific topic, in this case about "Climate Change" for the current calendar year. The function-based CrewAI Guardrail limits the number of words in that blog to a maximum of 100 words. Such program code based word counting might be required, because many LLMs are good with counting output tokens, but less so with correctly counting output words.

The `TaskOutput` object contains the output data of a completed Task. It gets passed to the CrewAI Guardrail function, which validates the output. In this example, the CrewAI Guardrail function counts how many words that the blog contains. If it's beyond the limit of 100 words, then it asks the Agent again and it does that iteratively until the output of the Task meets the word count, or gives up when it reaches the `max_retries` number.

This function-based CrewAI Guardrail example shows how to:

- Write a function-based CrewAI Guardrail
- Attach it to a Task
- Automatically retry until the output meets the criteria, or the number of retries reaches the `max_retries` number

It uses the search tool `SerperDevTool` to search the web for specific keywords trying to answer the question.

The final result is returned in Markdown format. The `rich` library is used to display the rendered Markdown in the terminal.

![alt text](https://github.com/user-attachments/assets/450906da-7534-4b9e-a9cd-63adef3ed10a "Guardrails")

## Required API keys for this example

1. You need an OpenAI API key for this example. [Get your OpenAI API key here](https://platform.openai.com/login). Insert the OpenAI API key into the `.env.example` file.
2. You also need a free Serper API key for this example. [Get your free Serper API key here](https://serper.dev/signup). Insert the Serper API key into the `.env.example` file.
3. Rename the `.env.example` file to just `.env` (remove the ".example" ending).

## Run this example

Simply run the `main.py` script.
