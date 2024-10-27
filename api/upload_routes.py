from flask import jsonify, request, Blueprint
from firebase_init import storage
from utils import upload_files, get_files


upload_routes = Blueprint('upload_routes', __name__)


@upload_routes.route("/api/upload_userfiles", methods=["POST"])
def upload_userfiles():
    if 'files' not in request.files:
        return 'No file part'
    
    files = request.files.getlist('files')  # Получаем список файлов
    if not files:
        return 'No selected files'
    
    return upload_files(parent_file_id=None, files=files)


@upload_routes.route("/api/get_userfiles", methods=["POST"])
def get_userfiles():
    return get_files(parent_file_id=None)



        