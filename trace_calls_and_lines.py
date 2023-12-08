import os.path
import sys


def trace_call(frame, event, arg):
    print("calling {} in {} at line {:d}".format(
        frame.f_code.co_name,
        os.path.basename(frame.f_code.co_filename),
        frame.f_lineno))
    return trace_local_events


def trace_local_events(frame, event, arg):
    if event == "line":
        print("line {} in {}".format(
            frame.f_lineno,
            frame.f_code.co_name
        ))


def f():
    pass


def g():
    f()


def h():
    g()


if __name__ == '__main__':
    sys.settrace(trace_call)
    h()
