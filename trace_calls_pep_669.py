import os.path
import sys

DEBUGGER_ID = sys.monitoring.DEBUGGER_ID


def init_tracing():
    sys.monitoring.use_tool_id(DEBUGGER_ID, "pep669_based_debugger")
    sys.monitoring.set_events(DEBUGGER_ID, sys.monitoring.events.PY_START)


    def pep_669_py_start_trace(code, instruction_offset):
        frame = sys._getframe(1)
        print("calling {} in {} at line {:d}".format(
        code.co_name,
            os.path.basename(code.co_filename),
            frame.f_lineno))

    sys.monitoring.register_callback(
        DEBUGGER_ID,
        sys.monitoring.events.PY_START,
        pep_669_py_start_trace)


def f():
    pass


def g():
    f()


def h():
    g()


if __name__ == '__main__':
    init_tracing()
    h()
