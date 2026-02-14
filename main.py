import os
import argparse
from dotenv import load_dotenv
from call_function import available_functions
from call_function import call_function
from google import genai
from google.genai import types
from prompts import system_prompt


def main():
    print("Hello from ai-agent!")
    load_dotenv()

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    try:
        api_key = os.environ.get("GEMINI_API_KEY")
    except RuntimeError:
        print("Could not get API key")

    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    client = genai.Client(api_key=api_key)
    
    for _ in range(15):
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(tools=[available_functions],system_instruction=system_prompt)
        )
        if response.usage_metadata is None:
            raise RuntimeError("API request failed")

        if response.candidates is not None:
            for message in response.candidates:
                messages.append(message.content)

        if args.verbose:
            print(
                f"User prompt: {args.user_prompt} \nPrompt tokens: {response.usage_metadata.prompt_token_count}\nResponse tokens: {response.usage_metadata.candidates_token_count}"
            )
        function_results = []
        if response.function_calls is not None:
            for f in response.function_calls:
                print(f'Calling function "{f.name}" on: {f.args}\n')
                function_call_result = call_function(f)
                if function_call_result.parts[0].function_response is None:
                    raise Exception("  Error: {err}")
                if function_call_result.parts[0].function_response.response is None:
                    raise Exception("  Error: {err}")
                if args.verbose:
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                function_results.append(function_call_result.parts[0])
            messages.append(types.Content(role="user", parts=function_results))
        else:
            print(response.text)
            exit(0)
    exit(1)

if __name__ == "__main__":
    main()
