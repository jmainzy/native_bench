import os
import datetime
from openai import OpenAI
import argparse
import pandas as pd
import nltk.translate.chrf_score as chrf

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

def get_phrase_list(filename):
    phrase_list = []
    # phrase list should be in format <language_name>\t<target_language_phrase>\t<english_phrase>
    with open(filename, "r") as file:
        for line in file:
            phrase_list.append(line.strip().split("\t"))
    return phrase_list

def quiz(source_language, target_language, phrase, client, model):
    print(f"Translating from {source_language} to {target_language}: {phrase}")
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "developer",
                "content": f"You are a helpful assistant that translates phrases from {source_language} to {target_language}."
            },
            {
                "role": "user",
                "content": f"What is the {target_language} translation for '{phrase}'? Respond with only the translated phrase."
            }
        ],
    )
    return response.choices[0].message.content.strip()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Vocabulary Quiz")
    parser.add_argument("--phrase_list_file", type=str, default="./phrase_list_demo.tsv", help="TSV file with phrases to translate")
    parser.add_argument("--model", type=str, default=DEFAULT_MODEL, help="Model name to use for the quiz")
    args = parser.parse_args()
    phrase_list_file = args.phrase_list_file
    model_name = args.model

    # init
    client = initialize_client(model_name)

    # read word list from file
    phrase_list = get_phrase_list(phrase_list_file)

    current_date = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    output_file = f"out_{model_name}_{current_date}.tsv"

    # 1. en -> target
    en_target_responses = []
    for language_name, target_phrase, source_phrase in phrase_list:
        response = quiz("English", language_name, source_phrase, client, model_name)
        en_target_responses.append(response)
        print(f"{source_phrase} -> {response}")
        
    # 2. target -> en
    target_en_responses = []
    for language_name, target_phrase, source_phrase in phrase_list:
        response = quiz(language_name, "English", target_phrase, client, model_name)
        target_en_responses.append(response)
        print(f"{target_phrase} -> {response}")

    # write results
    df = pd.DataFrame(phrase_list, columns=["Language", "Target Phrase", "Source Phrase"])
    df["EN->Target"] = en_target_responses
     # calculate chrf score
    df["CHRF_target"] = df.apply(lambda row: chrf.sentence_chrf(row["Target Phrase"], row["EN->Target"]), axis=1)
    df["Target->EN"] = target_en_responses
    df["CHRF_en"] = df.apply(lambda row: chrf.sentence_chrf(row["Source Phrase"], row["Target->EN"]), axis=1)

    df.to_csv(output_file, sep="\t", index=False)