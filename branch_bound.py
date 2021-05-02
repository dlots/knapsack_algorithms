__author__ = 'BogoroditskayaEkaterina'


import copy
from scipy.optimize import linprog

def if_better(a, num):
    global best_number

    if -a > best_number and num == -1:
        best_number = -a

    return best_number


# ----------------------------------------------------------------------------------------------------------------------
class tree:

    def __init__(self, main, weight, price, border, W, A_equal, b_equal):
        global num_op
        num_op += 1

        if A_equal and b_equal:
            opt = linprog(c=main, A_ub=[weight], b_ub=W, A_eq=A_equal, b_eq=b_equal, bounds=border, method='simplex')
        else:
            opt = linprog(c=main, A_ub=[weight], b_ub=W, bounds=border, method='simplex')

        if opt.status != 0:
            self.status = -1
            return None

        self.left = None
        self.right = None

        self.fun = opt.fun
        self.obj = []
        self.num = -1

        for i in range(len(opt.x)):
            if abs(1 - opt.x[i]) > 0.01:
                self.obj.append(opt.x[i])
            else:
                self.obj.append(round(opt.x[i]))
            if self.obj[i] > 0 and self.obj[i] < 1:
                self.num = i  # позиция нецелого элемента

        if_better(self.fun, self.num)  # проверяем, нашли ли лучшее решение

        self.A_equal = A_equal
        self.b_equal = b_equal
        self.status = 0
        # print("fun = ", self.fun, self.obj, "num = ", self.num, "best", if_better(self.fun, self.num))

    # ----------------------------------------------------------------------------------------------------------------------
    def build(self, main, weight, price, border, W):

        global solution

        if self.num == -1:  # если получили целочисленное решение
            if -self.fun == if_better(self.fun, self.num):
                solution = self.obj
            return

        if -self.fun <= if_better(self.fun, self.num):
            return

        A_equal = copy.deepcopy(self.A_equal)
        b_equal_l = copy.deepcopy(self.b_equal)
        b_equal_r = copy.deepcopy(self.b_equal)

        temp_l = []

        for i in range(len(weight)):
            if i == self.num:
                temp_l.append(1)
            else:
                temp_l.append(0)

        A_equal.append(temp_l)
        b_equal_l.append(1)
        b_equal_r.append(0)

        temp_tree_l = tree(main, weight, price, border, W, A_equal, b_equal_l)  # проверяю статус
        if temp_tree_l.status == 0:
            self.left = temp_tree_l

        temp_tree_r = tree(main, weight, price, border, W, A_equal, b_equal_r)  # проверяю статус
        if temp_tree_r.status == 0:
            self.right = temp_tree_r

        if self.left:
            self.left.build(main, weight, price, border, W)
        else:
            self.left = None

        if self.right:
            self.right.build(main, weight, price, border, W)
        else:
            self.right = None


def main_branc_boundary(weight, price, W):
    main = []
    for p in price:
        main.append(-p)

    border = []
    for i in range(len(weight)):
        border.append((0, 1))

    global best_number
    global solution
    global num_op

    best_number = 0
    solution = []
    num_op = 0

    exp = tree(main, weight, price, border, W, [], [])
    exp.build(main, weight, price, border, W)


def Branch_and_boundary(W, weight, price):
    main_branc_boundary(weight, price, W)
    res_weight = 0
    res_price = 0

    for i in range(len(solution)):
        if solution[i] == 1:
            res_weight += weight[i]
            res_price += price[i]

    return solution, res_weight, res_price, num_op