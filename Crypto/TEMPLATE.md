# [赛事/靶场] [Crypto] 题目名

> 难度：⭐⭐ | 考点：`RSA` `共模攻击`

## 题目信息

- 给定：`n`, `e1`, `e2`, `c1`, `c2`（附 output.txt / task.py）

## 解题思路

### 1. 识别参数特征

- 同一 `n`、不同 `e` → **共模攻击**（gcd(e1,e2)=1）
- `e=3` 且明文较小 → 低指数攻击（直接开立方）
- `d` 很小 → Wiener
- `n` 可分解 → factordb / yafu

### 2. 数学推导

共模攻击：同一明文 m 在相同 n 下被 e1、e2 加密，且 gcd(e1,e2)=1，
由扩展欧几里得求出 `s1*e1 + s2*e2 = 1`，则：

```
m = (c1^s1 * c2^s2) mod n
```

## Exploit

```python
from gmpy2 import invert, powmod
# 完整脚本见 scripts/crypto/rsa_attack.py
```

## Flag

```
flag{...}
```

## 总结

- 拿到 RSA 题先**分类**：看 n（能否分解）、看 e（大小、是否重复）、看泄露了什么
- 工具链：factordb、yafu、sympy、gmpy2
