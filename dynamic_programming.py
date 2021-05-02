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
            if i == 0 or w == 0:
                comparisons += 2  # 2 comparisons
                A[i][w] = 0
            elif weights[i - 1] <= w:
                comparisons += 4  # 2 previous comparisons + 1 on this elif + 1 for max call
                A[i][w] = max(A[i - 1][w], prices[i - 1] + A[i - 1][w - weights[i - 1]])
            else:
                comparisons += 3  # comparisons from if and elif
                A[i][w] = A[i - 1][w]

    # finding selected items
    n = N
    m = capacity
    while n != 0:
        comparisons += 2  # while and if
        if A[n][m] != A[n - 1][m]:
            optimal[n - 1] = 1
            m = m - weights[n - 1]
        n = n - 1
    comparisons += 1  # 1 for last while check
    return optimal, comparisons
