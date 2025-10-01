#!/usr/bin/env python

import os
import sys
from typing import List, Optional

from dotenv import load_dotenv
from google import genai
from google.genai import types
from websockets import Response

from config import MAX_ITERS, system_prompt
from functions.call_function import available_functions, call_function


def main() -> None:
    """Main entry point for the AI coding agent.
    
    Processes command-line arguments, initializes the Gemini API client,
    and iteratively generates content based on user prompts.
    Exits when a final response is generated or max iterations are reached.
    """
    iteration_loop = 0
    load_dotenv()

    verbose = "--verbose" in sys.argv
    args = [arg for arg in sys.argv[1:] if not arg.startswith("--")]

    if not args:
        print("Usage: python3 main.py <prompt>")
        sys.exit(1)

    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)

    user_prompt = " ".join(args)

    if verbose:
        print(f"User prompt: {user_prompt}\n")

    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    while True:
        iteration_loop += 1
        if iteration_loop > MAX_ITERS:
            print(f"Max iterations ({MAX_ITERS}) reached")
            sys.exit(1)

        try:
            final_response = generate_content(client, messages, verbose)
            if final_response:
                print("Final response:")
                print(final_response)
                break
        except Exception as e:
            print(f"Error in generate_content: {e}")


def generate_content(
    client: genai.Client, messages: List[types.Content], verbose: bool
) -> Optional[str]:
    """Generate content using the Gemini API with function calling support.
    
    Args:
        client: The Gemini API client instance.
        messages: List of conversation messages including user prompts and tool responses.
        verbose: If True, prints detailed information about token usage and function calls.
    
    Returns:
        The final text response from the model, or None if function calls are needed.
    
    Raises:
        Exception: If function call results are empty or malformed.
    """
    response = client.models.generate_content(
        model="gemini-2.0-flash-001",
        contents=messages,
        config=types.GenerateContentConfig(
            tools=[available_functions], system_instruction=system_prompt
        ),
    )
    if verbose:
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    if response.candidates:
        for item in response.candidates:
            messages.append(item.content)

    if not response.function_calls:
        return response.text

    function_responses = []
    for function_call_part in response.function_calls:
        function_call_result = call_function(function_call_part, verbose)
        if (
            not function_call_result.parts
            or not function_call_result.parts[0].function_response
        ):
            raise Exception("empty function call result")
        if verbose:
            print(f"-> {function_call_result.parts[0].function_response.response}")
        function_responses.append(function_call_result.parts[0])

    if not function_responses:
        raise Exception("no function responses generated, exiting.")

    messages.append(types.Content(role="tool", parts=function_responses))


if __name__ == "__main__":
    main()
