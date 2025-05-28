from pathlib import Path

import firebase_admin
from firebase_admin import credentials, db

cred_path = Path("config/firebase-credentials.json")

if not firebase_admin._apps:
    cred = credentials.Certificate(cred_path)
    firebase_admin.initialize_app(
        cred, {"databaseURL": "https://user-api-project-default-rtdb.firebaseio.com/"}
    )


def create_user(data):
    ref = db.reference("users")
    new_ref = ref.push(data)
    return new_ref.key


def get_all_users():
    ref = db.reference("users")
    return ref.get()


def get_user(user_id):
    ref = db.reference(f"users/{user_id}")
    return ref.get()


def update_user(user_id, data):
    ref = db.reference(f"users/{user_id}")
    ref.update(data)


def delete_user(user_id):
    ref = db.reference(f"users/{user_id}")
    ref.delete()
