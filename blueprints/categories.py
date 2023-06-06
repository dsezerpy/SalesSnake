from flask import Blueprint, request, render_template, make_response, url_for, redirect, flash
import helpers

categories = Blueprint('categories', __name__, template_folder='../templates')


@categories.route("/categories", methods=["GET", "POST"])
def categories_page():
    auth_token = request.cookies.get("auth")
    if not auth_token:
        return redirect(url_for("authentication.login"))
    user = helpers.verify_token(auth_token)
    if not user:
        return redirect(url_for("authentication.login"))
    if request.method == "POST":
        ni = {
            "user": user["_id"],
            "name": request.form['name'],
        }
        helpers.database["categories"].insert_one(ni)
    cats = [name["name"] for name in helpers.database["categories"].find({"user": user["_id"]})]
    return render_template("categories.jinja2", categories=cats)
