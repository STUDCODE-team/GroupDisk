from flask import redirect, render_template, session, url_for
import re


def renderIfNotLoggedIn(aim_url, if_logged_url):
    if not session.get("is_logged_in", False):
        return render_template(aim_url)
    else:
        return redirect(url_for(if_logged_url))
    
def redirectIfNotLoggedIn(aim_url, if_logged_url):
    if not session.get("is_logged_in", False):
        return redirect(url_for(aim_url))
    else:
        return redirect(url_for(if_logged_url))


def check_password_strength(password):
    return re.match(r'^(?=.*\d).{4,}$', password) is not None