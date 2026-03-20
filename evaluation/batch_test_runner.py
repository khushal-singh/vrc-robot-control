import os
import csv
import sys
from collections import defaultdict

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from asr_module.asr_engine import transcribe
from intent_module.intent_mapper import map_intent

COMMAND_MAP = {
    "moveforward":  "move forward",
    "movebackward": "move backward",
    "turnleft":     "turn left",
    "turnright":    "turn right",
    "stop":         "stop",
}

INTENT_TO_COMMAND = {
    "MOVE_FORWARD":  "move forward",
    "MOVE_BACKWARD": "move backward",
    "TURN_LEFT":     "turn left",
    "TURN_RIGHT":    "turn right",
    "STOP":          "stop",
    "NO_COMMAND":    "",
}


def get_expected(filename):
    """
    Parse expected label from filename.

    Handles both formats:
      Noisy:  speaker1_MoveForward_snr20db.wav  → 'move forward'
      Clean:  speaker1_MoveForward.wav          → 'move forward'

    Command is always at index 1 after splitting on '_'.
    """
    base  = filename.replace(".wav", "")
    parts = base.split("_")

    if len(parts) >= 2:
        command_raw = parts[1].lower()
        return COMMAND_MAP.get(command_raw, command_raw)

    return base.lower()


def get_condition(filename):
    """
    speaker1_MoveForward_snr20db.wav → 'SNR_20dB'
    speaker1_MoveForward_snr0db.wav  → 'SNR_0dB'
    speaker1_MoveForward.wav         → 'clean'
    """
    base = filename.replace(".wav", "").lower()
    if "snr" not in base:
        return "clean"
    db_value = base.split("snr")[-1].replace("db", "")
    return f"SNR_{db_value}dB"


def get_speaker(filename):
    """speaker1_MoveForward_snr20db.wav → 'speaker1'"""
    return filename.split("_")[0]


def run_batch(audio_dir, output_csv):
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)

    files = sorted([f for f in os.listdir(audio_dir) if f.endswith(".wav")])

    if not files:
        print(f"No WAV files found in: {audio_dir}")
        return

    results = []

    for fname in files:
        path      = os.path.join(audio_dir, fname)
        expected  = get_expected(fname)
        condition = get_condition(fname)
        speaker   = get_speaker(fname)

        # ── Full pipeline: ASR → intent mapper → command ──────────────────
        result        = transcribe(path)
        intent_result = map_intent(result["text"], result["confidence"])

        predicted  = INTENT_TO_COMMAND.get(intent_result["intent"], "")
        confidence = intent_result["confidence"]
        latency    = result["latency"]
        correct    = (predicted == expected)

        results.append({
            "filename":   fname,
            "speaker":    speaker,
            "condition":  condition,
            "expected":   expected,
            "predicted":  predicted,
            "correct":    correct,
            "confidence": confidence,
            "latency_s":  latency,
        })

        status = "OK  " if correct else "FAIL"
        print(f"[{status}] {fname}")
        print(f"       expected : '{expected}'")
        print(f"       got      : '{predicted}'  conf={confidence}  latency={latency}s")

    # ── Write CSV ─────────────────────────────────────────────────────────────
    with open(output_csv, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    # ── Summary ───────────────────────────────────────────────────────────────
    total         = len(results)
    correct_count = sum(1 for r in results if r["correct"])
    accuracy      = round(correct_count / total * 100, 1)

    by_condition = defaultdict(list)
    by_speaker   = defaultdict(list)
    by_command   = defaultdict(list)

    for r in results:
        by_condition[r["condition"]].append(r["correct"])
        by_speaker[r["speaker"]].append(r["correct"])
        by_command[r["expected"]].append(r["correct"])

    print("\n" + "=" * 55)
    print("OVERALL SUMMARY")
    print("=" * 55)
    print(f"  Total files tested : {total}")
    print(f"  Correct            : {correct_count}")
    print(f"  Overall Accuracy   : {accuracy}%")

    print("\n── Per Noise Condition ──────────────────────────────")
    for cond in sorted(by_condition):
        res = by_condition[cond]
        acc = round(sum(res) / len(res) * 100, 1)
        print(f"  {cond:12s}  {sum(res):3d}/{len(res):3d}  =  {acc}%")

    print("\n── Per Speaker ──────────────────────────────────────")
    for spk in sorted(by_speaker):
        res = by_speaker[spk]
        acc = round(sum(res) / len(res) * 100, 1)
        print(f"  {spk:10s}  {sum(res):3d}/{len(res):3d}  =  {acc}%")

    print("\n── Per Command ──────────────────────────────────────")
    for cmd in sorted(by_command):
        res = by_command[cmd]
        acc = round(sum(res) / len(res) * 100, 1)
        print(f"  {cmd:15s}  {sum(res):3d}/{len(res):3d}  =  {acc}%")

    latencies = [r["latency_s"] for r in results]
    print("\n── Latency (seconds) ────────────────────────────────")
    print(f"  Mean : {round(sum(latencies) / len(latencies), 2)}s")
    print(f"  Min  : {round(min(latencies), 2)}s")
    print(f"  Max  : {round(max(latencies), 2)}s")

    print(f"\n  Results saved → {output_csv}")
    print("=" * 55)


if __name__ == "__main__":
    # ── Run noisy (augmented) dataset ─────────────────────────────────────────
    run_batch(
        audio_dir="audio_dataset/augmented",
        output_csv="evaluation/results/processed_metrics.csv"
    )

    # ── Run clean dataset ─────────────────────────────────────────────────────
    run_batch(
        audio_dir="audio_dataset/clean_flat",
        output_csv="evaluation/results/clean_metrics.csv"
    )