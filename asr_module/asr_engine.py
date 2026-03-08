import time
import json
import math
import re
from faster_whisper import WhisperModel

model = WhisperModel("base", device="cpu", compute_type="int8")

def transcribe(wav_path):
    start = time.time()
    segments, _ = model.transcribe(wav_path, language="en")
    segments = list(segments)
    latency = round(time.time() - start, 2)

    text = " ".join([s.text.strip() for s in segments]).lower()
    text = re.sub(r'[^\w\s]', '', text).strip()

    confidence = 0.0
    if segments:
        avg_logprob = sum([s.avg_logprob for s in segments]) / len(segments)
        confidence = round(min(1.0, math.exp(avg_logprob)), 3)

    return {"text": text, "confidence": confidence, "latency": latency}

if __name__ == "__main__":
    import sys
    wav = sys.argv[1] if len(sys.argv) > 1 else "test.wav"
    print(json.dumps(transcribe(wav), indent=2))
