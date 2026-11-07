# Space Rocks · 前后端接口练习

我用一个 Pygame 小行星游戏练习前后端接口。点击注册时，浏览器用 `fetch()` 发送 `POST /api/register`，Flask 把账号写入 SQLite，再返回 JSON。登录后可以启动桌面游戏，结束后用 `GET /api/results` 查看自己的战绩。

## 代码结构

```text
.
├── templates/lobby.html   # 大厅页面和表单
├── static/
│   ├── lobby.js           # 发请求、读回复、更新页面
│   ├── lobby.css          # 页面样式
│   └── guide.html         # 网页版学习指南
├── app.py                 # Flask 接口：注册、登录、启动游戏、读取战绩
├── space_rocks/
│   ├── __main__.py        # 桌面游戏入口
│   ├── game.py            # 游戏循环和胜负判断
│   ├── models.py          # 飞船、小行星和子弹
│   ├── utils.py           # 资源加载和移动辅助函数
│   └── storage.py         # SQLite 读写
├── assets/                # 游戏图片和声音
└── data/players.sqlite3   # 首次启动时在本机生成
```

## 本机运行

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python app.py
```

打开 <http://127.0.0.1:5050> 注册并登录。大厅在浏览器中使用，游戏在运行 Flask 的电脑上打开桌面窗口。
