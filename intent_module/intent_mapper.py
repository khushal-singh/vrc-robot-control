from intent_module.fuzzy_matcher import match_command

CONFIDENCE_THRESHOLD = 0.75


def map_intent(asr_text, asr_confidence):

    command, score = match_command(asr_text)

    final_confidence = min(score, asr_confidence)

    if final_confidence < CONFIDENCE_THRESHOLD:
        return {
            "intent": "NO_COMMAND",
            "confidence": final_confidence
        }

    intent = command.upper().replace(" ", "_")

    return {
        "intent": intent,
        "confidence": final_confidence
    }
