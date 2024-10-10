import flask

from flask import request, render_template, Flask

app = Flask(__name__, template_folder="html")


@app.route("/")
@app.route("/register")
def register():

    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    text = request.form.get("text")
    if request.method == "POST":

        print(text)
        return render_template("encrypt.html")
    if request.method == "GET":
        print(text)
        return render_template("encrypt.html")


@app.route("/decrypt")
def decrypt():
    return render_template("decrypt.html")


if __name__ == "__main__":
    app.run(debug=True)
