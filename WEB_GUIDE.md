# Space Rocks 本机游戏大厅

在游戏项目根目录运行：

    .venv/bin/python -m pip install -r requirements.txt
    .venv/bin/python app.py

打开 http://127.0.0.1:5050 。网页和 Pygame 窗口都在运行 Python 的这台电脑上。原来的单机入口 `.venv/bin/python space_rocks` 也能单独使用。

## 第一次实验：登录一次

1. 在浏览器开发者工具打开 Network（网络），填入用户名和至少 8 个字符的密码，点击注册。
2. 找到 `POST /api/register`，在 Payload 看表单字段，在 Response 看 Python 返回的 JSON。请使用练习密码。
3. 在 `static/lobby.js` 找到 `send()`。它通过 `fetch()` 发送表单。在 `app.py` 找到同一路径的 `register()`，它校验输入，将密码哈希交给 `storage.add_player()` 写入 SQLite。
4. 点击登录。后端验证密码哈希，成功后用签名的会话 Cookie 记住玩家。下一次查询战绩时，后端从会话取得玩家 ID，因此每个人只看到自己的记录。

## 第二次实验：保存一局

点击开始游戏，浏览器发送 `POST /api/play`。Python 启动已有的 Pygame 游戏。获胜、失败或按 Esc 时，游戏调用 `record(result)`，将结果写入 `results` 表。点击刷新战绩，浏览器发送 `GET /api/results` 并把 JSON 显示成列表。每局最多保存一次。

## 文件分工

- `templates/lobby.html` 和 `static/lobby.css` 定义页面结构和样式。
- `static/lobby.js` 接收点击、发请求、显示响应。
- `app.py` 接收 HTTP 请求，处理登录状态和启动游戏。
- `space_rocks/storage.py` 管理 `players`、`results` 两张表。`results.player_id` 指向 `players.id`。
- `data/players.sqlite3` 首次启动自动生成。重启服务后重新登录即可看到以前的战绩。
