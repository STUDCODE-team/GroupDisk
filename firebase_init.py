import pyrebase
from config.firebase_config import firebase_config

firebase = pyrebase.initialize_app(firebase_config)

auth = firebase.auth()
db = firebase.database()
storage = firebase.storage()
