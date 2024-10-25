import os
from flask import Flask

from api.upload_routes import upload_routes
from api.auth_routes import auth_routes
from api.main_routes import main_routes


app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

app.register_blueprint(upload_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(main_routes)

if __name__ == "__main__":
    app.run(debug=True)
