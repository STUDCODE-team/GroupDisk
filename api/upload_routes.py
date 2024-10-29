from flask import jsonify, request, Blueprint
from firebase_init import storage
from utils import upload_files, get_files


upload_routes = Blueprint('upload_routes', __name__)


@upload_routes.route("/api/upload_userfiles", methods=["POST"])
def upload_userfiles():
    error_message = ""

    # Проверяем, есть ли ключ 'files' в request.files
    if 'files' not in request.files:
        error_message = 'No file part'
        return {"is_success": False, "error_message": error_message}

    # Получаем список файлов
    files = request.files.getlist('files')
    
    if not files:
        error_message = 'No selected files'
        return {"is_success": False, "error_message": error_message}

    response = {
        "is_success": True,
        "error_message": ""
    }

    # Ваш код для обработки файлов
    if not upload_files(request.form.get('parentId'), files):
        response['is_success'] = False
        response['error_message'] = 'File upload failed'
    
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



        