# AI Use Disclosure

Raghava · DA24B021 · AIOps Module 1

I used an AI assistant Claude while working on this assignment. Below is what it was
used for and what it was not.

## Where AI was used

To format and neat up the .md presentable files


**MLflow logging syntax.** Looked up the correct API calls and their arguments:
`log_param` vs `log_params`, `log_metric` with `step=` for time series metrics,
`log_metrics` for the final scalars, `set_tag`, `log_artifact`, and
`log_model` with a signature

**AWS S3 setup and Linux configuration.** Setting up the S3 bucket, writing the
IAM policy, and understanding why `s3:ListBucket` needs the bucket ARN without
`/*` while `s3:GetObject` needs it with `/*`. Also used for getting the whole
thing working inside a UTM Linux VM: installing DVC with S3 support, keeping
credentials in `.dvc/config.local` instead of the committed config, and
diagnosing a `RequestTimeTooSkewed` error that turned out to be the VM's clock
drifting after a suspend.

**Question 4 debugging.** This is where I used it most. Several things broke
during the reproduction and I used AI to work out what was actually wrong:

- `dvc pull` returning 403 on Partner A's bucket, which came down to a fresh
  clone having no `.dvc/config.local` so DVC was falling back to the wrong
  AWS profile
- a `ValueError: Found array with dim 3` from `MLPClassifier`, traced to the
  DVC-tracked dataset being stored as 60000x28x28 while the training code
  expected 60000x784
- `PermissionError: '/home/shruthi-rathod'` on artifact logging, traced to the
  tracking server running without `--serve-artifacts` and handing my machine an
  absolute path on hers
- connecting to Partner A's MLflow server across two machines, and confirming
  I was actually pointed at her server and not my own


The ai usage saved a lot of time in fixing problems and doing the rote work like setting up aws.