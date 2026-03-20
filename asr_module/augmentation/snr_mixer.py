import numpy as np
import soundfile as sf
import os


def mix_noise(clean_path, noise_path, output_path, snr_db):
    clean, sr = sf.read(clean_path)
    noise, _ = sf.read(noise_path)

    # Convert to mono if stereo
    if len(clean.shape) > 1:
        clean = clean.mean(axis=1)
    if len(noise.shape) > 1:
        noise = noise.mean(axis=1)

    if len(noise) < len(clean):
        noise = np.tile(noise, int(np.ceil(len(clean) / len(noise))))
    noise = noise[:len(clean)]

    clean_power = np.mean(clean ** 2)
    noise_power = np.mean(noise ** 2)
    snr_linear  = 10 ** (snr_db / 10)
    noise_scaled = noise * np.sqrt(clean_power / (snr_linear * noise_power + 1e-9))

    mixed = clean + noise_scaled
    mixed = mixed / (np.max(np.abs(mixed)) + 1e-9)
    sf.write(output_path, mixed, sr)
    print(f"Saved: {output_path} at SNR {snr_db}dB")


def augment_dataset(clean_dir, noise_file, output_dir, snr_levels=[20, 10, 0]):
    """
    Walks clean_dir/speakerN/Command.wav and produces:
        output_dir/speakerN_Command_snrXdb.wav

    Output filename format (must match batch_test_runner.get_expected):
        speakerN_CommandName_snrXdb.wav
        e.g. speaker1_MoveForward_snr20db.wav
    """
    os.makedirs(output_dir, exist_ok=True)

    # ── Remove stale files from old naming conventions ────────────────────────
    removed = 0
    for f in os.listdir(output_dir):
        if f.startswith("Speaker_") and f.endswith(".wav"):
            os.remove(os.path.join(output_dir, f))
            removed += 1
    if removed:
        print(f"Removed {removed} old-format Speaker_ files from '{output_dir}'")

    # ── Generate fresh augmented files ───────────────────────────────────────
    total = 0
    for speaker in sorted(os.listdir(clean_dir)):
        speaker_path = os.path.join(clean_dir, speaker)
        if not os.path.isdir(speaker_path):
            continue
        for fname in sorted(os.listdir(speaker_path)):
            if not fname.endswith(".wav"):
                continue
            clean_path    = os.path.join(speaker_path, fname)
            command_stem  = fname.replace(".wav", "")  # e.g. 'MoveForward'
            for snr in snr_levels:
                # e.g. speaker1_MoveForward_snr20db.wav
                out_name = f"{speaker}_{command_stem}_snr{snr}db.wav"
                out_path = os.path.join(output_dir, out_name)
                mix_noise(clean_path, noise_file, out_path, snr)
                total += 1

    print(f"\nDone. {total} augmented files written to '{output_dir}'")


if __name__ == "__main__":
    augment_dataset(
        clean_dir="audio_dataset/clean",
        noise_file="audio_dataset/noise/background.wav",
        output_dir="audio_dataset/augmented"
    )