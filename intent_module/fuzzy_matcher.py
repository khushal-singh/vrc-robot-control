from rapidfuzz import process
from intent_module.vocabulary import COMMANDS

# CHANGED 60 -> 75 to prevent marginal fuzzy matches like
# "turn light" -> "turn right" (score ~67) from producing wrong commands.
THRESHOLD = 75


def match_command(text):
    result = process.extractOne(text, COMMANDS)

    if result is None:
        return "NO_COMMAND", 0.0

    command, score, _ = result

    if score >= THRESHOLD:
        return command, score / 100
    else:
        return "NO_COMMAND", score / 100