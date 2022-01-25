from dataclasses import field
from decimal import Decimal
from math import log, log2
from typing import List, Dict


def do(seq):
    ensemble = find_ensemble(seq)
    partial_probabilities = {ch: find_partial_probabilities(ch, seq) for ch in ensemble}
    full_probabilities = {ch: sum(partial_probabilities.get(ch)) for ch in ensemble}
    conditional_probabilities_x = condition_probabilities(seq)
    conditional_probabilities_y = condition_probabilities(seq, rev=True)
    full_probabilities_mult = full_probabilities_multiplication(full_probabilities, seq)

    x_probabilities = find_entry('x', full_probabilities).values()
    y_probabilities = find_entry('y', full_probabilities).values()

    print('Полные вероятности:')
    print_full_probabilities(partial_probabilities, full_probabilities)

    print()
    print('Произведение полных вероятностей')
    #print('Определение зависимости ансамблей:')
    for define in full_probabilities_mult:
        print(f'p({define[0]})·p({define[1]}) =', full_probabilities_mult.get(define))

    print()
    print('Условные вероятности:')
    print_conditional_probabilities(conditional_probabilities_x)
    print_conditional_probabilities(conditional_probabilities_y)

    print()
    print('Энтроприя:')
    print_entropy('x', x_probabilities, ensemble_entropy(x_probabilities))
    print_entropy('y', y_probabilities, ensemble_entropy(y_probabilities))


def print_full_probabilities(partial_probabilities, full_probabilities):
    for ch in partial_probabilities:
        print(f'p({ch})', '=', end=' ')
        print(*partial_probabilities.get(ch), sep=' + ', end=' = ')
        print(full_probabilities.get(ch))


def print_multiplication_of_full_probabilities():
    pass


def print_conditional_probabilities(conditional_probabilities):
    for comb in conditional_probabilities:
        print(f'p({comb[0]}|{comb[1]})', '=', end=' ')
        print(conditional_probabilities.get(comb))


def print_entropy(letter, px, result):
    parts = []
    for probability in px:
        parts.append(f'{probability}·log2({probability})')
    print(f'H({letter})', end=' = -(')
    print(*parts, sep=' + ', end=') = ')
    print(result)


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


def find_entry(letter: str, seq):
    """
    Находит значения, ключ для которых содержит указанный символ
    :param letter: символ, для которого необходимо найти значения
    :param seq: словарь ключей и значений, в котором необходимо найти значения
    :return: словарь значений, ключ для которых содержит указанный символ
    """
    letter_values = {}
    for val in seq:
        if letter in val: letter_values[val] = seq.get(val)
    return letter_values

# Deprecated
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


def full_probability(ch: str, seq):
    """
    Находит сумму частичных вероятностей (полную вероятность для символа `ch`)
    для последовательности `seq`
    :param ch: символ, для которого необходимо найти вероятность;
    :param seq: последовательность сочетаний;
    :return: полную вероятность для символа `ch`.
    """
    return sum(find_partial_probabilities(ch, seq))


def condition_probabilities(seq, rev=False):
    """
    Находит условную вероятность для сочетания `comb`
    :param comb: сочетание, для которого нужно найти условную вероятность;
    :return: условную вероятность для сочетания `comb`.
    """
    if rev: return {comb[::-1]: round(dec(seq.get(comb)) / dec(full_probability(comb[::-1][1], seq)), 3) for comb in seq}
    else: return {comb: round(dec(seq.get(comb)) / full_probability(comb[1], seq), 3) for comb in seq}


def full_probabilities_multiplication(full_probabilities, seq):
    prob = full_probabilities
    return {comb: round(dec(prob.get(comb[0])) * dec(prob.get(comb[1])), 3) for comb in seq}


def ensemble_entropy(px):
    sum_ = 0
    for p in px: sum_ += dec(p) * dec(log2(p))
    return -round(sum_, 3)


def conditional_entropy(p):
    pass


def probs(chs, seq):
    return {ch: full_probability(ch, seq) for ch in chs}

# seq = {('x1', 'y1'): 0.21, ('x1', 'y2'): 0.42, ('x1', 'y3'): 0.07, ('x2', 'y1'): 0.09, ('x2', 'y2'): 0.18, ('x2', 'y3'): 0.03}
