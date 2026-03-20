import csv
import os


def analyze(csv_path="evaluation/results/processed_metrics.csv"):
    if not os.path.exists(csv_path):
        print(f"CSV not found: {csv_path}")
        return

    rows = list(csv.DictReader(open(csv_path)))
    if not rows:
        print("No data found in CSV.")
        return

    # Aligned to actual operational threshold in intent_mapper.py / transitions.py
    THRESHOLD = 0.40

    total = len(rows)
    above = [r for r in rows if float(r['confidence']) >= THRESHOLD]
    below = [r for r in rows if float(r['confidence']) <  THRESHOLD]

    above_correct = sum(1 for r in above if r['correct'] == 'True')
    below_correct = sum(1 for r in below if r['correct'] == 'True')

    passed  = len(above)
    blocked = len(below)

    print(f"\n── Confidence Threshold Analysis (threshold={THRESHOLD}) ───")
    print(f"  Total predictions     : {total}")
    print(f"  Passed  (conf >= {THRESHOLD}): {passed:4d}  ({passed  / total * 100:.1f}%)")
    print(f"  Blocked (conf <  {THRESHOLD}): {blocked:4d}  ({blocked / total * 100:.1f}%)")

    print(f"\n── Accuracy within each group ───────────────────────")
    if above:
        print(f"  Conf >= {THRESHOLD}: {above_correct:3d}/{len(above):3d} correct  = {above_correct / len(above) * 100:.1f}%")
    if below:
        print(f"  Conf <  {THRESHOLD}: {below_correct:3d}/{len(below):3d} correct  = {below_correct / len(below) * 100:.1f}%")

    confidences = [float(r['confidence']) for r in rows]
    buckets = [(0.0, 0.25), (0.25, 0.40), (0.40, 0.50), (0.50, 0.75), (0.75, 1.01)]
    print(f"\n── Confidence Distribution ──────────────────────────")
    for lo, hi in buckets:
        bucket_rows = [r for r in rows if lo <= float(r['confidence']) < hi]
        correct_in  = sum(1 for r in bucket_rows if r['correct'] == 'True')
        label = f"[{lo:.2f}, {hi:.2f})"
        marker = " <- operational threshold" if lo == 0.40 else ""
        if bucket_rows:
            print(f"  {label}  {len(bucket_rows):4d} predictions  {correct_in:3d} correct  ({correct_in/len(bucket_rows)*100:.1f}%){marker}")
        else:
            print(f"  {label}  0 predictions{marker}")

    print(f"\n  Mean conf: {sum(confidences)/len(confidences):.3f}  "
          f"Min: {min(confidences):.3f}  Max: {max(confidences):.3f}")


if __name__ == "__main__":
    analyze()