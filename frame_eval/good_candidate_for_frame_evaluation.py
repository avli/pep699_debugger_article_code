def f():
    res = 0
    for i in range(100_000):
        res += i
    # Debugger logic will be injected here!
    return res  # breakpoint


if __name__ == '__main__':
    f()
