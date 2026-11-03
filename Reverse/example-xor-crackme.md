# 学习笔记 · 无壳 ELF 简单逆向（XOR 校验）

> 来源：入门练习 | 难度：⭐ | 考点：`IDA` `算法还原`

## 题目特征

`file` 显示无壳 ELF，运行后提示 `wrong`，IDA 打开 main 逻辑很短。

## 思路链

### 1. 静态分析

IDA（F5 伪代码）看到类似逻辑：

```c
for (i = 0; i < len; i++)
    if ((input[i] ^ 0x34) != enc[i]) wrong();
right();
```

`enc` 是初始化数组（Shift+E 导出字节数组）。

### 2. 逆向求解

XOR 自逆，直接再异或一遍：

```python
enc = [0x53, 0x47, 0x40, ...]          # IDA 导出的密文
print(bytes(b ^ 0x34 for b in enc).decode())
```

### 3. 验证

把结果喂回程序输出 `right`，确认无误。

## 常见变体与对策

| 变体 | 对策 |
|---|---|
| 多轮 XOR/移位 | 逆推顺序相反执行一遍 |
| 查表替换 | 找到表，构建逆映射 |
| TEA/XXTEA | 找到 delta 与轮数，直接写解密 |
| 反调试卡住 | patch 掉 ptrace/检测跳转，或 LD_PRELOAD |
| z3 约束 | 把比较写成约束，交给 solver |

## 总结

入门逆向 = **看懂伪代码 + 用 Python 复现逆过程**。先掌握这五个变体，大部分简单题都能拿下。
