import time
import json
import math
import re
import tempfile
import os
from faster_whisper import WhisperModel
from asr_module.preprocessing.vad import trim_silence
from asr_module.preprocessing.normalize import normalize


model = WhisperModel("small", device="cpu", compute_type="int8")


def normalize_text(text: str) -> str:
    """Fix known Whisper transcription quirks."""
    text = re.sub(r'\bmove backwards\b', 'move backward', text)
    text = re.sub(r'\bbackwards\b',      'backward',      text)
    text = re.sub(r'\bforwards\b',       'forward',       text)

    if len(text.split()) <= 5:
        text = re.sub(r'\bnew backward\b',  'move backward', text)
        text = re.sub(r'\bblue forward\b',  'move forward',  text)
        text = re.sub(r'\bsun left\b',      'turn left',     text)
        text = re.sub(r'\bsun rate\b',      'turn right',    text)
        text = re.sub(r'\bdone left\b',     'turn left',     text)
        text = re.sub(r'\bon left\b',       'turn left',     text)
        text = re.sub(r'\bthen left\b',     'turn left',     text)
        text = re.sub(r'\bthen write\b',    'turn right',    text)
        text = re.sub(r'\bturn light\b',    'turn right',    text)

    return text


def transcribe(wav_path):
    start = time.time()

    with tempfile.TemporaryDirectory() as tmp:
        norm_path = os.path.join(tmp, "norm.wav")
        vad_path  = os.path.join(tmp, "vad.wav")
        normalize(wav_path, norm_path)
        trim_silence(norm_path, vad_path)

        segments, _ = model.transcribe(
            vad_path,
            language="en",
            beam_size=5,
            condition_on_previous_text=False,
            no_speech_threshold=0.3,
            log_prob_threshold=-2.0,
            # ONLY NEW PARAMETER: primes Whisper's decoder toward the known
            # command vocabulary, reducing noise hallucinations without
            # suppressing valid short-command segments.
            initial_prompt="move forward, move backward, turn left, turn right, stop",
        )
        segments = list(segments)

    latency = round(time.time() - start, 2)

    text = " ".join([s.text.strip() for s in segments]).lower()
    text = re.sub(r'[^\w\s]', '', text).strip()
    text = normalize_text(text)

    confidence = 0.0
    if segments:
        avg_logprob = sum([s.avg_logprob for s in segments]) / len(segments)
        confidence = round(min(1.0, math.exp(avg_logprob)), 3)

    return {"text": text, "confidence": confidence, "latency": latency}


if __name__ == "__main__":
    import sys
    wav = sys.argv[1] if len(sys.argv) > 1 else "test.wav"
    print(json.dumps(transcribe(wav), indent=2))