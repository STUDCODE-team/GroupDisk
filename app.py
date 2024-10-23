# Import necessary modules
import os
import re
import pyrebase
from flask import Flask, flash, redirect, render_template, request, session, abort, url_for
from datetime import datetime
from dotenv import load_dotenv
from utils import *


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
storage = firebase.storage()
# Route for the login page

@app.route("/")
def login():
    return renderIfNotLoggedIn('login.html', 'welcome')

# Route for the signup page
@app.route("/signup")
def signup():
    return renderIfNotLoggedIn('signup.html', 'welcome')

UPLOAD_FOLDER = 'uploads/'  # Путь к папке для загрузки файлов
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/welcome", methods=['GET', 'POST'])
def welcome():
    # Если это GET-запрос, просто отображаем страницу
    if request.method == 'GET':
        # Проверяем, что пользователь залогинен
        if session.get("is_logged_in", False):
            return render_template("welcome.html", email=session["email"], name=session["name"])
        else:
            # Если не залогинен, перенаправляем на страницу входа
            return redirect(url_for('login'))
    
    # Если это POST-запрос (загрузка файла)
    if request.method == 'POST':
        if 'file' not in request.files:
            return 'No file part'
        file = request.files['file']
        if file.filename == '':
            return 'No selected file'
        if file and allowed_file(file.filename):
             # Загрузка файла в Firebase Storage
            # bucket = storage.bucket()
            # blob = bucket.blob(file.filename)
            # blob.upload_from_file(file)
            filename = file.filename
            # storage.child("uploaded/file.txt").put(filename)
            storage.child(filename).put(file)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return f'File {filename} uploaded successfully'
        return 'File type not allowed'



def check_password_strength(password):
    return re.match(r'^(?=.*\d).{4,}$', password) is not None


# Route for login
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
        return redirectIfNotLoggedIn('login', 'welcome')

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
        return redirectIfNotLoggedIn('signup', 'welcome')

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
