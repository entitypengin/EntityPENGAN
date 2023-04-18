#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from threading import Thread

from flask import Flask


app = Flask("")


@app.route("/")
def main() -> str:
    return "alive"


def run() -> None:
    app.run("0.0.0.0", port=8080)


def keep_alive() -> None:
    t = Thread(target=run)
    t.start()
