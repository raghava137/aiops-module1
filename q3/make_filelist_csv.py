"""
AIOps Module 1 - Question 3
Builds a CSV manifest of every image file under data/.

v1 (data.zip only)             -> 1800 rows + header = 1801 lines
v2 (data.zip + new-labels.zip) -> 2800 rows + header = 2801 lines

Rows are sorted by relative path so the same input always produces a
byte-identical file. A non-deterministic manifest would change its DVC hash on
every run, making the rollback demonstration meaningless.
"""

import argparse
import csv
import os

IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".bmp", ".gif"}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--data-dir", default="data")
    p.add_argument("--out", default="filelist.csv")
    args = p.parse_args()

    if not os.path.isdir(args.data_dir):
        raise SystemExit(f"ERROR: '{args.data_dir}' not found.")

    rows = []
    for dirpath, _dirnames, filenames in os.walk(args.data_dir):
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() not in IMAGE_EXTS:
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, args.data_dir)
            parts = rel.split(os.sep)
            rows.append({
                "filename": fn,
                "relative_path": rel.replace(os.sep, "/"),
                "split": parts[0] if len(parts) > 1 else "",
                "label": parts[1] if len(parts) > 2 else "",
                "size_bytes": os.path.getsize(full),
            })

    rows.sort(key=lambda r: r["relative_path"])

    with open(args.out, "w", newline="") as f:
        w = csv.DictWriter(
            f, fieldnames=["filename", "relative_path", "split", "label", "size_bytes"]
        )
        w.writeheader()
        w.writerows(rows)

    print(f"Wrote {args.out}")
    print(f"  data rows   : {len(rows)}")
    print(f"  total lines : {len(rows) + 1}  (including header)")

    counts = {}
    for r in rows:
        counts[(r["split"], r["label"])] = counts.get((r["split"], r["label"]), 0) + 1
    print("\n  breakdown:")
    for (split, label), n in sorted(counts.items()):
        print(f"    {split}/{label}: {n}")


if __name__ == "__main__":
    main()
