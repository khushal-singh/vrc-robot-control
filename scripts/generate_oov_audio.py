# scripts/generate_oov_audio.py
import asyncio, os, edge_tts

OOV_PHRASES = [
    "the weather is nice today",
    "please open the door",
    "hello how are you",
    "what time is it",
    "i need some water",
    "the robot is interesting",
    "can you hear me",
    "this is a test sentence",
    "Frankfurt am Main is a city",
    "artificial intelligence is advancing",
    "i would like some coffee",
    "the meeting starts at nine",
    "please close the window",
    "where is the nearest station",
    "thank you very much",
    "good morning everyone",
    "the project is almost done",
    "i am going to the lab",
    "machine learning is fascinating",
    "let me check the schedule",
]

VOICES = ["en-US-GuyNeural", "en-GB-RyanNeural", "en-IN-PrabhatNeural",
          "en-AU-WilliamNeural", "en-NG-AbeoNeural"]

async def main():
    os.makedirs("audio_dataset/noise/oov_clips", exist_ok=True)
    for i, phrase in enumerate(OOV_PHRASES):
        voice = VOICES[i % len(VOICES)]
        path = f"audio_dataset/noise/oov_clips/oov_{i+1:02d}.wav"
        await edge_tts.Communicate(phrase, voice).save(path)
        print(f"Saved: {path}")

asyncio.run(main())