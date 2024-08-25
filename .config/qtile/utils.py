def calc_center(h: float):
    assert h > 0 and h <= 1
    remaining_space = 1 - h
    remaining_space = remaining_space / 2
    return remaining_space
