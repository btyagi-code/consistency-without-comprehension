## Overall

| Model | CS | Accuracy | Phishing acc. | Legitimate acc. | CBR |
|---|---|---|---|---|---|
| BART (facebook/bart-large-mnli) | 0.9000 | 0.6000 | 0.2000 | 1.0000 | 0.7000 |
| RoBERTa (roberta-large-mnli) | 0.8500 | 0.6222 | 0.2444 | 1.0000 | 0.6000 |
| DeBERTa-v3 (MoritzLaurer/deberta-v3-large-zeroshot-v2.0) | 0.8167 | 0.9167 | 0.9111 | 0.9222 | 0.0333 |
| DistilBART (valhalla/distilbart-mnli-12-3) | 0.9167 | 0.6000 | 0.2000 | 1.0000 | 0.7333 |
| Random baseline | 0.2500 | 0.5000 | 0.5000 | 0.5000 | 0.1250 |

## CS by paraphrase type

| Type | bart | roberta | deberta | distilbart |
|---|---|---|---|---|
| synonym | 0.9545 | 0.9545 | 0.8636 | 0.9545 |
| syntactic | 0.9375 | 0.8750 | 0.8750 | 0.8750 |
| manual | 0.8182 | 0.7273 | 0.7273 | 0.9091 |

## CS by true label

| Label | bart | roberta | deberta | distilbart |
|---|---|---|---|---|
| phishing | 0.8000 | 0.7000 | 0.8333 | 0.8333 |
| legitimate | 1.0000 | 1.0000 | 0.8000 | 1.0000 |

## Inconsistent groups

- **bart** (6): 6 (phishing, manual), 13 (phishing, syntactic), 16 (phishing, manual), 17 (phishing, synonym), 19 (phishing, manual), 49 (phishing, manual)
- **roberta** (9): 2 (phishing, syntactic), 6 (phishing, manual), 9 (phishing, manual), 13 (phishing, syntactic), 16 (phishing, manual), 17 (phishing, synonym), 19 (phishing, manual), 43 (phishing, manual), 49 (phishing, manual)
- **deberta** (11): 5 (phishing, syntactic), 9 (phishing, manual), 13 (phishing, syntactic), 20 (phishing, manual), 34 (legitimate, synonym), 38 (legitimate, manual), 39 (legitimate, synonym), 43 (phishing, manual), 53 (legitimate, manual), 59 (legitimate, manual), 60 (legitimate, synonym)
- **distilbart** (5): 2 (phishing, syntactic), 6 (phishing, manual), 13 (phishing, syntactic), 17 (phishing, synonym), 19 (phishing, manual)
