import os
import subprocess
from flask import Flask, render_template, redirect, url_for

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")
MAIN_SCRIPT = os.path.join(BASE_DIR, "src", "main.py")


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/launch")
def launch_tool():
    subprocess.Popen(
        ["cmd", "/c", "start", "python", MAIN_SCRIPT],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )
    return redirect(url_for("index"))


@app.route("/outputs")
def open_outputs():
    subprocess.Popen(["explorer", OUTPUTS_DIR])
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)
