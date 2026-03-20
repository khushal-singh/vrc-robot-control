import numpy as np
import soundfile as sf

def normalize(wav_path, output_path, target_sr=16000):
    data, sr = sf.read(wav_path)

    # Convert stereo to mono
    if len(data.shape) > 1:
        data = data.mean(axis=1)

    # Resample if needed using scipy (reliable, no numba dependency)
    if sr != target_sr:
        from scipy.signal import resample_poly
        import math
        gcd = math.gcd(target_sr, sr)
        data = resample_poly(data, target_sr // gcd, sr // gcd)

    # Amplitude normalisation
    data = data / (np.max(np.abs(data)) + 1e-9)
    sf.write(output_path, data, target_sr)
    return output_path