from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from users.router import router as user_router

app = FastAPI(
    title="User Geolocation API",
    description="Creates and manages users by enriching them with ZIP-based geolocation data including timezone info.",
    version="1.0.0",
    contact={
        "name": "Sam Lightstone",
        "email": "slightstone@gmail.com",
    },
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(user_router, prefix="/users", tags=["users"])
