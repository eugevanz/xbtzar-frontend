import numpy as np


def directional_change(close: np.ndarray, high: np.ndarray, low: np.ndarray, sigma: float) -> tuple:
    up_zig = True  # Last extreme is a bottom. Next is top
    tmp_max, tmp_min = high[0], low[0]
    tmp_max_i, tmp_min_i = 0, 0
    tops, bottoms = [], []
    length = len(close)

    for i in range(length):
        if up_zig:  # Last extreme is a bottom
            if high[i] > tmp_max:
                tmp_max, tmp_max_i = high[i], i
            else:  # close[i] >= tmp_max - tmp_max * sigma
                if close[i] < tmp_max - tmp_max * sigma:  # Price retraced by sigma%
                    tops.append([i, tmp_max_i, tmp_max])  # Record it
                    up_zig = False  # Setup for next bottom
                    tmp_min, tmp_min_i = low[i], i
        else:  # Last extreme is a top
            if low[i] < tmp_min:
                tmp_min, tmp_min_i = low[i], i
            else:  # close[i] <= tmp_min + tmp_min * sigma
                if close[i] > tmp_min + tmp_min * sigma:  # Price retraced by sigma%
                    bottoms.append([i, tmp_min_i, tmp_min])  # Record it
                    up_zig = True  # Setup for next bottom
                    tmp_max, tmp_max_i = high[i], i

    return tops, bottoms
