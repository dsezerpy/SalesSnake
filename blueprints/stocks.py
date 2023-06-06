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
        if "":
            pass
        else:
            ni = {
                "user": user["_id"],
                "nameid": "",
                "category": request.form['category'],
                "displayname": request.form['name'],
                "unit": request.form['unit'],
                "stock_amount": int(request.form['stock']),
                "avg_value": int(request.form['avg_value']),
                "currency": request.form['currency']
            }
            helpers.database["stocks"].insert_one(ni)
    items = helpers.database["stocks"].find({"user": user["_id"]})
    items = [helpers.Item(item['category'], item['displayname'], item['unit'], item['currency'], item['stock_amount'],
                          item['avg_value']) for item in items]
    cats=[item['name'] for item in helpers.database["categories"].find({"user": user["_id"]})]
    return render_template("stocks.jinja2", stocks=items,cats=cats)
