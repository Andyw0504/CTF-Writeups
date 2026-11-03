# 学习笔记 · RSA 共模攻击

> 来源：经典攻击学习 | 难度：⭐⭐ | 考点：`RSA` `共模攻击` `扩展欧几里得`

## 题目特征

output.txt 给出同一 `n`、两个不同指数 `e1, e2`、两个密文 `c1, c2`。

## 原理

同一明文 `m` 用同一模数 `n`、不同指数加密：

```
c1 = m^e1 mod n
c2 = m^e2 mod n
```

若 `gcd(e1, e2) = 1`，扩展欧几里得可得 `s1, s2` 使 `s1*e1 + s2*e2 = 1`，于是：

```
m = c1^s1 * c2^s2 mod n
```

（负指数用逆元处理：`c^-1 mod n = pow(c, -1, n)`）

## Exploit

完整脚本见 [scripts/crypto/rsa_attack.py](../../scripts/crypto/rsa_attack.py)，核心：

```python
from gmpy2 import gcdext, powmod
g, s1, s2 = gcdext(e1, e2)
m = (powmod(c1, s1, n) * powmod(c2, s2, n)) % n
print(int(m).to_bytes((int(m).bit_length()+7)//8, 'big'))
```

## RSA 题目快速分类表

| 特征 | 攻击 |
|---|---|
| n 可分解 | factordb / yafu |
| e=3 且 m 很小 | 直接开三次方 |
| e 很大（≈n） | d 小 → Wiener / d 泄露 |
| 同 n 不同 e | 共模攻击 |
| 给了 d 或部分 p | 按位恢复 / Coppersmith |
| 多组共享素数 | 两两 gcd |

## 总结

Crypto 题重在**识别特征**，把常见攻击对应到参数特征上，写好模板脚本随取随用。
