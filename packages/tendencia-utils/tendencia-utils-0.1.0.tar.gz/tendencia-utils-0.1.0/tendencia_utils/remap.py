
def trend_remap(slope, p) -> int:
    if p <= 0.01 and slope <= 0:
        return 1
    elif 0.01 < p and p <= 0.05 and slope <= 0:
        return 2
    elif 0.05 < p and slope <= 0:
        return 3
    elif p <= 0.01 and slope > 0:
        return 6
    elif 0.01 < p and p <= 0.05 and slope > 0:
        return 5
    elif 0.05 < p and slope > 0:
        return 4
    else:
        return 0


def pearsonr_remap(r, p) -> int:
    if p < 0.01:
        out = 1 if r < 0 else 6
    elif 0.01 <= p < 0.05:
        out = 2 if r < 0 else 5
    else:
        out = 3 if r < 0 else 4
    return out


def mk_result_remap(trend) -> int:
    data = {
        'increasing': 3,
        'decreasing': 1,
        'no trend': 2,
    }
    return data.get(trend, 0)
