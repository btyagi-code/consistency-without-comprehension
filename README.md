# Consistency Without Comprehension

**Paraphrase consistency and statistical bias in zero-shot phishing detection**

Bhawna Tyagi, University of Massachusetts Amherst · [paper (PDF)](paper/main.pdf) · LaTeX source in `paper/main.tex`

## Question

If a classifier understands what an email means, rewording the email without changing its meaning should not change the label. This project tests whether four zero-shot natural language inference (NLI) classifiers keep their labels on meaning-preserving rewrites of short phishing and legitimate email messages, and whether a stable label is also a correct one.

## Dataset

`data/paraphrase_groups.json` (also as `data/paraphrase_groups.csv`) holds 60 paraphrase groups, each with three variants that keep the same meaning, for 180 messages in total.

| | Synonym | Syntactic | Manual rewrite | Total |
|---|---|---|---|---|
| Phishing | 11 | 8 | 11 | 30 |
| Legitimate | 11 | 8 | 11 | 30 |

Phishing groups are IDs 1–20 and 41–50. Legitimate groups are IDs 21–40 and 51–60. All messages were written by the author and do not come from real mailboxes.

## Models

All four are run through the Hugging Face `zero-shot-classification` pipeline with candidate labels `["phishing", "legitimate"]`. The prediction is the top-scoring label. There is no fine-tuning and no few-shot prompting.

| Short name | Model |
|---|---|
| bart | `facebook/bart-large-mnli` |
| roberta | `roberta-large-mnli` |
| deberta | `MoritzLaurer/deberta-v3-large-zeroshot-v2.0` |
| distilbart | `valhalla/distilbart-mnli-12-3` |

## Metrics

- **Consistency Score (CS):** the share of groups in which all three variants receive the same label. A random binary classifier scores 0.25.
- **Accuracy:** the share of variants labeled correctly, reported overall and per true class.
- **Consistent-Bias Rate (CBR):** the share of phishing groups labeled "legitimate" on all three variants. It separates stable understanding from stable error. A random classifier scores 0.125.

## Results

These results come from the original run (`results/predictions_original_run.csv`). The full set of tables is in `results/metrics.md`.

| Model | CS | Accuracy | Phishing acc. | Legitimate acc. | CBR |
|---|---|---|---|---|---|
| BART | 0.9000 | 0.6000 | 0.2000 | 1.0000 | 0.7000 |
| RoBERTa | 0.8500 | 0.6222 | 0.2444 | 1.0000 | 0.6000 |
| DeBERTa-v3 | 0.8167 | 0.9167 | 0.9111 | 0.9222 | 0.0333 |
| DistilBART | 0.9167 | 0.6000 | 0.2000 | 1.0000 | 0.7333 |

Three of the four models were highly consistent (CS 0.85–0.92), yet they caught only 20–24% of phishing messages. For 60–73% of phishing groups, they labeled every variant "legitimate." DeBERTa-v3 was the most accurate model (91.7%) and the least consistent (CS 0.82). High consistency alone is therefore not evidence of understanding.

Several groups were labeled phishing only in the variant containing a trigger phrase. In group 6, for example, BART and RoBERTa flagged only the variant that begins "Action required:".

## Reproducing

```bash
pip install -r requirements.txt
python code/run_eval.py --data data/paraphrase_groups.json --out results/predictions.csv   # GPU recommended; --device -1 for CPU
python code/compute_metrics.py results/predictions.csv
```

`notebooks/original_run.ipynb` is the Colab notebook that produced the original results, with its printed outputs kept. `results/predictions_original_run.csv` was reconstructed from those outputs. It records labels only, because the notebook's confidence scores were not saved. A fresh run of `run_eval.py` records confidences too. Results can differ slightly across library versions.

## Known limitations

- The messages are short, one- or two-sentence email texts, not full emails with headers or links.
- The dataset is small (60 groups), so differences of a few groups between models are not statistically meaningful on their own.
- Groups 39 and 60 share one identical variant ("Your password was updated successfully.").
- Paraphrase quality was checked manually by one annotator.

## License

Code: MIT (see `LICENSE`). Dataset and results: CC BY 4.0.
