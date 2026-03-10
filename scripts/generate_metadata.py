import os
import csv
import soundfile as sf

clean_dir = "audio_dataset/clean"
augmented_dir = "audio_dataset/augmented"
output_csv = "audio_dataset/metadata.csv"

rows = []

for fname in os.listdir(clean_dir):
    if fname.endswith(".wav"):
        path = os.path.join(clean_dir, fname)
        data, sr = sf.read(path)
        duration = round(len(data) / sr, 2)
        command = fname.replace(".wav", "").lower()
        rows.append([fname, "clean", command, sr, duration])

for fname in os.listdir(augmented_dir):
    if fname.endswith(".wav"):
        path = os.path.join(augmented_dir, fname)
        data, sr = sf.read(path)
        duration = round(len(data) / sr, 2)
        command = fname.split("_snr")[0].lower()
        snr = fname.split("_snr")[1].replace("db.wav", "") + "dB"
        rows.append([fname, f"augmented_{snr}", command, sr, duration])

with open(output_csv, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["filename", "condition", "command", "sample_rate", "duration_sec"])
    writer.writerows(rows)

print(f"metadata.csv written with {len(rows)} entries")
