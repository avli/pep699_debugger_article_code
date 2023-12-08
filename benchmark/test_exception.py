import timeit
import sys


def foo():
    for i in range(100_000):
        if i == 50_000:
            pass
    try:
        raise RuntimeError("Boom!")
    except RuntimeError:
        # Ignore.
        pass

print("No debug")

print(timeit.timeit(foo, number=100))

DEBUGGER_ID = sys.monitoring.DEBUGGER_ID

print("PEP 669")

raise_count = 0


def pep_669_exception(code, instruction_offset, exception):
    global raise_count
    raise_count += 1

sys.monitoring.use_tool_id(DEBUGGER_ID, 'debugger')
sys.monitoring.register_callback(DEBUGGER_ID, sys.monitoring.events.RAISE,
                                 pep_669_exception)
sys.monitoring.set_events(DEBUGGER_ID, sys.monitoring.events.RAISE)

print(timeit.timeit(foo, number=100))

sys.monitoring.set_local_events(DEBUGGER_ID, foo.__code__, 0)

print("Exception raised", raise_count, "times")

raise_count = 0
# Use sys.settrace, this is about as fast as a sys.settrace debugger can be if written in Python.

print("sys.settrace")

foo_code = foo.__code__


def sys_settrace_exception(frame, event, arg):
    global raise_count
    if frame.f_code is not foo_code:
        return None
    if event == "raise":
        raise_count += 1
    return sys_settrace_exception


sys.settrace(sys_settrace_exception)

print(timeit.timeit(foo, number=100))

sys.settrace(None)

print("Exception raised", raise_count, "times")