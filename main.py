import flask

from flask import request

app = flask(__name__)


@app.route("/register")
@app.route("/login")
@app.route("/encrypt")
@app.route("decrypt")
def decrypt(nothing):
    return nothing


if __name__ == "__main__":
    app.run(debug=True)
