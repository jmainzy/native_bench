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

def get_questions(filename):
    question_list = []
    with open(filename, "r") as file:
        for line in file:
            question = line.split("\t")[0]
            options = []
            for option in line.strip().split("\t")[1:]:
                options.append(option)
            question_list.append((question, options))
    return question_list

def quiz(question, options, client, model):
    format_options = ""
    for idx, option in enumerate(options):
        format_options += f"{chr(65 + idx)}. {option} "
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "developer",
                "content": f"You are a helpful assistant that answers cultural questions about North American Indigenous peoples. You will respond to multiple choice questions with only the letter of the correct answer."
            },
            {
                "role": "user",
                "content": f"{question} Here are the options: {format_options} Respond with only the letter of the correct answer."
            }
        ],
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Culture Quiz")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Model name to use for the quiz")
    parser.add_argument("--question_file", type=str, default="./culture_questions.tsv", help="TSV file with quiz questions")
    args = parser.parse_args()
    model_name = args.model
    question_file = args.question_file

    # init
    client = initialize_client(model_name)

    # read word list from file
    question_list = get_questions(question_file)

    current_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"out_{model_name}_{current_date}.tsv"
    with open(output_file, "w") as result_file:
        for question, options in question_list:
            response_word = quiz(question, options, client, model_name)
            result_file.write(f"{question}\t{response_word}\n")
            print(f"{question} -> {response_word}")