# [赛事/靶场] [Misc] 题目名

> 难度：⭐⭐ | 考点：`图片隐写` `LSB`

## 题目信息

- 附件：`flag.png`

## 解题思路

### 1. 基础排查（按顺序过一遍）

```bash
file flag.png                    # 真实类型 / 是否改后缀
binwalk flag.png                 # 嵌入文件（zip/png/压缩包）
exiftool flag.png                # 元数据（作者、注释、GPS）
strings -n 8 flag.png | grep -i flag
```

### 2. 隐写分析

- **LSB**：`zsteg flag.png`（PNG/BMP）；Stegsolve 逐通道查看
- **频域/通道**：Stegsolve 的 Channel/Bit Plane 翻一遍
- **附加数据**：PNG 检查 IDAT 块是否异常、IEND 之后有没有数据

### 3. 深入

- 怀疑密码隐写（steghide/outguess）→ 先找密码提示（图里、题目描述、exif）
- 怀疑 LSB 编码数据 → python 手写提取脚本按位还原

## Flag

```
flag{...}
```

## 总结

- Misc 的套路是**排查顺序**：file → binwalk → exif → strings → zsteg/stegsolve → 专用工具
- 一键排查脚本见 `scripts/misc/stego_check.sh`
