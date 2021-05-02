# Лабораторная работа №2: Задача о рюкзаке
### 18ПМИ Богородицкая Екатерина, Сазанов Дмитрий, Селивановская Дарья


```python
import os.path as path


benchmarks_location = 'benchmarks'
file_name_template = 'p0%s_%s.txt'
indices = range(1,8)
categories = ['c', 'w', 'p', 's']
```


```python
import requests


dataset_location = 'https://people.sc.fsu.edu/~jburkardt/datasets/knapsack_01/'
for index in indices:
    for category in categories:
        filename = file_name_template % (index, category)
        r = requests.get(dataset_location + filename, allow_redirects=True)
        file = open(path.join(benchmarks_location, filename), 'wb')
        file.write(r.content)
        file.close()
```


```python
from ptas import WEIGHT, VALUE


def make_item(weight, value):
    item = [-1, -1]
    item[WEIGHT] = weight
    item[VALUE] = value
    return tuple(item)


CAPACITY = 0
ITEMS = 1
OPTIMAL = 2
dataset = []
for index in indices:
    f = open(path.join(benchmarks_location, file_name_template % (index, 'c')))
    capacity = int(f.read())
    f.close()
    f = open(path.join(benchmarks_location, file_name_template % (index, 'w')))
    weights = [int(line) for line in f.readlines()]
    f.close()
    f = open(path.join(benchmarks_location, file_name_template % (index, 'p')))
    profits = [int(line) for line in f.readlines()]
    f.close()
    f = open(path.join(benchmarks_location, file_name_template % (index, 's')))
    binary_optimal = [int(line) for line in f.readlines()]
    optimal = []
    for i in range(len(binary_optimal)):
        if binary_optimal[i] == 1:
            optimal.append(i)
    f.close()
    items = [make_item(weight=weights[i], value=profits[i]) for i in range(len(weights))]
    sample = [-1, -1, -1]
    sample[CAPACITY] = capacity
    sample[ITEMS] = items
    sample[OPTIMAL] = optimal
    dataset.append(tuple(sample))
#dataset
```


```python
from ptas import sahni_ptas; k=3 # на этом наборе данных лучше результаты получаются с k=3
from dynamic_programming import knapsack_dp
from two_approximation import two_approx
from branch_bound import Branch_and_boundary

algorithms = [sahni_ptas, knapsack_dp, two_approx, Branch_and_boundary]
```


```python
import time as timer


def get_output_and_time(iterations, f, *args):
    start = timer.time()
    for i in range(iterations):
        output = f(*args)
    elapsed = timer.time() - start
    return *output, elapsed
```


