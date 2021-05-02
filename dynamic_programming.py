__author__ = 'dselivanovskaya'  # GitHub user name


import numpy as np


def knapsack_dp(capacity, weights, prices):
    comparisons = 0
    N = len(prices)
    A = np.zeros((N + 1, capacity + 1))
    optimal = [0] * N

    # building table A
    for i in range(N + 1):
        for w in range(capacity + 1):
            comparisons += 1
            if i == 0 or w == 0:
                A[i][w] = 0
            elif weights[i - 1] <= w:
                A[i][w] = max(A[i - 1][w], prices[i - 1] + A[i - 1][w - weights[i - 1]])
            else:
                A[i][w] = A[i - 1][w]

    # finding selected items
    n = N
    m = capacity
    while n != 0:
        if A[n][m] != A[n - 1][m]:
            optimal[n - 1] = 1
            m = m - weights[n - 1]
        n = n - 1

    return optimal, comparisons
