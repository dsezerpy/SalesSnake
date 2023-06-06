from flask import Flask, url_for, request, redirect
from blueprints.authentication import authentication
from blueprints.stocks import stocks
from blueprints.categories import categories
import helpers

app = Flask(__name__)
app.register_blueprint(authentication)
app.register_blueprint(stocks)
app.register_blueprint(categories)


@app.route("/")
def main():
    auth_token = request.cookies.get("auth")
    if not auth_token:
        return redirect(url_for("authentication.login"))
    user = helpers.verify_token(auth_token)
    if not user:
        return redirect(url_for("authentication.login"))
    return redirect(url_for("stocks.stocks_page"))


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)
