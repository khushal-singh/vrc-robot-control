import numpy as np
import soundfile as sf

def normalize(wav_path, output_path, target_sr=16000):
    data, sr = sf.read(wav_path)
    if len(data.shape) > 1:
        data = data.mean(axis=1)  # stereo to mono
    data = data / (np.max(np.abs(data)) + 1e-9)
    sf.write(output_path, data, target_sr)
    print(f"Saved normalized audio to {output_path}")
    return output_path