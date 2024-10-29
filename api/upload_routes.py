from flask import jsonify, request, Blueprint
from firebase_init import storage
from utils import upload_files, get_files


upload_routes = Blueprint('upload_routes', __name__)


@upload_routes.route("/api/upload_userfiles", methods=["POST"])
def upload_userfiles():

    error_message = ""

    if 'files' not in request.files:
        error_message = 'No file part'
    
    files = request.files.getlist('files')  # Получаем список файлов
    if not files:
        error_message = 'No selected files'
    
    response = {
        "is_success": True,
        "error_message": ""
    }

    if error_message or not upload_files(files, request.form.get('parentId')):
        response['is_success'] = False
        response['error_message'] = error_message
    
    return response



@upload_routes.route("/api/get_userfiles", methods=["POST"])
def get_userfiles():
    
    files = get_files(parent_file_id=None)
    
    response = {
        "is_success": True,
        "files": files,
        "error_message": ""
    }

    return response



        