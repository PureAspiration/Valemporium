import datetime
import time
from threading import Thread

from flask import Flask

app = Flask("")


@app.route("/")
def home():
    return datetime.datetime.fromtimestamp(time.time()).strftime("%d/%m/%Y %H:%M:%S")


def run():
    app.run(host="0.0.0.0", port=8080)


def keep_alive():
    t = Thread(target=run)
    t.start()
