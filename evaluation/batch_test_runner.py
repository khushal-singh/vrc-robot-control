import os
import csv
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from asr_module.asr_engine import transcribe

COMMAND_MAP = {
    "moveforward": "move forward",
    "movebackward": "move backward",
    "turnleft": "turn left",
    "turnright": "turn right",
    "stop": "stop"
}

def get_expected(filename):
    base = filename.split("_snr")[0].split("_speaker")[0]
    return COMMAND_MAP.get(base.lower(), base.lower())

def run_batch(audio_dir, output_csv):
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    results = []
    files = [f for f in os.listdir(audio_dir) if f.endswith(".wav")]

    for fname in sorted(files):
        path = os.path.join(audio_dir, fname)
        expected = get_expected(fname)
        result = transcribe(path)
        predicted = result["text"].strip().lower()
        confidence = result["confidence"]
        latency = result["latency"]
        correct = predicted == expected
        condition = "clean" if "snr" not in fname else fname.split("_snr")[1].replace(".wav","") + "dB"

        results.append({
            "filename": fname,
            "expected": expected,
            "predicted": predicted,
            "confidence": confidence,
            "latency": latency,
            "correct": correct,
            "condition": condition
        })
        print(f"[{'OK' if correct else 'FAIL'}] {fname}")
        print(f"      expected: '{expected}' | got: '{predicted}' | conf: {confidence} | latency: {latency}s")

    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    total = len(results)
    correct_count = sum(1 for r in results if r["correct"])
    print(f"\n--- SUMMARY ---")
    print(f"Total files tested : {total}")
    print(f"Correct            : {correct_count}")
    print(f"Accuracy           : {round(correct_count/total*100, 1)}%")
    print(f"Results saved to   : {output_csv}")

if __name__ == "__main__":
    run_batch(
        audio_dir="audio_dataset/augmented",
        output_csv="evaluation/results/processed_metrics.csv"
    )