```python
for index in range(len(dataset)):
    print('Sample %s' % (index+1), end='\n\n')
    sample = dataset[index]
    for algorithm in algorithms:
        print(algorithm.__name__)
        profit = 0
        iters = 100
        if algorithm.__name__ == 'sahni_ptas':
            profit, items, comparisons, time = get_output_and_time(iters, algorithm, sample[CAPACITY], sample[ITEMS], k)
            binary_items = []
            for item_index in range(len(sample[ITEMS])):
                if item_index in items:
                    binary_items.append(1)
                else:
                    binary_items.append(0)
            items = binary_items
        elif algorithm.__name__ == 'knapsack_dp' or algorithm.__name__ == 'two_approx':
            weights = []
            prices = []
            for item in sample[ITEMS]:
                weights.append(item[WEIGHT])
                prices.append(item[VALUE])
            items, comparisons, time = get_output_and_time(iters, algorithm, sample[CAPACITY], weights, prices)
            for item_index in range(len(items)):
                if items[item_index] == 1:
                    profit += sample[ITEMS][item_index][VALUE]
        elif algorithm.__name__ == 'Branch_and_boundary':
            iters = 10
            weights = []
            prices = []
            for item in sample[ITEMS]:
                weights.append(item[WEIGHT])
                prices.append(item[VALUE])
            items, weight, profit, comparisons, time = get_output_and_time(iters, algorithm, sample[CAPACITY], weights, prices)
        weight = 0
        for item_index in range(len(items)):
            if items[item_index] == 1:
                weight += sample[ITEMS][item_index][WEIGHT]
        print('Items: %s\nProfit: %s\nWeight: %s\nComparisons: %s\nTime: %s (%s iterations)'\
              % (items, profit, weight, comparisons, time, iters), end='\n\n')
    print('')
```

    Sample 1
    
    sahni_ptas
    Items: [1, 1, 1, 1, 0, 1, 0, 0, 0, 0]
    Profit: 309
    Weight: 165
    Comparisons: 187
    Time: 0.1672821044921875 (100 iterations)
    
    knapsack_dp
    Items: [1, 1, 1, 1, 0, 1, 0, 0, 0, 0]
    Profit: 309
    Weight: 165
    Comparisons: 1826
    Time: 0.7765276432037354 (100 iterations)
    
    two_approx
    Items: [1, 1, 1, 1, 0, 1, 0, 0, 0, 0]
    Profit: 309
    Weight: 165
    Comparisons: None
    Time: 0.006340503692626953 (100 iterations)
    
    Branch_and_boundary
    Items: [1.0, 1.0, 1.0, 1.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0]
    Profit: 309
    Weight: 165
    Comparisons: 95
    Time: 7.695439577102661 (10 iterations)
    
    
    Sample 2
    
    sahni_ptas
    Items: [0, 1, 1, 1, 0]
    Profit: 51
    Weight: 26
    Comparisons: 12
    Time: 0.0024690628051757812 (100 iterations)
    
    knapsack_dp
    Items: [0, 1, 1, 1, 0]
    Profit: 51
    Weight: 26
    Comparisons: 162
    Time: 0.04814934730529785 (100 iterations)
    
    two_approx
    Items: [1, 0, 1, 0, 0]
    Profit: 47
    Weight: 23
    Comparisons: None
    Time: 0.00417327880859375 (100 iterations)
    
    Branch_and_boundary
    Items: [0.0, 1.0, 1.0, 1.0, 0.0]
    Profit: 51
    Weight: 26
    Comparisons: 15
    Time: 0.9385185241699219 (10 iterations)
    
    
    Sample 3
    
    sahni_ptas
    Items: [1, 1, 0, 0, 1, 0]
    Profit: 150
    Weight: 190
    Comparisons: 32
    Time: 0.01832127571105957 (100 iterations)
    
    knapsack_dp
    Items: [1, 1, 0, 0, 1, 0]
    Profit: 150
    Weight: 190
    Comparisons: 1337
    Time: 0.5683188438415527 (100 iterations)
    
    two_approx
    Items: [0, 0, 1, 0, 1, 1]
    Profit: 119
    Weight: 172
    Comparisons: None
    Time: 0.014359712600708008 (100 iterations)
    
    Branch_and_boundary
    Items: [1.0, 1.0, 0.0, 0.0, 1.0, 0.0]
    Profit: 150
    Weight: 190
    Comparisons: 23
    Time: 1.6938800811767578 (10 iterations)
    
    
    Sample 4
    
    sahni_ptas
    Items: [1, 1, 0, 0, 0, 1, 1]
    Profit: 105
    Weight: 50
    Comparisons: 61
    Time: 0.02057480812072754 (100 iterations)
    
    knapsack_dp
    Items: [1, 0, 0, 1, 0, 0, 0]
    Profit: 107
    Weight: 50
    Comparisons: 408
    Time: 0.13924193382263184 (100 iterations)
    
    two_approx
    Items: [1, 0, 0, 1, 0, 0, 0]
    Profit: 107
    Weight: 50
    Comparisons: None
    Time: 0.0052144527435302734 (100 iterations)
    
    Branch_and_boundary
    Items: [1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
    Profit: 107
    Weight: 50
    Comparisons: 39
    Time: 2.323709011077881 (10 iterations)
    
    
    Sample 5
    
    sahni_ptas
    Items: [1, 0, 1, 1, 1, 0, 1, 1]
    Profit: 900
    Weight: 104
    Comparisons: 110
    Time: 0.05936789512634277 (100 iterations)
    
    knapsack_dp
    Items: [1, 0, 1, 1, 1, 0, 1, 1]
    Profit: 900
    Weight: 104
    Comparisons: 945
    Time: 0.32321834564208984 (100 iterations)
    
    two_approx
    Items: [0, 1, 1, 1, 0, 1, 1, 1]
    Profit: 888
    Weight: 92
    Comparisons: None
    Time: 0.028102397918701172 (100 iterations)
    
    Branch_and_boundary
    Items: [1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 1.0, 1.0]
    Profit: 900
    Weight: 104
    Comparisons: 21
    Time: 1.689634084701538 (10 iterations)
    
    
    Sample 6
    
    sahni_ptas
    Items: [0, 1, 0, 1, 0, 0, 1]
    Profit: 1735
    Weight: 169
    Comparisons: 66
    Time: 0.026411771774291992 (100 iterations)
    
    knapsack_dp
    Items: [0, 1, 0, 1, 0, 0, 1]
    Profit: 1735
    Weight: 169
    Comparisons: 1368
    Time: 0.4283626079559326 (100 iterations)
    
    two_approx
    Items: [0, 1, 0, 1, 0, 0, 1]
    Profit: 1735
    Weight: 169
    Comparisons: None
    Time: 0.03157639503479004 (100 iterations)
    
    Branch_and_boundary
    Items: [0.0, 1.0, 0.0, 1.0, 0.0, 0.0, 1.0]
    Profit: 1735
    Weight: 169
    Comparisons: 109
    Time: 5.518566846847534 (10 iterations)
    
    
    Sample 7
    
    sahni_ptas
    Items: [1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]
    Profit: 1419
    Weight: 735
    Comparisons: 910
    Time: 0.713756799697876 (100 iterations)
    
    knapsack_dp
    Items: [1, 0, 1, 0, 1, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1]
    Profit: 1458
    Weight: 749
    Comparisons: 12016
    Time: 4.694413661956787 (100 iterations)
    
    two_approx
    Items: [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1]
    Profit: 1315
    Weight: 682
    Comparisons: None
    Time: 0.020045995712280273 (100 iterations)
    
    Branch_and_boundary
    Items: [1.0, 0.0, 1.0, 0.0, 1.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0]
    Profit: 1458
    Weight: 749
    Comparisons: 1305
    Time: 170.38672018051147 (10 iterations)
    
    
    
