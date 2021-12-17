from math import copysign, fabs, floor, isfinite, modf, log
from decimal import Decimal


def float_to_bin(f):
    if not isfinite(f):
        return repr(f)  # inf nan
    sign = '-' * (copysign(1.0, f) < 0)
    frac, fint = modf(fabs(f))  # split on fractional, integer parts
    n, d = frac.as_integer_ratio()  # frac = numerator / denominator
    assert d & (d - 1) == 0  # power of two
    return f'{sign}{floor(fint):b}.{n:0{d.bit_length()-1}b}'


#def


def l_average(pi, l):
    sum = 0
    for i in range(len(pi)):
        sum += Decimal(str(pi[i])) * Decimal(str(l[i]))
    return sum


def entropy(pi):
    sum = 0
    for p in pi:
        sum += Decimal(str(p)) * Decimal(str(-log(p, 2)))
    return sum


def redundancy(l_av, H):
    return Decimal(str(l_av)) - Decimal(str(H))


def qm_func(pi):
    sum = 0
    res = []
    for p in pi:
        res.append(sum)
        sum += Decimal(str(p))
    return res


def G_func(pi, qm):
    return [Decimal(str(pi[i] / 2)) + qm[i] for i in range(len(qm))]


def l_func(pi):
    return [int(-log(p, 2) + 1) + 1 for p in pi]


def code_func(G, l):
    return [float_to_bin(G[i])[2:2+(l[i]):] for i in range(len(l))]


def hilbert_coding(xm, pi):
    qm = qm_func(pi)
    G = G_func(pi, qm)
    l = l_func(pi)
    code = code_func(G, l)

    res_header = f'xm\t\tpi\t\tqm\t\tG\t\tl\t\tcode'
    line = '-' * (len(res_header) + 80)
    # print(line)
    print(res_header)
    print(line)
    for i in range(len(xm)):
        print(
            f'{xm[i]}\t\t'
            f'{pi[i]}\t\t'
            f'{qm[i]}\t\t'
            f'{G[i]}\t\t'
            f'{l[i]}\t\t{code[i]}')


xm = ['z1', 'z5', 'z4', 'z6', 'z10', 'z8', 'z7', 'z2', 'z9', 'z3']
pi = [0.355, 0.28, 0.1, 0.073, 0.054, 0.046, 0.034, 0.03, 0.018, 0.01]
hilbert_coding(xm, pi)
