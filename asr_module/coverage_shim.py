import coverage

# Minimal coverage.types implementation so numba.misc.coverage_support
# can import without crashing. These are only used for type hints.
ATTR_NAMES = [
    "TTraceData",
    "TShouldTraceFn",
    "TFileDisposition",
    "TShouldStartContextFn",
    "TWarnFn",
]

class _DummyTracer:
    def start(self): pass
    def stop(self): pass

class _Types:
    Tracer = _DummyTracer

# If coverage.types doesn't exist, create it with all attributes.
if not hasattr(coverage, "types"):
    for name in ATTR_NAMES:
        setattr(_Types, name, object)
    coverage.types = _Types()
else:
    # Patch any missing attributes on existing coverage.types
    for name in ATTR_NAMES:
        if not hasattr(coverage.types, name):
            setattr(coverage.types, name, object)
