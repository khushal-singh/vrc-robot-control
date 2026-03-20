from .states import States
from .confirmation_logic import ConfirmationManager

# CHANGED 0.45 -> 0.40 to match intent_mapper.py
CONFIDENCE_THRESHOLD = 0.40


class StateMachine:

    def __init__(self):
        self.state = States.IDLE
        self.pending_command = None
        self.confirmation = ConfirmationManager()

    def receive_command(self, intent, confidence):

        if intent == "NO_COMMAND":
            return None

        if confidence < CONFIDENCE_THRESHOLD:
            print(f"Command rejected: confidence {confidence} below threshold {CONFIDENCE_THRESHOLD}")
            return None

        if intent == "STOP" and confidence > 0.9:
            print("Emergency STOP executed")
            self.pending_command = None
            self.state = States.IDLE
            return "STOP"

        if self.state == States.IDLE:
            self.pending_command = intent
            self.state = States.WAITING_CONFIRMATION
            self.confirmation.start_timer()
            print(f"Confirm command: {intent}?")
            return None

    def receive_confirmation(self, text):

        if self.state != States.WAITING_CONFIRMATION:
            return None

        if self.confirmation.is_timeout():
            print("Confirmation timeout")
            self.pending_command = None
            self.state = States.IDLE
            return None

        if text == "yes":
            self.state = States.EXECUTING
            command = self.pending_command
            print(f"Executing command: {command}")
            self.pending_command = None
            self.state = States.IDLE
            return command

        if text == "no":
            print("Command cancelled")
            self.pending_command = None
            self.state = States.IDLE
            return None