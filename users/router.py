from fastapi import APIRouter, HTTPException

from users import firebase
from users.geocode import fetch_location_from_zip
from users.models import UserCreateRequest, UserData, UserResponse
from users.utils import to_firebase_dict, to_firebase_update_dict

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreateRequest):
    try:
        location = fetch_location_from_zip(user.zip_code)
    except Exception as e:
        raise HTTPException(
            status_code=502, detail=f"Could not fetch location info: {str(e)}"
        )

    user_data = to_firebase_dict(location, user)

    user_id = firebase.create_user(user_data)
    return {"id": user_id}


@router.get("/", response_model=dict[str, UserData])
def list_users():
    return firebase.get_all_users()


@router.get("/{user_id}", response_model=UserData)
def get_user(user_id: str):
    user = firebase.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}")
def update_user(user_id: str, updates: dict):
    if "zip_code" in updates:
        try:
            location = fetch_location_from_zip(updates["zip_code"])
        except Exception as e:
            raise HTTPException(
                status_code=502, detail=f"Could not fetch location info: {str(e)}"
            )

        updates = to_firebase_update_dict(location, updates)

    firebase.update_user(user_id, updates)
    return {"updated": True}


@router.delete("/{user_id}")
def delete_user(user_id: str):
    firebase.delete_user(user_id)
    return {"deleted": True}
