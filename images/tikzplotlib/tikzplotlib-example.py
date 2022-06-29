#!/usr/bin/env python3

import itertools

import matplotlib.pyplot as plt
import numpy as np
import tikzplotlib

# Adapted from a Robotics I homework.


def pairwise(iterable):
    a, b = itertools.tee(iterable)
    next(b, None)
    return zip(a, b)


def speed_dist(t, T, tau):
    return -2 / T**3 * t**3 + 3 / T**2 * t**2


def speed_dist_old(t, T, tau):
    return np.piecewise(
        t,
        [t <= tau, tau < t < (T - tau), (T - tau) <= t < T, t >= T],
        [
            (1 / (T - tau) / tau) * t**2 / 2,
            (1 / (T - tau)) * (t - tau) + (1 / (T - tau) / tau) * tau**2 / 2,
            1 - (1 / (T - tau) / tau) * (tau - (t - (T - tau))) ** 2 / 2,
            1,
        ],
    )


def main() -> None:
    T = 10
    tau = 2
    step = 0.01
    interval = np.arange(0.0, T, step)
    pseudo_derivative_old = [
        (speed_dist_old(t2, T, tau) - speed_dist_old(t1, T, tau)) / step
        for t1, t2 in pairwise(list(interval))
    ]
    pseudo_derivative_new = [
        (speed_dist(t2, T, tau) - speed_dist(t1, T, tau)) / step
        for t1, t2 in pairwise(list(interval))
    ]
    plt.plot(
        interval[:-2], [(b - a) / step for a, b in pairwise(pseudo_derivative_old)]
    )
    plt.plot(
        interval[:-2], [(b - a) / step for a, b in pairwise(pseudo_derivative_new)]
    )
    plt.savefig("tpl-example.png")
    tikzplotlib.save("tpl-example.tex")
    plt.clf()


if __name__ == "__main__":
    main()
