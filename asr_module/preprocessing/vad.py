import numpy as np
import soundfile as sf

def trim_silence(wav_path, output_path, threshold=0.01, frame_ms=20):
    data, sr = sf.read(wav_path)
    frame_size = int(sr * frame_ms / 1000)
    frames = [data[i:i+frame_size] for i in range(0, len(data), frame_size)]
    active = [f for f in frames if np.sqrt(np.mean(f**2)) > threshold]
    trimmed = np.concatenate(active) if active else data
    sf.write(output_path, trimmed, sr)
    print(f"Saved trimmed audio to {output_path}")
    return output_path