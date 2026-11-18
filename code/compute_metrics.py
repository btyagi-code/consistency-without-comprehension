"""Compute every table in the paper from a predictions CSV.

Usage:
    python code/compute_metrics.py results/predictions_original_run.csv > results/metrics.md

Metrics
- Consistency Score (CS): share of paraphrase groups whose three variants all get the same label.
- Accuracy: share of variants labeled correctly, overall and per true class.
- Consistent-Bias Rate (CBR): share of phishing groups labeled "legitimate" on all three variants.
"""
import sys

import pandas as pd

MODEL_NAMES = {
    "bart": "BART (facebook/bart-large-mnli)",
    "roberta": "RoBERTa (roberta-large-mnli)",
    "deberta": "DeBERTa-v3 (MoritzLaurer/deberta-v3-large-zeroshot-v2.0)",
    "distilbart": "DistilBART (valhalla/distilbart-mnli-12-3)",
}


def group_table(df):
    g = df.groupby("group_id").agg(
        true_label=("true_label", "first"),
        paraphrase_type=("paraphrase_type", "first"),
        preds=("predicted_label", list),
    )
    g["consistent"] = g["preds"].apply(lambda p: len(set(p)) == 1)
    g["all_legit"] = g["preds"].apply(lambda p: all(x == "legitimate" for x in p))
    return g


def cs(g):
    return g["consistent"].mean()


def main(path):
    df = pd.read_csv(path)
    df["correct"] = df["predicted_label"] == df["true_label"]
    models = [m for m in MODEL_NAMES if m in df["model"].unique()]

    print("## Overall\n")
    print("| Model | CS | Accuracy | Phishing acc. | Legitimate acc. | CBR |")
    print("|---|---|---|---|---|---|")
    for m in models:
        d = df[df.model == m]
        g = group_table(d)
        ph = g[g.true_label == "phishing"]
        print(f"| {MODEL_NAMES[m]} | {cs(g):.4f} | {d.correct.mean():.4f} | "
              f"{d[d.true_label == 'phishing'].correct.mean():.4f} | "
              f"{d[d.true_label == 'legitimate'].correct.mean():.4f} | "
              f"{ph.all_legit.mean():.4f} |")
    print("| Random baseline | 0.2500 | 0.5000 | 0.5000 | 0.5000 | 0.1250 |\n")

    print("## CS by paraphrase type\n")
    print("| Type | " + " | ".join(models) + " |")
    print("|---|" + "---|" * len(models))
    for t in ["synonym", "syntactic", "manual"]:
        vals = [cs(group_table(df[(df.model == m) & (df.paraphrase_type == t)])) for m in models]
        print(f"| {t} | " + " | ".join(f"{v:.4f}" for v in vals) + " |")

    print("\n## CS by true label\n")
    print("| Label | " + " | ".join(models) + " |")
    print("|---|" + "---|" * len(models))
    for lab in ["phishing", "legitimate"]:
        vals = [cs(group_table(df[(df.model == m) & (df.true_label == lab)])) for m in models]
        print(f"| {lab} | " + " | ".join(f"{v:.4f}" for v in vals) + " |")

    print("\n## Inconsistent groups\n")
    for m in models:
        g = group_table(df[df.model == m])
        bad = g[~g.consistent]
        items = ", ".join(f"{gid} ({r.true_label}, {r.paraphrase_type})" for gid, r in bad.iterrows())
        print(f"- **{m}** ({len(bad)}): {items}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "results/predictions_original_run.csv")
