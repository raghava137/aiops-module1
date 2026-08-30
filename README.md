 # AI Operations (AIOps) — Module 1 Assignment

**Raghava** · Roll No: DA24B021

Experiment management and reproducibility: MLflow tracking, DVC data
versioning, and an end-to-end reproducibility drill run with a partner.

The written report covering all four questions is
[`da3408_report_1.pdf`](da3408_report_1.pdf).

---

## Repository layout

```
.
├── da3408_report_1.pdf          written report, all four questions
├── .dvc/                        DVC config (S3 remote)
├── q2/                          MLflow experiment tracking
│   ├── MLFLOW.ipynb             MNIST + MLPClassifier, six-run sweep
│   ├── logging_snippet.py       the log_param / log_metric code
│   ├── curves.png               train_loss and val_accuracy per epoch
│   ├── generalization_gap.png   train_acc − val_acc per epoch
│   └── comparision_table_screenshots/
├── q3/                          DVC data versioning and rollback
│   ├── make_filelist_csv.py     builds the manifest from data/
│   ├── filelist.csv.dvc         DVC pointer (data itself lives in S3)
│   └── Screenshot ...           rollback evidence
└── q4/                          reproducibility capstone (Partner B)
```

---

## Question 1 — Technical debt diagnosis

| Symptom | Category |
|---|---|
| (a) Delivery-time rounding hurt an unrelated feature | Entanglement (CACE) |
| (b) Marketing silently reading the output table | Undeclared Consumers |
| (c) Fourteen undocumented shell scripts | Configuration and Glue-Code Debt |

The proposed fix for (c) is in the report: rewrite the scripts as a DVC pipeline
with each step declared in `dvc.yaml` and all hyperparameters in one
`params.yaml`.

---

## Question 2 — MLflow experiment comparison

Six runs on a 20,000-image subset of MNIST with an `MLPClassifier`, 25 epochs
each, varying learning rate (0.0001, 0.001, 0.01) and batch size (32, 256).
The starter script's `load_iris` was replaced with MNIST and
`RandomForestClassifier` with `MLPClassifier`.

| Run | lr | batch | best val acc | final train loss |
|---|---|---|---|---|
| `mlp-lr0.001-bs32` | 0.001 | 32 | **0.9688** | 0.0095 |
| `mlp-lr0.01-bs256` | 0.01 | 256 | 0.9625 | 0.0304 |
| `mlp-lr0.001-bs256` | 0.001 | 256 | 0.9615 | 0.0233 |
| `mlp-lr0.01-bs32` | 0.01 | 32 | 0.9523 | 0.1136 |
| `mlp-lr0.0001-bs32` | 0.0001 | 32 | 0.9495 | 0.1147 |
| `mlp-lr0.0001-bs256` | 0.0001 | 256 | 0.9263 | 0.2310 |

Learning rate mattered about four times as much as batch size: mean peak
accuracy moved 0.0272 across the three learning rates against 0.0068 across the
two batch sizes.

Metrics are logged with `step=epoch`, which makes them time series rather than
single scalars. That is what produces `curves.png` and `generalization_gap.png`
and allows the overfitting discussion in the report.

**Reproducing:**

```bash
mlflow server --backend-store-uri sqlite:///mlflow.db \
    --artifacts-destination ./mlartifacts --serve-artifacts \
    --host 0.0.0.0 --port 5000

export MLFLOW_TRACKING_URI=http://localhost:5000
jupyter lab q2/MLFLOW.ipynb
```

MNIST downloads on first run and caches to `mnist_cache.npz`, which is
gitignored.

---

## Question 3 — DVC data versioning and rollback

A CSV manifest of the cats-vs-dogs dataset, versioned with DVC against an
**AWS S3** remote.

| Version | Image files | CSV lines | Tag |
|---|---|---|---|
| v1 | 1800 | 1801 | `v1.0` |
| v2 | 2800 | 2801 | `v2.0` |

The rollback shows why both tools are needed:

```
2801   on v2
2801   after `git checkout v1.0`      pointer moved, bytes unchanged
1801   after `dvc checkout`           bytes fetched from the cache
```

`.dvc/config` holds the bucket URL and is committed. Credentials live in
`.dvc/config.local`, which DVC gitignores, and are not in this repository.

---

## Question 4 — Reproducibility capstone

Completed with **Shruthi** (Partner A). I was **Partner B**: my role was to
rebuild her run from the repository alone, with no communication about the
environment or the data.

**Shared repository:**
https://github.com/Shruthi276/reproducibility_capstone

**Result: MATCH.** `final_test_accuracy` reproduced at exactly **0.969200**
against a stated tolerance of ±0.005, giving a delta of **0.000000**. Every
logged parameter matched, and the dataset SHA256 matched Partner A's logged
tag, confirming identical training bytes.

Reproduction used only `git clone`, `git checkout` of her logged commit,
`conda env create -f environment.yml`, `dvc pull` and `dvc checkout`, and a
rerun of her unmodified training script.

Evidence is in [`q4/`](q4/).

---

## Notes

- On a fresh clone the DVC cache is gitignored and therefore empty, so
  `dvc checkout` alone links nothing; `dvc pull` has to fetch the bytes first.
  The rubric names only `dvc checkout`, but both are needed in practice.
- The protocol pins code (Git), environment (Conda), data (DVC) and run
  configuration (MLflow). It does not pin the tracking infrastructure itself,
  which is a gap that only appears once a second machine tries to use it.
