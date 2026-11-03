# [赛事/靶场] [Pwn] 题目名

> 难度：⭐⭐ | 考点：`栈溢出` `ret2libc`

## 题目信息

- 附件：`chall`、`libc.so.6`
- 远程：`nc 1.2.3.4 9999`

## 解题思路

### 1. 保护检查

```bash
checksec chall
# Arch: amd64 | RELRO: Partial | Stack: No canary | NX: enabled | PIE: No PIE
```

无 canary → 可栈溢出；NX 开 → 不能直接上 shellcode → 考虑 ROP/ret2libc；无 PIE → 地址固定。

### 2. 偏移量确定

```bash
cyclic 200 | ./chall
cyclic -l 0x6161616x   # → offset
```

### 3. 利用构造

泄漏 puts@got → 根据 libc 版本计算基址 → 返回 system("/bin/sh")。

## Exploit

```python
from pwn import *
# 见 scripts/pwn/ret2libc_template.py
```

## Flag

```
flag{...}
```

## 总结

- **学到了什么**：
- **可复用姿势**：
