# 学习笔记 · PNG 隐写排查套路

> 来源：刷题总结 | 难度：⭐ | 考点：`图片隐写` `LSB`

## 通用排查顺序（背下来）

```bash
file flag.png                       # 1. 真实类型？改后缀？
binwalk -e flag.png                 # 2. 有嵌入文件直接解出来
exiftool flag.png                   # 3. 元数据里有没有提示/flag
strings -n 6 flag.png | grep -iE "flag|key"   # 4. 明文搜索
zsteg flag.png                      # 5. PNG/BMP 的 LSB 分析
```

## 常见分支

### LSB 隐写（zsteg 有输出）

按 zsteg 给出的通道（如 `b1,rgb,lsb,xy`）用 python 提取：

```python
from PIL import Image
im = Image.open('flag.png')
px = im.load()
bits = ''.join(str(px[x,y][0] & 1) for y in range(im.height) for x in range(im.width))
data = int(bits, 2).to_bytes(len(bits)//8, 'big')   # 再按需转文本
```

### Steghide（需要密码）

密码来源一般是图片描述、评论字段或题目附带的另一张图。无提示时先试空密码。

### PNG 结构异常

- 用 `pngcheck -v flag.png` 看 CRC 报错，修复后再看隐藏块
- IEND 之后附加的数据直接 `dd` / python 切出来

## 一键脚本

见 [scripts/misc/stego_check.sh](../../scripts/misc/stego_check.sh)，把上面前 5 步打包。

## 总结

隐写题不靠灵感，靠**固定排查顺序 + 工具熟练度**。每一步都有明确目的，过完没发现就换分类（音频/流量/压缩包伪加密）。
