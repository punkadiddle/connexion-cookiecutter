"""Minimale Flask-Anwendung.

Kann verwendet werden, um einen CF Container am Laufen zu halten,
wenn die eigentliche Anwendung nicht funktioniert.
"""

from flask import Flask
app = Flask(__name__)


@app.route("/")
def hello():
    return "Hello, World!"


if __name__ == "__main__":
    app.run()
