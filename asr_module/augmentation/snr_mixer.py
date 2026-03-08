import numpy as np
import soundfile as sf
import os

def mix_noise(clean_path, noise_path, output_path, snr_db):
    clean, sr = sf.read(clean_path)
    noise, _ = sf.read(noise_path)

    if len(noise) < len(clean):
        noise = np.tile(noise, int(np.ceil(len(clean) / len(noise))))
    noise = noise[:len(clean)]

    clean_power = np.mean(clean ** 2)
    noise_power = np.mean(noise ** 2)
    snr_linear = 10 ** (snr_db / 10)
    noise_scaled = noise * np.sqrt(clean_power / (snr_linear * noise_power + 1e-9))

    mixed = clean + noise_scaled
    mixed = mixed / (np.max(np.abs(mixed)) + 1e-9)
    sf.write(output_path, mixed, sr)
    print(f"Saved: {output_path} at SNR {snr_db}dB")

def augment_dataset(clean_dir, noise_file, output_dir, snr_levels=[20, 10, 0]):
    os.makedirs(output_dir, exist_ok=True)
    for fname in os.listdir(clean_dir):
        if fname.endswith(".wav"):
            clean_path = os.path.join(clean_dir, fname)
            for snr in snr_levels:
                out_name = fname.replace(".wav", f"_snr{snr}db.wav")
                out_path = os.path.join(output_dir, out_name)
                mix_noise(clean_path, noise_file, out_path, snr)

if __name__ == "__main__":
    augment_dataset(
        clean_dir="audio_dataset/clean",
        noise_file="audio_dataset/noise/background.wav",
        output_dir="audio_dataset/augmented"
    )
