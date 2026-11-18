"""Run the four zero-shot NLI classifiers on every paraphrase variant.

Usage:
    python code/run_eval.py --data data/paraphrase_groups.json --out results/predictions.csv

This is the evaluation loop from notebooks/original_run.ipynb, packaged as a script.
It records the predicted label and its confidence for each of the 180 variants per model.
No Hugging Face login is needed: all four models are public.
"""
import argparse
import json

import pandas as pd
from transformers import pipeline

CANDIDATE_LABELS = ["phishing", "legitimate"]

MODELS = {
    "bart": "facebook/bart-large-mnli",
    "roberta": "roberta-large-mnli",
    "deberta": "MoritzLaurer/deberta-v3-large-zeroshot-v2.0",
    "distilbart": "valhalla/distilbart-mnli-12-3",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", default="data/paraphrase_groups.json")
    parser.add_argument("--out", default="results/predictions.csv")
    parser.add_argument("--device", type=int, default=0, help="GPU index, or -1 for CPU")
    args = parser.parse_args()

    with open(args.data) as f:
        groups = json.load(f)

    rows = []
    for model_name, model_id in MODELS.items():
        clf = pipeline("zero-shot-classification", model=model_id, device=args.device)
        for group in groups:
            for i, text in enumerate(group["variants"], start=1):
                out = clf(text, candidate_labels=CANDIDATE_LABELS, multi_label=False)
                rows.append({
                    "model": model_name,
                    "group_id": group["group_id"],
                    "true_label": group["label"],
                    "paraphrase_type": group["paraphrase_type"],
                    "variant_index": i,
                    "variant_text": text,
                    "predicted_label": out["labels"][0],
                    "confidence": round(out["scores"][0], 4),
                })
        print(f"finished {model_name}")

    pd.DataFrame(rows).to_csv(args.out, index=False)
    print(f"saved {len(rows)} predictions to {args.out}")


if __name__ == "__main__":
    main()
