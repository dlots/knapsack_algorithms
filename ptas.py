import itertools


WEIGHT = 0
VALUE = 1


def not_in_m(capacity, n, items, m_subset, comparisons):
    total_value = 0
    subset_weight = 0
    for item_index in m_subset:
        subset_weight += items[item_index][WEIGHT]
    remaining_capacity = capacity - subset_weight
    knapsack = []
    for item_index in range(n):
        comparisons += 1
        if item_index not in m_subset and items[item_index][WEIGHT] <= remaining_capacity:
            total_value += items[item_index][VALUE]
            remaining_capacity -= items[item_index][WEIGHT]
            knapsack.append(item_index)
    return total_value, knapsack


def sahni_ptas(capacity, items, k=3):
    comparisons = 0
    knapsack_value = 0
    knapsack = []
    n = len(items)
    subsets = itertools.combinations(range(n), k)
    m_subsets = []
    for subset in subsets:
        comparisons += 1
        if sum([items[item_index][WEIGHT] for item_index in subset]) <= capacity:
            m_subsets.append(subset)
    for m_subset in m_subsets:
        not_in_m_value, not_in_m_knapsack = not_in_m(capacity, n, items, m_subset, comparisons)
        sample_value = not_in_m_value + sum([items[item_index][VALUE] for item_index in m_subset])
        comparisons += 1
        if sample_value > knapsack_value:
            knapsack_value = sample_value
            knapsack = not_in_m_knapsack + list(m_subset)
    return knapsack_value, sorted(knapsack), comparisons


if __name__ == '__main__':
    cap = 10
    items_list = [(1,1),(2,2),(3,3),(3,4),(2,5),(1,6)]
    print(sahni_ptas(cap, items_list, 5))
