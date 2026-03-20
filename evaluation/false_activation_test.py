# evaluation/false_activation_test.py
import os
import sys
import csv

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from asr_module.asr_engine import transcribe
from intent_module.intent_mapper import map_intent


def run_false_activation_test(
    oov_dir,
    output_csv="evaluation/results/false_activation.csv"
):
    files = sorted([f for f in os.listdir(oov_dir) if f.endswith(".wav")])

    if not files:
        print(f"No WAV files found in: {oov_dir}")
        return

    results = []
    false_activations = []

    for fname in files:
        path   = os.path.join(oov_dir, fname)
        asr    = transcribe(path)
        intent = map_intent(asr["text"], asr["confidence"])

        triggered = intent["intent"] != "NO_COMMAND"

        if triggered:
            false_activations.append({
                "filename":  fname,
                "asr_text":  asr["text"],
                "intent":    intent["intent"],
                "confidence": intent["confidence"],
            })

        results.append({
            "filename":        fname,
            "asr_text":        asr["text"],
            "confidence":      asr["confidence"],
            "intent":          intent["intent"],
            "false_activation": triggered,
        })

        status = "FALSE ACTIVATION" if triggered else "OK"
        print(f"[{status}] {fname} → '{asr['text']}' → {intent['intent']}")

    # ── Summary ───────────────────────────────────────────────────────────────
    total       = len(files)
    false_count = len(false_activations)
    rate        = false_count / total * 100

    print(f"\n=== FALSE ACTIVATION RATE ===")
    print(f"  Files tested      : {total}")
    print(f"  False activations : {false_count}")
    print(f"  Rate              : {rate:.1f}%  (target: <2%)")

    if false_activations:
        print(f"\n── Triggered cases ──────────────────────────────────")
        for fa in false_activations:
            print(f"  {fa['filename']}")
            print(f"    asr      : '{fa['asr_text']}'")
            print(f"    intent   : {fa['intent']}  (conf={fa['confidence']})")
    else:
        print(f"\n  No false activations — all OOV phrases correctly suppressed.")

    passed = rate < 2.0
    print(f"\n  Result : {'PASS' if passed else 'FAIL'}  (target: <2%)")

    # ── Write CSV ─────────────────────────────────────────────────────────────
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    print(f"  Results saved → {output_csv}")


if __name__ == "__main__":
    run_false_activation_test("audio_dataset/noise/oov_clips")