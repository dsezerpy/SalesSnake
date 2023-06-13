from flask import Blueprint, request, render_template, make_response, url_for, redirect, flash, jsonify
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
        date = request.form["date"].split("-")
        date = datetime(int(date[0]), int(date[1]), int(date[2]))
        itemquery = {
            "user": user["_id"],
            "nameid": request.form["name"][0:50].lower(),
            "category": request.form['category'],
        }
        item = helpers.database["stocks"].find_one(itemquery)
        if item:
            helpers.database["stocklogs"].insert_one({
                "item": item["_id"],
                "price": int(request.form['avg_value']),
                "amount": int(request.form['stock']),
                "date": date
            })
            helpers.database["stocks"].find_one_and_replace({"_id": item["_id"]},
                                                            helpers.calc_weighted_avg(item, request.form))
        else:
            ni = {
                "user": user["_id"],
                "nameid": request.form["name"][0:50].lower(),
                "category": request.form['category'],
                "displayname": request.form['name'][0:50],
                "unit": request.form['unit'],
                "average_price": int(request.form['avg_value']),
                "stock_size": int(request.form['stock'])
            }
            helpers.database["stocklogs"].insert_one({
                "item": helpers.database["stocks"].insert_one(ni).inserted_id,
                "price": int(request.form['avg_value']),
                "amount": int(request.form['stock']),
                "date": date
            })
    return render_template("stocks.jinja2", **helpers.process_stocks(user))


@stocks.route("/stocks/detail/<nameid>")
def get_detail(nameid):
    print(nameid)
    items = []
    if nameid == "":
        return jsonify("wrong format")
    stock_logs = helpers.database["stocks"].aggregate([
        {
            '$group': {
                '_id': '$_id',
                'nameid': {
                    '$first': '$nameid'
                }
            }
        }, {
            '$lookup': {
                'from': 'stocklogs',
                'localField': '_id',
                'foreignField': 'item',
                'as': 'logs'
            }
        }
    ])
    for item in stock_logs:
        if item["nameid"] == nameid:
            stock_logs = item
            break
    else:
        return jsonify("item not found")
    for item in stock_logs["logs"]:
        items.append({
            "date": item["date"],
            "price": item["price"],
            "amount": item["amount"]
        })
    return jsonify(items)
