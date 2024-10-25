from flask import jsonify, request, Blueprint
from firebase_init import storage


upload_routes = Blueprint('upload_routes', __name__)


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_routes.route("/api/upload_userfiles", methods=["POST"])
def upload_userfiles():
    if 'files' not in request.files:
        return 'No file part'
    
    files = request.files.getlist('files')  # Получаем список файлов
    if not files:
        return 'No selected files'  # Исправлено сообщение
    
    for file in files:
        if file and allowed_file(file.filename):
            filename = file.filename
            storage.child(filename).put(file)  # Загрузка каждого файла
        else:
            return f'File type not allowed: {file.filename}'  # Сообщение об ошибке для неподходящих файлов

    return f'Files uploaded successfully'


        