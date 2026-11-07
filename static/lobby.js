// fetch 发送 HTTP 请求。服务器返回 JSON，浏览器根据结果更新页面。
const message = document.querySelector("#message");

async function send(url, form) {
    try {
        const response = await fetch(url, {
            method: "POST",
            headers: {"X-CSRF-Token": document.querySelector('meta[name="csrf-token"]').content},
            body: form ? new FormData(form) : null
        });
        if (response.status === 403) {
            message.textContent = "页面已过期，请刷新后重试。";
            return;
        }
        const data = await response.json();
        if (response.ok && data.reload) location.reload();
        else message.textContent = data.message;
    } catch {
        message.textContent = "请求失败，请检查 Python 服务是否正在运行。";
    }
}

const account = document.querySelector("#account");
if (account) {
    account.addEventListener("submit", event => {
        event.preventDefault();
        send(event.submitter?.value || "/api/login", account);
    });
}

document.querySelectorAll("[data-api]").forEach(button => {
    button.addEventListener("click", () => send(button.dataset.api));
});

async function loadResults() {
    const list = document.querySelector("#results");
    try {
        const response = await fetch("/api/results");
        if (response.status === 401) { location.reload(); return; }
        if (!response.ok) throw new Error();
        const data = await response.json();
        const labels = {win: "胜利", loss: "失败", quit: "提前退出"};
        list.replaceChildren();
        if (!data.results.length) list.textContent = "还没有战绩，开始第一局吧。";
        for (const row of data.results) {
            const item = document.createElement("li");
            const time = new Date(row.played_at.replace(" ", "T") + "Z");
            item.textContent = labels[row.outcome] + " · " + time.toLocaleString();
            list.append(item);
        }
    } catch {
        message.textContent = "无法读取战绩，请刷新重试。";
    }
}

const refresh = document.querySelector("#refresh");
if (refresh) {
    refresh.addEventListener("click", loadResults);
    loadResults();
}
