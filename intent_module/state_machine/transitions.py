from .states import States
from .confirmation_logic import ConfirmationManager


class StateMachine:

    def __init__(self):

        self.state = States.IDLE
        self.pending_command = None
        self.confirmation = ConfirmationManager()

    def receive_command(self, intent, confidence):

        if intent == "NO_COMMAND":
            return None

        # Emergency STOP
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

        if self.confirmation.is_timeout():

            print("Confirmation timeout")

            self.pending_command = None
            self.state = States.IDLE

            return None