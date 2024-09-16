from flask import Flask, flash, redirect, render_template, request, session, abort, url_for


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
