from flask import Blueprint, request, render_template, make_response, url_for, redirect, flash
import helpers
from datetime import datetime

stocks = Blueprint('stocks', __name__, template_folder='../templates')


@stocks.route("/stocks", methods=["GET", "POST"])
def stocks_page():
    auth_token = request.cookies.get("auth")
    if not auth_token:
        return redirect(url_for("authentication.login"))
    user = helpers.verify_token(auth_token)
    if not user:
        return redirect(url_for("authentication.login"))
    if request.method == "POST":
        itemquery={
            "user": user["_id"],
            "nameid": request.form["name"].lower(),
            "category": request.form['category'],
        }
        item=helpers.database["stocks"].find_one(itemquery)
        if item:
            helpers.database["stocklogs"].insert_one({
                "item":item["_id"],
                "price":int(request.form['avg_value']),
                "amount":int(request.form['stock'])
            })
        else:
            ni = {
                "user": user["_id"],
                "nameid": request.form["name"].lower(),
                "category": request.form['category'],
                "displayname": request.form['name'],
                "unit": request.form['unit'],
                "currency": request.form['currency']
            }
            helpers.database["stocklogs"].insert_one({
                "item": helpers.database["stocks"].insert_one(ni).inserted_id,
                "price": int(request.form['avg_value']),
                "amount": int(request.form['stock'])
            })
    return render_template("stocks.jinja2", **helpers.process_stocks(user))
