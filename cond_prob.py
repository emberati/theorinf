from dataclasses import field
from decimal import Decimal
from math import log2
from typing import List, Dict


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


ens = None
part = None
full = None
cond = None
full_m = None
ens_ent = None
cond_ent = None
seq = {
    ('x1', 'y1'): 0.019, ('x1', 'y2'): 0.039,
    ('x1', 'y3'): 0.034, ('x1', 'y4'): 0.056,
    ('x2', 'y1'): 0.022, ('x2', 'y2'): 0.092,
    ('x2', 'y3'): 0.038, ('x2', 'y4'): 0.034,
    ('x3', 'y1'): 0.06,  ('x3', 'y2'): 0.055,
    ('x3', 'y3'): 0.037, ('x3', 'y4'): 0.514
}


def do(seq):
    global ens, part, full, cond, full_m, ens_ent, cond_ent
    ens     = find_ensemble(seq)
    part    = partial_probability(seq, ensemble=ens)
    full    = full_probability(part)
    cond    = conditional_probabilities(seq, full)
    full_m  = full_probabilities_multiplication(full, seq)
    ens_ent= ensemble_entropy(full)
    cond_ent= ensemble_entropy(cond)

    print('Полные вероятности:')
    print_full_probabilities(part, full)

    print()
    print('Произведение полных вероятностей:')
    #print('Определение зависимости ансамблей:')
    for define in full_m:
        print(f'p({define[0]})·p({define[1]}) =', full_m.get(define))

    print()
    print('Условные вероятности:')
    print_conditional_probabilities(cond)

    print()
    print('Энтроприя:')
    print_ensemble_entropy(full, ens_ent)

    print()
    print('Условная энтропия:')
    print_conditional_entropy(cond_ent)


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


def print_ensemble_entropy(full, entropies):
    dict_solution = {}
    for key, prob in full.items():
        for letter, entropy in entropies.items():
            if letter in key:
                if letter not in dict_solution:
                    dict_solution[letter] = ([], entropy)
                dict_solution[letter][0].append((key, prob))
                break
            continue
    # Casting to string
    text_solution = ''
    for key, val in dict_solution.items():
        text_solution += f'H({key}) = -('
        text_solution += ' + '.join([f'p({pi[0]})·log2(p({pi[0]}))' for pi in val[0]]) + ') = -('
        text_solution += ' + '.join([f'p({pi[1]})·log2(p({pi[1]}))' for pi in val[0]]) + ') = '
        text_solution += str(val[1]) + '\n'
    print(text_solution)


def print_conditional_entropy(entropies):
    for key, val in entropies.items():
        print(f'H({key[0]}|{key[1]}) =', val)


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


def find_entry(letter: str, seq):
    """
    Находит значения, ключ для которых содержит указанный символ
    :param letter: символ, для которого необходимо найти значения
    :param seq: словарь ключей и значений, в котором необходимо найти значения
    :return: словарь значений, ключ для которых содержит указанный символ
    """
    values = []
    for val in seq:
        if letter in val: values.append(seq.get(val))
    return values


def dec(var):
    """
    Преобразует float `var` в десятичное (Decimal) число.
    :param var: число с плавающей точкой;
    :return: десятичное (Decimal) число.
    """
    return Decimal(str(var))


def partial_probability(seq, ensemble: List[int] = None):
    if not ensemble: ensemble = find_ensemble(seq)
    return {ch: find_entry(ch, seq) for ch in ensemble}


def full_probability(partial_probabilities):
    """
    Находит сумму частичных вероятностей (полную вероятность для каждого символа)
    в виде словаря.
    :param partial_probabilities: словарь, ключами для которых являются символы,
    для которых значениями являются массивы частычных вероятностей;
    :return: словарь, ключами для которых являются символы,
    а значениями - суммы данных частичных вероятностей для каждого символа.
    """
    result = {}
    for letter in partial_probabilities:
        full = 0
        for value in partial_probabilities.get(letter):
            full += dec(value)
        result[letter] = round(full, 3)
    return result


def conditional_probabilities(seq, full_probabilities):
    """
    Находит условные вероятноси для X или Y из словаря совместных вероятностей двух ансамблей.
    :param seq: исходная последовательность (совместная вероятность двух ансамблей);
    :param full_probabilities: словарь полных вероятности для каждого символа;
    :return: словарь условных вероятностей для сочетаний.
    """
    cond_y = {
        key: value for (key, value) in sorted({
            comb[::-1]: round(
                dec(seq.get(comb)) / dec(full_probabilities.get(comb[::-1][1])), 3
            ) for comb in seq
        }.items())
    }
    cond_x = {comb: round(dec(seq.get(comb)) / dec(full_probabilities.get(comb[1])), 3) for comb in seq}
    return {**cond_x, **cond_y}


def full_probabilities_multiplication(full_probabilities, seq):
    prob = full_probabilities
    return {comb: round(dec(prob.get(comb[0])) * dec(prob.get(comb[1])), 3) for comb in seq}


def ensemble_entropy(probabilities):
    import re
    result = {}
    for key, val in probabilities.items():
        if isinstance(key, str): letter = ''.join(re.findall("[a-zA-Z]+", key))
        elif isinstance(key, tuple): letter = (''.join(re.findall("[a-zA-Z]+", key[0])).upper(), key[1])
        else: return 'Переданы неправильные данные!'
        if letter not in result: result[letter] = 0
        result[letter] += dec(val) * dec(log2(val))

    for key, val in result.items():
        result[key] = -round(val, 3)
    return result


# if __name__ == '__main__':
#     do(seq)
