def test_arithmetic_progression():
    acc = 0
    for i in range(1000):
        acc += i
    assert acc == 1000 * 999 // 2
