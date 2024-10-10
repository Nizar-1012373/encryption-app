import flask

from flask import request, render_template, Flask
from cryptography.fernet import Fernet
import os
from dotenv import dotenv_values, load_dotenv

config = dotenv_values(".env")

load_dotenv()
app = Flask(__name__, template_folder="html")
user_key = os.getenv("user_key")

encrypt_key = Fernet(user_key)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


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
        message = encrypt_key.encrypt(text.encode())
        print(message)
        return render_template("encrypt.html")
    if request.method == "GET":
        print(text)
        return render_template("encrypt.html")


@app.route("/decrypt")
def decrypt():
    return render_template("decrypt.html")


if __name__ == "__main__":
    app.run(debug=True)
