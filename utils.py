import hashlib
import os
import re
from flask import redirect, render_template, session, url_for
from firebase_init import db, storage


def render_if_not_logged_in(aim_url, if_logged_url):
    if not session.get("is_logged_in", False):
        return render_template(aim_url)
    else:
        return redirect(url_for(if_logged_url))
    
def redirect_if_not_logged_in(aim_url, if_logged_url):
    if not session.get("is_logged_in", False):
        return redirect(url_for(aim_url))
    else:
        return redirect(url_for(if_logged_url))


def check_password_strength(password):
    return re.match(r'^(?=.*\d).{4,}$', password) is not None


ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return True
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def get_files(parent_file_id): #TODO parent_file_id
    user_id = session["uid"]

    # Получение списка fileid из users/user_id/my_files
    my_files = db.child("users").child(user_id).child("my_files").get()
    
    # Проверка наличия данных
    if not my_files.each():
        print("No files found for user.")
        return []

    # Получаем список fileid
    file_ids = [file_id.val() for file_id in my_files.each()]

    # Получаем объекты файлов по их ID
    files = []
    for file_id in file_ids:
        file_obj = db.child("files").child(file_id).get()
        if file_obj.val():
            files.append(file_obj.val())
    
    return files


def upload_files(parent_file_id, files):
    is_all_success = True

    for file in files:
        if file and allowed_file(file.filename):
            upload_file(parent_file_id, file)
        else:
            is_all_success = False
    return is_all_success


def upload_file(parent_file_id, file):
    file_id = get_new_file_id()

    _, file_extension = os.path.splitext(file.filename)
    file_extension = file_extension[1:]  # Remove the dot before the extension
    user_id = session["uid"]
    owner = get_owner(parent_file_id, user_id)

    file_data = {
        "extension": file_extension,
        "icon": "",
        "name": file.filename,
        "owner": owner, 
        "path": f'{owner}/{file_id}',
        "shared_with": {},
        "subfiles": {},
        "type": "file"
    }

    # Store file metadata in the database
    db.child(f'files/{file_id}').set(file_data)
    
    # Update user's file list
    if parent_file_id == "null":
        user_files = db.child(f'users/{user_id}/my_files').get().val() or []
        user_files.append(file_id)
        db.child(f'users/{user_id}/my_files').set(user_files)
    else:
        subfiles = db.child(f'files/{parent_file_id}/subfiles').get().val() or []
        subfiles.append(file_id)
        db.child(f'files/{parent_file_id}/subfiles').set(subfiles)

    storage.child(f'{owner}/{file_id}').put(file)


# Returns the user as the owner if there's no parent folder, otherwise the owner of the folder
def get_owner(parent_file_id, user_id):
    if parent_file_id == "null":
        return user_id
    return db.child(f'files/{parent_file_id}/owner').get().val()


def get_new_file_id():
    while True:
        random_bytes = os.urandom(16)
        random_string = random_bytes.hex()
        sha1_hash = hashlib.sha1(random_string.encode()).hexdigest()

        # Check if file_id is unique in the database
        if not db.child('files').child(sha1_hash).get().val():
            return sha1_hash
