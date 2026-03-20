import numpy as np
import soundfile as sf


def normalize(wav_path, output_path, target_sr=16000):
    data, sr = sf.read(wav_path)

    # Convert stereo to mono
    if len(data.shape) > 1:
        data = data.mean(axis=1)

    # Resample if the file's native sample rate differs from target.
    # Simply relabelling with sf.write(data, target_sr) when sr != target_sr
    # writes the raw samples at the wrong rate, corrupting pitch and speed.
    if sr != target_sr:
        try:
            import resampy
            data = resampy.resample(data, sr, target_sr)
        except ImportError:
            # fallback: scipy (always available with numpy ecosystem)
            from scipy.signal import resample_poly
            import math
            gcd = math.gcd(target_sr, sr)
            data = resample_poly(data, target_sr // gcd, sr // gcd)

    # Amplitude normalisation
    data = data / (np.max(np.abs(data)) + 1e-9)

    sf.write(output_path, data, target_sr)
    return output_path