import os
from datetime import timedelta
from flask import Flask, session

from api.upload_routes import upload_routes
from api.auth_routes import auth_routes
from api.main_routes import main_routes


app = Flask(__name__)

# настройка сессий
@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=365)
    

# настройки
app.secret_key = os.getenv('SECRET_KEY')

# прокидываение маршрутов
app.register_blueprint(upload_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(main_routes)

# настройки локального запуска
if __name__ == "__main__":
    app.run(debug=True, port=5001)
