from decimal import Decimal


def code(sequence, reverse=False):
    sequence = sorted(sequence)
    interval = {symb[0] for symb in sequence}

def decode():
    pass


def arithmetic_coding(s, ps, prob=True):
    pss = sorted(ps)
    #seq = (ps[i], s[i] for i in range(len(s))) if prob else (s[i], ps[i] for i in range(len(s)))

    seq = sorted(seq)


def intervals(ps):
    sum = 0
    res = []
    for pi in ps:
        res.append(sum)
        sum += Decimal(str(pi))

    return res


def calc_code(first, end, start, last):
    return first + abs(end - start) * last


def calc_decode():
    pass
