# Import necessary modules
import os
import re
import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from datetime import datetime
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

app.secret_key = os.getenv('SECRET_KEY')

firebase_config = {
    "apiKey": os.getenv('FIREBASE_API_KEY'),
    "authDomain": os.getenv('FIREBASE_AUTH_DOMAIN'),
    "projectId": os.getenv('FIREBASE_PROJECT_ID'),
    "storageBucket": os.getenv('FIREBASE_STORAGE_BUCKET'),
    "messagingSenderId": os.getenv('FIREBASE_MESSAGING_SENDER_ID'),
    "appId": os.getenv('FIREBASE_APP_ID'),
    "measurementId": os.getenv('FIREBASE_MEASUREMENT_ID'),
    "databaseURL": os.getenv('FIREBASE_DATABASE_URL')
}

firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()
db = firebase.database()
# Route for the login page
@app.route("/")
def login():
    return render_template("login.html")

# Route for the signup page
@app.route("/signup")
def signup():
    return render_template("signup.html")

# Route for the welcome page
@app.route("/welcome")
def welcome():
    # Check if user is logged in
    if session.get("is_logged_in", False):
        return render_template("welcome.html", email=session["email"], name=session["name"])
    else:
        # If user is not logged in, redirect to login page
        return redirect(url_for('login'))
def check_password_strength(password):
    # At least one digit and at least 6 characters long (no special character or uppercase letter requirement)
    return re.match(r'^(?=.*\d).{6,}$', password) is not None


# Route for login result
@app.route("/result", methods=["POST", "GET"])
def result():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]
        try:
            # Authenticate user
            user = auth.sign_in_with_email_and_password(email, password)
            session["is_logged_in"] = True
            session["email"] = user["email"]
            session["uid"] = user["localId"]
            # Fetch user data
            data = db.child("users").get().val()
            # Update session data
            if data and session["uid"] in data:
                session["name"] = data[session["uid"]]["name"]
                # Update last login time
                db.child("users").child(session["uid"]).update({"last_logged_in": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
            else:
                session["name"] = "User"
            # Redirect to welcome page
            return redirect(url_for('welcome'))
        except Exception as e:
            print("Error occurred: ", e)
            return redirect(url_for('login'))
    else:
        # If user is logged in, redirect to welcome page
        if session.get("is_logged_in", False):
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('login'))

# Route for user registration
@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        result = request.form
        email = result["email"]
        password = result["pass"]
        name = result["name"]
        if not check_password_strength(password):
            print("Password does not meet strength requirements")
            return redirect(url_for('signup'))
        try:
            # Create user account
            auth.create_user_with_email_and_password(email, password)
            # Authenticate user
            user = auth.sign_in_with_email_and_password(email, password)
            session["is_logged_in"] = True
            session["email"] = user["email"]
            session["uid"] = user["localId"]
            session["name"] = name
            # Save user data
            data = {"name": name, "email": email, "last_logged_in": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")}
            db.child("users").child(session["uid"]).set(data)
            return redirect(url_for('welcome'))
        except Exception as e:
            print("Error occurred during registration: ", e)
            return redirect(url_for('signup'))
    else:
        # If user is logged in, redirect to welcome page
        if session.get("is_logged_in", False):
            return redirect(url_for('welcome'))
        else:
            return redirect(url_for('signup'))

# Route for password reset
@app.route("/reset_password", methods=["GET", "POST"])
def reset_password():
    if request.method == "POST":
        email = request.form["email"]
        try:
            # Send password reset email
            auth.send_password_reset_email(email)
            return render_template("reset_password_done.html")  # Show a page telling user to check their email
        except Exception as e:
            print("Error occurred: ", e)
            return render_template("reset_password.html", error="An error occurred. Please try again.")  # Show error on reset password page
    else:
        return render_template("reset_password.html")  # Show the password reset page

# Route for logout
@app.route("/logout")
def logout():
    # Update last logout time
    db.child("users").child(session["uid"]).update({"last_logged_out": datetime.now().strftime("%m/%d/%Y, %H:%M:%S")})
    session["is_logged_in"] = False
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
