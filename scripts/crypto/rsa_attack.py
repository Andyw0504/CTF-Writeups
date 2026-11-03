#!/usr/bin/env python3
"""RSA 常见攻击集合: 共模 / 低指数 / 已知因子分解 / Wiener

用法:
    python rsa_attack.py common   n e1 e2 c1 c2
    python rsa_attack.py lowe     e c            (e=3, 明文较小时)
    python rsa_attack.py factordb n e c
    python rsa_attack.py wiener   n e c
"""
import sys
from math import gcd
from gmpy2 import invert, powmod, mpz, isqrt, iroot


def bytes_from_int(m):
    v = int(m)
    return v.to_bytes((v.bit_length() + 7) // 8, 'big')


def common_modulus(n, e1, e2, c1, c2):
    """同一 n 不同 e, gcd(e1,e2)=1"""
    g, s1, s2 = _ext_gcd(e1, e2)
    assert g == 1, 'gcd(e1,e2)!=1, 共模不适用'
    m = (powmod(mpz(c1), mpz(s1), mpz(n)) * powmod(mpz(c2), mpz(s2), mpz(n))) % mpz(n)
    return bytes_from_int(m)


def _ext_gcd(a, b):
    if b == 0:
        return a, 1, 0
    g, x, y = _ext_gcd(b, a % b)
    return g, y, x - (a // b) * y


def low_exponent(e, c, n=None):
    """e=3 且明文小: 直接开 e 次方"""
    m, exact = iroot(mpz(c), int(e))
    if not exact and n:
        # 尝试加 k*n 穷举
        for k in range(10000):
            t, exact = iroot(mpz(c) + k * mpz(n), int(e))
            if exact:
                return bytes_from_int(t)
        raise ValueError('穷举失败')
    return bytes_from_int(m)


def factordb(n, e, c):
    import requests
    f = requests.get(f'https://factordb.com/api?query={n}').json()
    ps = [int(x) for x in f.get('factorization', []) if x]
    if len(ps) < 2:
        raise ValueError('factordb 未能分解')
    p, q = ps[0], ps[1]
    d = invert(mpz(e), (p - 1) * (q - 1))
    return bytes_from_int(powmod(mpz(c), d, mpz(n)))


def wiener(n, e, c):
    """d 较小时, 连分数逼近恢复 d"""
    cf = _continued_fraction(e, n)
    for k, d in _convergents(cf):
        if k and (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            # 验证: x^2 - (n-phi+1)x + n = 0
            b = n - phi + 1
            disc = b * b - 4 * n
            if disc >= 0:
                s = isqrt(mpz(disc))
                if s * s == disc:
                    return bytes_from_int(powmod(mpz(c), mpz(d), mpz(n)))
    raise ValueError('Wiener 失败, d 可能不够小')


def _continued_fraction(a, b):
    while b:
        q = a // b
        yield q
        a, b = b, a - q * b


def _convergents(cf):
    n0, d0, n1, d1 = 0, 1, 1, 0
    for q in cf:
        n0, d0, n1, d1 = n1, d1, q * n1 + n0, q * d1 + d0
        yield n1, d1


if __name__ == '__main__':
    cmd = sys.argv[1]
    a = [int(x, 0) for x in sys.argv[2:]]
    res = {
        'common': lambda: common_modulus(*a[:5]),
        'lowe': lambda: low_exponent(*a),
        'factordb': lambda: factordb(*a),
        'wiener': lambda: wiener(*a),
    }[cmd]()
    print(res)
