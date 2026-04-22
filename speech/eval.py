# Example using Hugging Face evaluate
import argparse
import pandas as pd
import jiwer
import os


def read_file(predictions_file):
    df = pd.read_csv(predictions_file, sep="\t")
    # print column names
    print(df.columns)
    return df

def calculate_eval(data):
    cer = []
    wer = []
    for index, row in data.iterrows():
        reference = row["Transcription"]
        preds = row["Predictions"]
        # calculate CER and WER here
        cer.append(jiwer.cer(reference, preds))
        wer.append(jiwer.wer(reference, preds))

    data["CER"] = cer
    data["WER"] = wer
    return data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Calculate CER and WER scores")
    parser.add_argument("predictions_file", type=str, help="TSV file with predictions and references")
    args = parser.parse_args()
    predictions_file = args.predictions_file
    data = read_file(predictions_file)
    df = calculate_eval(data)

    # get filename
    filename = os.path.basename(predictions_file)
    output_file = filename.replace(".tsv", "_scores.tsv")
    # save results to tsv file
    df.to_csv(output_file, sep="\t", index=False)