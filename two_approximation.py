__author__ = 'dlots'  # GitHub user name


import numpy as np


def count_arg_sort(arr):
    length = len(arr)
    counting_array = [0 for _ in range(max(arr) + 1)]
    result_indices = [0 for _ in range(length)]
    indices = [i for i in range(length)]
    for num in arr:
        counting_array[num] += 1
    for i in range(1, len(counting_array)):
        counting_array[i] += counting_array[i - 1]
    i = length - 1
    while i >= 0:
        pos = counting_array[arr[i]] - 1
        result_indices[pos] = indices[i]
        counting_array[arr[i]] -= 1
        i -= 1
    return result_indices


def greed(capacity, weights, prices, comparisons):
    sorted_indices = count_arg_sort(prices)
    knapsack = [0 for _ in range(len(prices))]
    remaining_capacity = capacity
    profit = 0
    for i in reversed(sorted_indices):
        if weights[i] <= remaining_capacity:
            profit += prices[i]
            knapsack[i] = 1
            remaining_capacity -= weights[i]
    return profit, knapsack


def quality_greed(capacity, weights, prices, comparisons):
    quality = [round(prices[i]/weights[i]) for i in range(len(prices))]
    sorted_indices = count_arg_sort(quality)
    knapsack = [0 for _ in range(len(prices))]
    remaining_capacity = capacity
    profit = 0
    for i in reversed(sorted_indices):
        if weights[i] <= remaining_capacity:
            profit += prices[i]
            knapsack[i] = 1
            remaining_capacity -= weights[i]
    return profit, knapsack


def two_approx(capacity, weights, prices):
    comparisons = None
    g_cost, g_knapsack = greed(capacity, weights, prices, comparisons)
    qg_cost, qg_knapsack = quality_greed(capacity, weights, prices, comparisons)
    if g_cost > qg_cost:
        return g_knapsack, comparisons
    else:
        return qg_knapsack, comparisons


if __name__ == '__main__':
    a = [3,2,1,4,5]
    print(count_arg_sort(a))
