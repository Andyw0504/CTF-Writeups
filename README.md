# 🚩 CTF-Writeups

> CTF 竞赛 / 靶场题解归档。坚持「打一题、写一题」，重点记录**思路链**与可复用的解题姿势。

## 📂 目录结构

```
CTF-Writeups/
├── Web/      # Web 漏洞利用：SQLi、XSS、SSRF、文件上传、反序列化 ...
├── Pwn/      # 二进制漏洞利用：栈溢出、堆利用、格式化字符串 ...
├── Reverse/  # 逆向工程：静态/动态分析、脱壳、算法还原 ...
├── Crypto/   # 密码学：RSA、AES、格密码、古典密码 ...
├── Misc/     # 杂项：隐写、取证、OSINT、PPC ...
├── scripts/  # 解题脚本库（pwn/crypto/misc）
└── assets/   # 题解截图等资源
```

## 🧪 解题脚本库

| 脚本 | 用途 |
|---|---|
| [scripts/pwn/ret2libc_template.py](scripts/pwn/ret2libc_template.py) | ret2libc 通用模板（泄漏→算基址→二次返回） |
| [scripts/crypto/rsa_attack.py](scripts/crypto/rsa_attack.py) | RSA 攻击集：共模 / 低指数 / factordb / Wiener |
| [scripts/misc/stego_check.sh](scripts/misc/stego_check.sh) | 图片隐写一键排查 |

## 🏆 赛事 & 靶场

| 平台 | 类型 | 状态 |
|---|---|---|
| [BUUCTF](https://buuoj.cn/) | 综合刷题 | 🔄 持续更新 |
| [攻防世界](https://adworld.xctf.org.cn/) | 综合刷题 | 🔄 持续更新 |
| [Hack The Box](https://www.hackthebox.com/) | 靶场 | 🔄 持续更新 |
| [VulnHub](https://www.vulnhub.com/) | 内网渗透靶机 | 📋 计划中 |

## 📝 Writeup 规范

每篇题解按统一模板撰写，见 [Web/TEMPLATE.md](Web/TEMPLATE.md)，核心要求：

1. **思路优先**：先写「为什么这么做」，再写「怎么做」
2. **附上关键 Payload / 脚本**，能复现
3. **总结沉淀**：把学到的新知识单独记录，方便下次检索

## 📑 题解索引

<!-- 新题解写完后，在对应分类下添加链接 -->

### Web
- [学习笔记 · SQL 注入：万能密码到文件写入](Web/example-sqli-to-outfile.md) — `SQLi` `INTO OUTFILE`
- [学习笔记 · SSRF 打内网 Redis](Web/example-ssrf-to-redis.md) — `SSRF` `gopher` `Redis 未授权`
- [学习笔记 · 文件上传绕过姿势汇总](Web/example-upload-bypass.md) — `文件上传` `绕过清单`
- [学习笔记 · XSS 与 CSP 绕过](Web/example-xss-csp-bypass.md) — `XSS` `CSP`

### Pwn
- [学习笔记 · ret2libc 入门](Pwn/example-ret2libc.md) — `栈溢出` `ret2libc`

### Reverse
- [学习笔记 · 无壳 ELF 简单逆向（XOR 校验）](Reverse/example-xor-crackme.md) — `IDA` `算法还原`

### Crypto
- [学习笔记 · RSA 共模攻击](Crypto/example-rsa-common-modulus.md) — `RSA` `扩展欧几里得`

### Misc
- [学习笔记 · PNG 隐写排查套路](Misc/example-png-stego.md) — `隐写` `LSB`

---

> ⚠️ 所有内容仅用于安全学习与合法授权测试。
