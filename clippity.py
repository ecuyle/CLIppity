import openai
import os
import sys
from dotenv import load_dotenv


load_dotenv()
openai.api_key = os.getenv("API_KEY")
messages = []
token_usage = {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}


def calculate_token_cost(tokens):
    dollarPerToken = 0.000002
    return '${:,.7f}'.format(tokens * dollarPerToken)


def get_response(prompt_text):
    messages.append({"role": "user", "content": prompt_text})

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )
        messages.append(response.choices[0].message)
        token_usage["prompt_tokens"] += response.usage.prompt_tokens
        token_usage["completion_tokens"] += response.usage.completion_tokens
        token_usage["total_tokens"] += response.usage.total_tokens

        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {e}"


def main():
    print("ChatGPT CLI. Type 'exit' or 'quit' to end.")

    while True:
        prompt = input("> ")
        if prompt.lower() in ["exit", "quit"]:
            print("--------------------------------------------------")
            print("Conversation Summary:")
            print("--------------------------------------------------")
            print("Token Usage")
            print(f"  Prompt Tokens:     {token_usage['prompt_tokens']}")
            print(f"  Completion Tokens: {token_usage['completion_tokens']}")
            print(f"  Total Tokens:      {token_usage['total_tokens']}")
            print(
                f"Total Cost: {calculate_token_cost(token_usage['total_tokens'])}")
            print("\n")
            print("Goodbye!")
            sys.exit()

        response = get_response(prompt)
        print("CLIppity: ", response + "\n")


if __name__ == '__main__':
    main()
