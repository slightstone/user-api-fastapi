from fastapi import APIRouter, HTTPException

from users import firebase
from users.geocode import fetch_location_from_zip
from users.models import (UserCreateRequest, UserData, UserResponse,
                          UserUpdateRequest)
from users.utils import to_firebase_dict, to_firebase_update_dict

router = APIRouter()


@router.post("/", response_model=UserResponse)
def create_user(user: UserCreateRequest):
    # Enforce uniqueness
    all_users = firebase.get_all_users() or {}
    if any(
        existing_user.get("name") == user.name for existing_user in all_users.values()
    ):
        raise HTTPException(
            status_code=409, detail="User with that name already exists"
        )

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
    users = firebase.get_all_users()
    return users or {}


@router.get("/{user_id}", response_model=UserData)
def get_user(user_id: str):
    user = firebase.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/{user_id}")
def update_user(user_id: str, updates: UserUpdateRequest):
    updates_dict = updates.model_dump(exclude_unset=True)

    if "zip_code" in updates_dict:
        try:
            location = fetch_location_from_zip(updates_dict["zip_code"])
        except Exception as e:
            raise HTTPException(
                status_code=502, detail=f"Could not fetch location info: {str(e)}"
            )
        updates_dict = to_firebase_update_dict(location, updates_dict)

    firebase.update_user(user_id, updates_dict)
    return {"updated": True}


@router.delete("/{user_id}")
def delete_user(user_id: str):
    firebase.delete_user(user_id)
    return {"deleted": True}
