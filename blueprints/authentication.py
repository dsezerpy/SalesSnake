from flask import Blueprint, request, render_template, make_response, url_for, redirect, flash
import helpers

authentication = Blueprint('authentication', __name__, template_folder='../templates')


@authentication.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        helpers.authenticate_user(request.form["mail"], request.form["passwd"])
        resp = make_response(redirect(url_for("stocks.stocks_page")))
        resp.set_cookie("auth", helpers.create_token({"sub": request.form["mail"]}),
                        helpers.ACCESS_TOKEN_EXPIRE_SECONDS)
        return resp
    return render_template("login.jinja2")


@authentication.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        user = {
            "mail": request.form["mail"],
            "password": request.form["passwd"],
            "currency": request.form["currency"]
        }
        """if request.form["orgid"]:
            user["orgid"]=request.form["orgid"]"""
        helpers.register(user)
    return render_template("register.jinja2")
