import os
import datetime
from openai import OpenAI
import argparse
import pandas as pd
import nltk.translate.chrf_score as chrf
import anthropic

DEFAULT_MODEL = "gpt-4o-mini-2024-07-18"

def initialize_client(model_name):
    if model_name.startswith("gemini"):
        print("Using Gemini model, initializing client with Gemini API key.")
        client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
    elif model_name.startswith("deepseek"):
        print("Using DeepSeek model, initializing client with DeepSeek API key.")
        client = OpenAI(
            api_key=os.environ.get('DEEPSEEK_API_KEY'), 
            base_url="https://api.deepseek.com"
        )
    elif model_name.startswith("claude"):
        print("Using Claude model, initializing client with Claude API key.")
        client = anthropic.Client(api_key=os.getenv("ANTHROPIC_API_KEY"))
    else:
        print("Using OpenAI model, initializing client with OpenAI API key.")
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=OPENAI_API_KEY)

    #check validity
    validity = client.models.retrieve(model_name)
    print(validity)

    return client

def prompt(target_language, prompt, client, model):
    print(f"Prompting for {target_language}: {prompt}")
    if model.startswith("claude"):
        response = client.messages.create(
            model=model,
            max_tokens=1000,
            system=f"You are a knowledgable assistant that can respond in {target_language}.",
            messages=[
                {
                    "role": "user",
                    "content": f"'{prompt}'",
                }
            ],
        )
        return response.content[0].text.strip()
    else:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": f"You are a knowledgable assistant that can respond in {target_language}."
                },
                {
                    "role": "user",
                    "content": f"'{prompt}'",
                }
            ],
        )
        return response.choices[0].message.content.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vocabulary Quiz")
    parser.add_argument("prompt", type=str, help="The prompt for the story")
    parser.add_argument("--lang", type=str, default="Muscogee", help="The target language for the story")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Model name to use for the quiz")
    args = parser.parse_args()
    model_name = args.model

    # init
    client = initialize_client(model_name)

    current_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"out_{args.lang}_{model_name}_{current_date}.tsv"

    # record prompt to output file
    with open(output_file, "w") as f:
        f.write(f"Prompt:\t{args.prompt}\n\n")
        f.write(f"Target Language:\t{args.lang}\n\n")
        f.write(f"Model:\t{model_name}\n\n")

    # get response
    response = prompt(args.lang, args.prompt, client, model_name)
    # record response to output file
    with open(output_file, "a") as f:
        f.write(f"Response:\t{response}\n")