#!/usr/bin/env bash
# 图片隐写一键排查: file → binwalk → exiftool → strings → zsteg
# 用法: ./stego_check.sh <图片文件>

set -u
F="${1:?用法: $0 <图片>}"
say(){ printf '\n\033[1;32m== %s ==\033[0m\n' "$1"; }

say "文件类型"
file "$F"

say "binwalk 嵌入文件"
binwalk "$F" || true

say "元数据"
exiftool "$F" 2>/dev/null | grep -viE 'Directory|File (Name|Permissions|Modification)|Process' | head -20 || true

say "明文搜索 flag/key"
strings -n 6 "$F" | grep -iE 'flag|key|pass|ctf' | head || echo "(无命中)"

say "zsteg LSB 分析"
if command -v zsteg >/dev/null; then
    zsteg "$F" | head -20
else
    echo "(未安装 zsteg: gem install zsteg)"
fi

say "PNG 结构检查"
if command -v pngcheck >/dev/null; then
    pngcheck -v "$F" | tail -5
fi

printf '\n\033[1;33m提示:\033[0m 有可疑嵌入用 binwalk -e 解包; 有 LSB 输出按通道用 PIL 提取; 怀疑 steghide 记得找密码提示\n'
