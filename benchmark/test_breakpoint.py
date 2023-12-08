import timeit
import sys


def foo():
    for i in range(100_000):
        if i == 50_000:
            pass  # Put breakpoint here


print("No debug")

print(timeit.timeit(foo, number=100))

DEBUGGER_ID = sys.monitoring.DEBUGGER_ID

print("PEP 669")

break_count = 0


def pep_669_breakpoint(code, line):
    global break_count
    if line == 8:
        break_count += 1
    else:
        return sys.monitoring.DISABLE

sys.monitoring.use_tool_id(DEBUGGER_ID, 'debugger')
sys.monitoring.register_callback(DEBUGGER_ID, sys.monitoring.events.LINE,
                                 pep_669_breakpoint)
sys.monitoring.set_local_events(DEBUGGER_ID, foo.__code__,
                                sys.monitoring.events.LINE)

print(timeit.timeit(foo, number=100))

sys.monitoring.set_local_events(DEBUGGER_ID, foo.__code__, 0)

print("Break point hit", break_count, "times")

break_count = 0
# Use sys.settrace, this is about as fast as a sys.settrace debugger can be if written in Python.

print("sys.settrace")

foo_code = foo.__code__


def sys_settrace_breakpoint(frame, event, arg):
    global break_count
    if frame.f_code is not foo_code:
        return None
    if event == "line" and frame.f_lineno == 8:
        break_count += 1
    return sys_settrace_breakpoint


sys.settrace(sys_settrace_breakpoint)

print(timeit.timeit(foo, number=100))

sys.settrace(None)

print("Break point hit", break_count, "times")