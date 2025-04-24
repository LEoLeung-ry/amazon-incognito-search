# app.py
from flask import Flask, render_template, request
import requests, csv, urllib.parse, subprocess, platform

# 你的 Google 表格 CSV URL
GOOGLE_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRrfNPnJeFthusK6rSOMXz3wYSAkpFxXeWOk_UZNDJtmqSmnnHS9_RYhT0GgvW_QdQay7sp5cELUdGb/pub?output=csv"

app = Flask(__name__)
import os

# 在这行之后加入
print("👉 当前工作目录：", os.getcwd())
print("👉 Flask 根路径（root_path）：", app.root_path)
print("👉 Flask 期望的 templates 文件夹：", app.template_folder)
print("👉 该路径存在吗？", os.path.isdir(os.path.join(app.root_path, app.template_folder)))
print("👉 该目录下有什么文件？", os.listdir(os.path.join(app.root_path, app.template_folder)))


def fetch_keywords():
    resp = requests.get(GOOGLE_CSV_URL)
    resp.encoding = resp.apparent_encoding
    reader = csv.reader(resp.text.splitlines())
    # 假设关键词在每行第 1 列
    return [row[0] for row in reader if row and row[0].strip()]

def open_incognito(url: str):
    os_name = platform.system()
    if os_name == "Windows":
        subprocess.Popen(f'start chrome --incognito "{url}"', shell=True)
    elif os_name == "Darwin":
        subprocess.Popen(["open", "-a", "Google Chrome", "--args", "--incognito", url])
    else:
        subprocess.Popen(["google-chrome", "--incognito", url])

@app.route("/")
def index():
    keywords = fetch_keywords()
    return render_template("index.html", keywords=keywords)

@app.route("/search", methods=["POST"])
def search():
    kw = request.form["keyword"]
    url = "https://www.amazon.co.jp/s?k=" + urllib.parse.quote_plus(kw)
    open_incognito(url)
    return ("", 204)

if __name__ == "__main__":
    # debug=True 便于开发调试，部署时可去掉
    app.run(port=5000, debug=True)
