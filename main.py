import flask

from flask import redirect, request, render_template, Flask
from cryptography.fernet import Fernet
import os
from dotenv import dotenv_values, load_dotenv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, template_folder="html")
app.config["SQLALCHEMY_DATABASE_URI"] = (
    "sqlite:////Users/Nizar/OneDrive - Hogeschool Rotterdam/encryption-app/database1.db"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.app_context().push()
db = SQLAlchemy()
db.init_app(app)
config = dotenv_values(".env")

load_dotenv()

user_key = os.getenv("user_key")


encrypt_key = Fernet(user_key)


class users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column((db.String(100)), nullable=False)
    pass_word = db.Column((db.String(100)), nullable=False)

    def __init__(self):

        return f"{self.user_name},{ self.pass_word}"


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    username = request.form.get("username")
    password = request.form.get("password")
    if request.method == "POST":

        user = users(user_name=username, pass_word=password)
        db.session.add(user)
        db.session.commit()
        return render_template("register.html", user_name=username, pass_word=password)
    if request.method == "GET":
        return render_template("register.html", user_name=username, pass_word=password)


@app.route("/login", methods=["GET", "POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if request.method == "POST":
        if check_if_user(username, password):

            return redirect("/encrypt")

    return render_template("login.html")


def check_if_user(username1, password1):

    for i in db.session.query(users):
        print(i.user_name, i.pass_word)
        if (i.user_name, i.pass_word) == (username1, password1):
            return True

    return False


@app.route("/encrypt", methods=["GET", "POST"])
def encrypt():
    text = request.form.get("text")
    if request.method == "POST":
        message = encrypt_key.encrypt(text.encode("utf-8"))
        print(message)
        return render_template("encrypt.html", message=message)
    if request.method == "GET":
        print(text)
        return render_template("encrypt.html")


@app.route("/decrypt", methods=["GET", "POST"])
def decrypt():
    text = request.form.get("text")
    if request.method == "POST":
        message2 = encrypt_key.decrypt(text).decode("utf-8")

        print(type(message2))
        return render_template("decrypt.html", message2=message2)
    if request.method == "GET":
        print(text)

        return render_template("decrypt.html")


if __name__ == "__main__":

    db.create_all()
    app.run(debug=True)
