from dataclasses import field
from decimal import Decimal
from math import log, log2
from typing import List, Dict


def do(seq):
    ensemble = find_ensemble(seq)
    partial_probabilities = {ch: find_partial_probabilities(ch, seq) for ch in ensemble}
    full_probabilities = {ch: sum(partial_probabilities.get(ch)) for ch in ensemble}
    conditional_probabilities0 = find_condition_probabilities(seq)
    conditional_probabilities1 = find_condition_probabilities(seq, rev=True)
    define_ensemble = find_define_ensemble(full_probabilities, seq)

    x_probabilities = []
    y_probabilities = []
    for ch in ensemble:
        x_probabilities.append(full_probabilities.get(ch))
        y_probabilities.append(full_probabilities.get(ch))

    # print(f'{partial_probabilities=}')
    # print(f'{full_probabilities=}')
    # print(f'{conditional_probabilities0=}')
    # print(f'{conditional_probabilities1=}')
    # print()

    print('Полные вероятности:')
    for ch in partial_probabilities:
        print(ch, '=', end=' ')
        print(*partial_probabilities.get(ch), sep=' + ', end=' = ')
        print(full_probabilities.get(ch))
    print()

    print('Определение ансамблей:')
    for define in define_ensemble:
        print(f'{define}=', define_ensemble.get(define))

    print()
    print('Условные вероятности:')
    for comb in conditional_probabilities0:
        print(comb, '=', end=' ')
        print(conditional_probabilities0.get(comb))

    for comb in conditional_probabilities1:
        print(comb, '=', end=' ')
        print(conditional_probabilities1.get(comb))


def find_ensemble(seq: Dict[tuple, float] = field(default_factory=dict)):
    """
    Находит ансамбль (уникальные вхождения xi, yi) в исходном условии
    :param seq: исходная последовательность сочетаний;
    :return: список уникальных вхождений (ансамбль множества).
    """
    ens = []
    for s in seq:
        for ch in s:
            if ch not in ens: ens.append(ch)
    return sorted(ens)


'''
seq = {('x1', 'y1'): 0.019, ('x1', 'y2'): 0.039, ('x1', 'y3'): 0.034, ('x1', 'y4'): 0.056, ('x2', 'y1'): 0.022, ('x2', 'y2'): 0.092, ('x2', 'y3'): 0.038, ('x2', 'y4'): 0.034, ('x3', 'y1'): 0.06, ('x3', 'y2'): 0.055, ('x3', 'y3'): 0.037, ('x3', 'y4'): 0.514}
ens = ['x1', 'x2', 'x3', 'y1', 'y2', 'y3', 'y4']

# Казах
seq = {('x1', 'y1'): 0.011, ('x1', 'y2'): 0.041, ('x1', 'y3'): 0.037, ('x1', 'y4'): 0.074, ('x2', 'y1'): 0.057, ('x2', 'y2'): 0.06, ('x2', 'y3'): 0.192, ('x2', 'y4'): 0.09, ('x3', 'y1'): 0.068, ('x3', 'y2'): 0.06, ('x3', 'y3'): 0.2, ('x3', 'y4'): 0.11}
# Димас
seq = {('x1', 'y1'): 0.031, ('x1', 'y2'): 0.038, ('x1', 'y3'): 0.046, ('x1', 'y4'): 0.069, ('x2', 'y1'): 0.06, ('x2', 'y2'): 0.061, ('x2', 'y3'): 0.163, ('x2', 'y4'): 0.103, ('x3', 'y1'): 0.051, ('x3', 'y2'): 0.042, ('x3', 'y3'): 0.044, ('x3', 'y4'): 0.292}
# Лёха
seq = {('x1', 'y1'): 0.041, ('x1', 'y2'): 0.046, ('x1', 'y3'): 0.058, ('x1', 'y4'): 0.048, ('x2', 'y1'): 0.041, ('x2', 'y2'): 0.086, ('x2', 'y3'): 0.146, ('x2', 'y4'): 0.045, ('x3', 'y1'): 0.052, ('x3', 'y2'): 0.053, ('x3', 'y3'): 0.27, ('x3', 'y4'): 0.114}

'''


def dec(var):
    """
    Преобразует float `var` в десятичное (Decimal) число
    :param var: число с плавающей точкой;
    :return: десятичное (Decimal) число.
    """
    return Decimal(str(var))


def find_partial_probabilities(ch: str, seq):
    """
    Находит все частичные вероятности для символа из последовательности сочетаний,
    например, для символа `x1` в последовательности:
    {('x1', 'y1'): 0.21, ('x1', 'y2'): 0.42, ('x1', 'y3'): 0.07,
    ('x2', 'y1'): 0.09, ('x2', 'y2'): 0.18, ('x2', 'y3'): 0.03}
    -   [0.21, 0.42, 0.07]
    :param ch: символ для которого необходимо найти все вероятности;
    :param seq: последовательность сочетаний;
    :return: список найденых частичных вероятностей.
    """
    probs = []
    for pair in seq:
        if ch in pair: probs.append(dec(seq.get(pair)))
    return probs


def find_full_probability(ch: str, seq):
    """
    Находит сумму частичных вероятностей (полную вероятность для символа `ch`)
    для последовательности `seq`
    :param ch: символ, для которого необходимо найти вероятность;
    :param seq: последовательность сочетаний;
    :return: полную вероятность для символа `ch`.
    """
    return sum(find_partial_probabilities(ch, seq))


def find_condition_probabilities(seq, rev=False):
    """
    Находит условную вероятность для сочетания `comb`
    :param comb: сочетание, для которого нужно найти условную вероятность;
    :return: условную вероятность для сочетания `comb`.
    """
    if rev: return {comb[::-1]: round(dec(seq.get(comb)) / dec(find_full_probability(comb[::-1][1], seq)), 3) for comb in seq}
    else: return {comb: round(dec(seq.get(comb)) / find_full_probability(comb[1], seq), 3) for comb in seq}


def find_define_ensemble(full_probabilities, seq):
    prob = full_probabilities
    return {comb: round(dec(prob.get(comb[0])) * dec(prob.get(comb[1])), 3) for comb in seq}


def entropy(px):
    sum_ = 0
    for p in px:
        print(p)
        sum_ += dec(p) * dec(log2(p))
    return sum_


def conditional_entropy(p):
    pass


def probs(chs, seq):
    return {ch: find_full_probability(ch, seq) for ch in chs}

# seq = {('x1', 'y1'): 0.21, ('x1', 'y2'): 0.42, ('x1', 'y3'): 0.07, ('x2', 'y1'): 0.09, ('x2', 'y2'): 0.18, ('x2', 'y3'): 0.03}
