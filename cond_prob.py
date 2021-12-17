from decimal import Decimal


def do(ensemble, seq):
    partial_probabilities = {ch: find_partial_probabilities(ch, seq) for ch in ensemble}
    full_probabilities = {ch: sum(partial_probabilities.get(ch)) for ch in ensemble}
    conditional_probabilities = find_condition_probabilities(seq)
    print(f'{partial_probabilities=}')
    print(f'{full_probabilities=}')
    print(f'{conditional_probabilities=}')


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


def find_condition_probabilities(seq):
    """
    Находит условную вероятность для сочетания `comb`
    :param comb: сочетание, для которого нужно найти условную вероятность;
    :return: условную вероятность для сочетания `comb`.
    """

    return {comb: dec(seq.get(comb)) / find_full_probability(comb[1], seq) for comb in seq}


def ensemble_entropy(p):
    sum = 0
    for pi in p:
        sum += dec(pi) * dec(-log(pi, 2))
        return sum


def conditional_entropy(p):
    pass


def probs(chs, seq):
    return {ch: find_full_probability(ch, seq) for ch in chs}

# seq = {('x1', 'y1'): 0.21, ('x1', 'y2'): 0.42, ('x1', 'y3'): 0.07, ('x2', 'y1'): 0.09, ('x2', 'y2'): 0.18, ('x2', 'y3'): 0.03}
