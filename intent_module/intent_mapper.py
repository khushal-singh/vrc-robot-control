from intent_module.fuzzy_matcher import match_command

# CHANGED 0.45 -> 0.40
# In the original run, many SNR 0dB failures had correct transcriptions
# blocked by the 0.45 threshold (e.g. conf=0.438, 0.431, 0.445).
# Lowering to 0.40 recovers those while still blocking genuine noise
# outputs which cluster below 0.40.
# transitions.py must stay in sync with this value.
CONFIDENCE_THRESHOLD = 0.40


def map_intent(asr_text, asr_confidence):

    command, score = match_command(asr_text)
    final_confidence = min(score, asr_confidence)

    if final_confidence < CONFIDENCE_THRESHOLD:
        return {"intent": "NO_COMMAND", "confidence": final_confidence}

    intent = command.upper().replace(" ", "_")
    return {"intent": intent, "confidence": final_confidence}