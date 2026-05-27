# Example using Hugging Face evaluate
import argparse
import sacrebleu
import pandas as pd
import os

def read_file(predictions_file):
    df = pd.read_csv(predictions_file, sep="\t")
    # print column names
    print(df.columns)
    return df

def calculate_chrf(data):
    chrf_target = []
    chrf_en = []
    chrf = sacrebleu.CHRF(word_order=2, beta=2) 
    for index, row in data.iterrows():
        chrf_target.append(chrf.sentence_score(row["EN->Target"], [row["Target Phrase"]]).score / 100)
        chrf_en.append(chrf.sentence_score(row["Target->EN"], [row["Source Phrase"]]).score / 100)
    data["CHRF_target"] = chrf_target
    data["CHRF_en"] = chrf_en
    return data



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate chrf score")
    parser.add_argument("predictions_file", type=str, help="TSV file with predictions and references")
    args = parser.parse_args()
    predictions_file = args.predictions_file
    data = read_file(predictions_file)
    df = calculate_chrf(data)

    # get filename
    filename = os.path.basename(predictions_file)
    output_file = filename.replace(".tsv", "_chrf2_scores.tsv")
    # save results to tsv file
    df.to_csv(output_file, sep="\t", index=False)