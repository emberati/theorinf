from decimal import Decimal


def cond_prob(chs, seq):
    probabilities = probs(chs, seq)
    conditional_probabilities = calc_cond_prob(seq.keys(), seq)


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


def full_probability_from_seq(ch: str, seq):
    """
    Находит сумму частичных вероятностей (полную вероятность для символа `ch`)
    для последовательности `seq`
    :param ch: символ, для которого необходимо найти вероятность;
    :param seq: последовательность сочетаний;
    :return: полную вероятность для символа `ch`.
    """
    return sum(find_partial_probabilities(ch, seq))


def full_probability_from_partial(ch: str, partial):
    """
        Находит сумму частичных вероятностей (полную вероятность для символа `ch`)
        из частичных вероятностей `partial`
        :param ch: символ, для которого необходимо найти вероятность;
        :param partial: список частичных вероятностей для символа `ch`;
        :return: полную вероятность для символа `ch`.
    """
    return sum(partial)


def calc_condition_probability(comb, seq, prob):
    """
    Находит условную вероятность для сочетания `comb`
    :param comb: сочетание, для которого нужно найти условную вероятность;
    :return: условную вероятность для сочетания `comb`.
    """

    return {comb: dec(seq.get(comb)) / full_probability_from_seq(comb[1], seq) for comb in seq}


def ensemble_entropy(p):
    sum = 0
    for pi in p:
        sum += dec(pi) * dec(-log(pi, 2))
        return sum


def conditional_entropy(p):
    pass


def probs(chs, seq):
    return {ch: full_probability_from_seq(ch, seq) for ch in chs}

# seq = {('x1', 'y1'): 0.21, ('x1', 'y2'): 0.42, ('x1', 'y3'): 0.07, ('x2', 'y1'): 0.09, ('x2', 'y2'): 0.18, ('x2', 'y3'): 0.03}
