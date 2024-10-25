from flask import Blueprint, session
from utils import *


main_routes = Blueprint('main_routes', __name__)


@main_routes.route("/home", methods=['GET'])
def home():
    # Проверяем, что пользователь залогинен
    if session.get("is_logged_in", False):
        return render_template("home.html", email=session["email"], name=session["name"])
    else:
        # Если не залогинен, перенаправляем на страницу входа
        return redirect(url_for('auth_routes.login'))
    


@main_routes.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404