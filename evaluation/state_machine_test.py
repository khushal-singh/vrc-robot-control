import sys
import os
import time

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from intent_module.state_machine.transitions import StateMachine


def run_safety_test():
    tests = [
        ("Normal flow — confirm yes",  "MOVE_FORWARD",  0.85, "yes",     "MOVE_FORWARD"),
        ("Normal flow — confirm no",   "TURN_LEFT",     0.85, "no",      None),
        ("Emergency STOP high conf",   "STOP",          0.95, None,      "STOP"),
        ("Low confidence rejected",    "MOVE_BACKWARD", 0.30, None,      None),
        ("Timeout — no confirmation",  "TURN_RIGHT",    0.85, "timeout", None),
    ]

    passed = 0
    print("\n── State Machine Safety Tests ───────────────────────")

    for desc, intent, conf, confirm, expected in tests:
        sm = StateMachine()
        result = sm.receive_command(intent, conf)

        if confirm == "timeout":
            # Advance the clock past the 5-second window by patching start_time,
            # then call receive_confirmation — the state machine must reject it.
            sm.confirmation.start_time = time.time() - 6
            result = sm.receive_confirmation("yes")  # "yes" arrives too late

        elif confirm is not None:
            # Normal yes/no confirmation
            if result is None:
                result = sm.receive_confirmation(confirm)

        ok     = (result == expected)
        passed += (1 if ok else 0)
        status = "PASS" if ok else "FAIL"
        print(f"  [{status}] {desc}")
        print(f"         expected={expected}  got={result}")

    print(f"\n── Summary ──────────────────────────────────────────")
    print(f"  Tests passed      : {passed}/{len(tests)}")
    print(f"  Safe execution    : {passed / len(tests) * 100:.0f}%  (target: 100%)")


if __name__ == "__main__":
    run_safety_test()