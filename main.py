import os
import json
import sys
from dotenv import load_dotenv
from openai import OpenAI
from argparse import *
from prompts import *
from call_function import *


def main():
    # Set up API, variables as well as evnironment
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")
    if api_key is None:
        raise RuntimeError("api_key is None")
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key
    )
    # Parse the prompt from command line
    parser = ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    # Now we can access `args.user_prompt` which store user prompt
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    # Get response from LLM
    for _ in range(20):
        response = create_response(client, messages)
        message = response.choices[0].message
        messages.append(message)
        if message.tool_calls:
            for tool_call in message.tool_calls:
                result_message = call_function(tool_call, args.verbose)
                if not result_message.get("content"):
                    raise Exception("function need content")
                if args.verbose:
                    print(f"-> {result_message['content']}")
                messages.append(result_message)
        else:
            break
    else:
        sys.exit(1)

    prompt_token = response.usage.prompt_tokens
    response_token = response.usage.completion_tokens
    # Print tool call if any and response
    if args.verbose:
        print(f"User prompt: {args.user_prompt}\nPrompt tokens: {prompt_token}\nResponse tokens: {response_token}")
    else:
        print("Response:")
        print(response.choices[0].message.content)


def create_response(client, messages: list[dict[str, object]]):
    try:
        response = client.chat.completions.create(
            model="openrouter/free",
            messages=messages,
            tools=available_functions,
            temperature=0,
        )
        return response
    except RateLimitError:
        raise RuntimeError("Rate limit reached")


if __name__ == "__main__":
    main()
