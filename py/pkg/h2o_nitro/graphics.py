import random


def remap(f, dmin, dmax, rmin, rmax):
    return (f - dmin) / (dmax - dmin) * (rmax - rmin) + rmin


def random_walk(n, rmin=.05, rmax=.95):
    data = [random.uniform(-1, 1)]
    for i in range(1, n):
        data.append(data[i - 1] + random.uniform(-1, 1))
    dmin, dmax = min(data), max(data)
    return [remap(d, dmin, dmax, rmin, rmax) for d in data]  # normalize
