# Sensor Failure Compositionality

Paper 52 for the robotics 60-paper batch.

## Recovery artifacts

- Literature sweep rows: 1200
- Synthetic trials: 2400
- Manuscript source: `paper/main.tex`
- Build output: `paper/main.pdf`

## Synthetic summary

| Regime | Trials | Additive MAE | Compositional MAE | Gap |
|---|---:|---:|---:|---:|
| Independent | 800 | 0.0000 | 0.0000 | 0.0000 |
| Mild interactions | 800 | 0.0927 | 0.0000 | 0.0927 |
| Strong interactions | 800 | 0.1696 | 0.0000 | 0.1696 |

The core claim is that robot perception failures should be evaluated as composed interaction laws, not inferred from isolated dropout cases.
