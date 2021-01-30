import string


def sax(ts, size):
    assert len(ts) % size == 0, f"cannot split provided time series of length {len(ts)} in {size} equal parts"
    assert size <= len(string.ascii_lowercase), "alphabet exhausted"
    paa_ts = []
    sax_ts = []
    ts = list(ts)
    alphabet = list(string.ascii_lowercase)
    ratio = size / len(ts)
    for ts_i in range(1, size + 1):
        char = alphabet.pop(0)
        for _ in range(int(len(ts) / size)):
            paa_ts.append(ratio * sum([ts[i] for i in _range_for_frame(ts_i, ts, size)]))
            sax_ts.append(char)
    return sax_ts, paa_ts


def _range_for_frame(i, ts, size):
    start = int(len(ts) / size * (i - 1) + 1)
    end = int(len(ts) / size * i)
    return range(start - 1, end)
