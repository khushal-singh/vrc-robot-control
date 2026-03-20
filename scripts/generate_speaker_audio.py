# scripts/generate_speaker_audio.py
import asyncio
import os
import edge_tts

# 5 commands exactly matching your COMMAND_MAP
COMMANDS = {
    "MoveForward":  "move forward",
    "MoveBackward": "move backward",
    "TurnLeft":     "turn left",
    "TurnRight":    "turn right",
    "Stop":         "stop"
}

# Original 10 speakers
SPEAKERS = {
    "speaker1":  ("en-US-GuyNeural",        "American Male"),
    "speaker2":  ("en-US-JennyNeural",      "American Female"),
    "speaker3":  ("en-GB-RyanNeural",       "British Male"),
    "speaker4":  ("en-GB-SoniaNeural",      "British Female"),
    "speaker5":  ("en-IN-NeerjaNeural",     "Indian Female"),
    "speaker6":  ("en-IN-PrabhatNeural",    "Indian Male"),
    "speaker7":  ("en-AU-WilliamNeural",    "Australian Male"),
    "speaker8":  ("en-AU-NatashaNeural",    "Australian Female"),
    "speaker9":  ("en-NG-AbeoNeural",       "Nigerian Male"),
    "speaker10": ("en-IE-ConnorNeural",     "Irish Male"),
}

# 5 additional accents (speaker11-15)
NEW_SPEAKERS = {
    "speaker11": ("en-ZA-LeahNeural",       "South African Female"),
    "speaker12": ("en-ZA-LukeNeural",       "South African Male"),
    "speaker13": ("en-CA-ClaraNeural",      "Canadian Female"),
    "speaker14": ("en-CA-LiamNeural",       "Canadian Male"),
    "speaker15": ("en-NZ-MitchellNeural",   "New Zealand Male"),
}

# 5 more new accents (speaker16-20) — replaces the duplicate content
EXTRA_SPEAKERS = {
    "speaker16": ("en-SG-WayneNeural",      "Singaporean Male"),
    "speaker17": ("en-SG-LunaNeural",       "Singaporean Female"),
    "speaker18": ("en-KE-AsiliaNeural",     "Kenyan Female"),
    "speaker19": ("en-KE-ChilembaNeural",   "Kenyan Male"),
    "speaker20": ("en-PH-JamesNeural",      "Filipino Male"),
}

OUTPUT_BASE = "audio_dataset/clean"


async def generate(voice, text, output_path):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_path)
    print(f"  Saved: {output_path}")


async def generate_speakers(speakers: dict):
    for speaker_id, (voice, description) in speakers.items():
        speaker_dir = os.path.join(OUTPUT_BASE, speaker_id)

        # Skip if all 5 files already exist
        existing = [
            f for f in os.listdir(speaker_dir) if f.endswith(".wav")
        ] if os.path.isdir(speaker_dir) else []

        if len(existing) == len(COMMANDS):
            print(f"\n[SKIP] {speaker_id} ({description}) — already complete")
            continue

        os.makedirs(speaker_dir, exist_ok=True)
        print(f"\n[GEN]  {speaker_id} — {description} ({voice})")

        for filename, phrase in COMMANDS.items():
            out_path = os.path.join(speaker_dir, f"{filename}.wav")
            await generate(voice, phrase, out_path)


async def main():
    all_speakers = {**SPEAKERS, **NEW_SPEAKERS, **EXTRA_SPEAKERS}

    print("=" * 55)
    print("Generating all 20 speakers")
    print("Already complete speakers will be skipped")
    print("=" * 55)

    await generate_speakers(all_speakers)

    print("\n" + "=" * 55)
    print("Speaker map — all 20:")
    print("─" * 55)
    for sid, (voice, label) in all_speakers.items():
        print(f"  {sid:12s} → {label:30s} ({voice})")
    print("\nNext steps:")
    print("  1. Delete old augmented files:")
    print("     rm audio_dataset/augmented/*.wav")
    print("  2. Regenerate augmented:")
    print("     python3 asr_module/augmentation/snr_mixer.py")
    print("  3. Rebuild clean_flat and run evaluation:")
    print("     python3 evaluation/batch_test_runner.py")
    print("=" * 55)


if __name__ == "__main__":
    asyncio.run(main())