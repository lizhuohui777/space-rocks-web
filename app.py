"""本机游戏大厅入口：启动后在同一台电脑的浏览器中打开。"""
import secrets
import sqlite3
import subprocess
import sys
from pathlib import Path
from threading import Lock

from flask import Flask, abort, jsonify, render_template, request, session
from werkzeug.security import check_password_hash, generate_password_hash
from space_rocks import storage

ROOT = Path(__file__).resolve().parent
app = Flask(__name__)
# 重启服务后需要重新登录；账号和战绩仍然保存在数据库。
app.config.update(SECRET_KEY=secrets.token_hex(32), SESSION_COOKIE_SAMESITE="Strict",
                  MAX_CONTENT_LENGTH=8192, TRUSTED_HOSTS=["127.0.0.1", "localhost"])
game_process = None
launch_lock = Lock()


@app.get("/")
def lobby():
    session.setdefault("csrf", secrets.token_urlsafe(24))
    return render_template("lobby.html", username=session.get("username"))


@app.before_request
def check_form_token():
    if request.method == "POST":
        if not session.get("csrf") or request.headers.get("X-CSRF-Token") != session["csrf"]:
            abort(403)


@app.post("/api/register")
def register():
    data = request.form
    username = data.get("username", "").strip()
    password = data.get("password", "")
    if not 2 <= len(username) <= 30 or not 8 <= len(password) <= 128:
        return jsonify(message="用户名需 2–30 个字符，密码需 8–128 个字符。"), 400
    try:
        storage.add_player(username, generate_password_hash(password))
    except sqlite3.IntegrityError:
        return jsonify(message="这个用户名已经注册。"), 409
    return jsonify(message="注册成功，请用这个账号登录。"), 201


@app.post("/api/login")
def login():
    player = storage.find_player(request.form.get("username", "").strip())
    if player is None or not check_password_hash(player["password_hash"], request.form.get("password", "")):
        return jsonify(message="用户名或密码错误。"), 401
    session.clear()
    session.update(player_id=player["id"], username=player["username"])
    return jsonify(reload=True)


@app.post("/api/logout")
def logout():
    session.clear()
    return jsonify(reload=True)


@app.get("/api/results")
def results():
    if "player_id" not in session:
        return jsonify(message="请先登录。"), 401
    return jsonify(results=storage.recent_results(session["player_id"]))


@app.post("/api/play")
def play():
    global game_process
    if "player_id" not in session:
        return jsonify(message="请先登录。"), 401
    with launch_lock:
        if game_process is not None and game_process.poll() is None:
            return jsonify(message="游戏窗口已打开，请先结束这一局。"), 409
        game_process = subprocess.Popen(
            [sys.executable, "space_rocks", "--player-id", str(session["player_id"])], cwd=ROOT)
    return jsonify(message="已启动桌面游戏。结束后点击刷新战绩。"), 202


if __name__ == "__main__":
    storage.init_db()
    app.run(host="127.0.0.1", port=5050)
