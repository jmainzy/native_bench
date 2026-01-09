import os
import datetime
from openai import OpenAI
import argparse

DEFAULT_MODEL = "gpt-4o-mini-2024-07-18"

def initialize_client(model_name):
    if model_name.startswith("gemini"):
        client = OpenAI(
            api_key=os.getenv("GEMINI_API_KEY"),
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
        )
    else:
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        client = OpenAI(api_key=OPENAI_API_KEY)

    #check validity
    validity = client.models.retrieve(model_name)
    print(validity)

    return client

def get_word_list(filename):
    word_list = []
    with open(filename, "r") as file:
        for line in file:
            word_list.append(line.strip().split("\t")[0])
    return word_list

def quiz(english_word, client, model, response_language):
    # Responses API is not supported for all models, this is a newer thing from OpenAI
    # response = client.responses.create(
    #     model=model,
    #     instructions=f"Respond with only the {response_language} word for the given English word.",
    #     input=english_word
    # )
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "developer",
                "content": f"You are a helpful assistant that translates English words into {response_language}."
            },
            {
                "role": "user",
                "content": f"What is the {response_language} word for '{english_word}'? Respond with only the translated word."
            }
        ],
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vocabulary Quiz")
    parser.add_argument("language", type=str, help="Target language for the quiz (e.g., Muscogee, Choctaw)")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Model name to use for the quiz")
    args = parser.parse_args()
    response_language = args.language
    model_name = args.model

    # init
    client = initialize_client(model_name)

    # read word list from file
    word_list = get_word_list("./vocab_list.tsv")

    current_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"out_{response_language}_{model_name}_{current_date}.tsv"
    with open(output_file, "w") as result_file:
        for english_word in word_list:
            response_word = quiz(english_word, client, model_name, response_language)
            result_file.write(f"{english_word}\t{response_word}\n")
            print(f"{english_word} -> {response_word}")