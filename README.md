# 📦 User API - FastAPI Backend

This project is a backend service to manage users and fetch timezone and location data based on ZIP code.

---

## 📘 Assignment Summary

> "The project will start as a simple Express server that you will need to expand and connect to a frontend application (your choice)."

- I implemented the backend in **FastAPI** (Python).
- Firebase is used as the data store.
- Location/timezone is resolved using ZIP codes via the OpenWeatherMap API and `timezonefinder`.

---

## ✅ Features

- Create, retrieve, update, and delete user records
- Automatically fetch and store:
  - Latitude and longitude
  - Timezone name and UTC offset
- ZIP code validation and timezone resolution
- Swagger docs (`/docs`)
- Redoc docs (`/redoc`)
- Test coverage with `pytest` and `vcr.py`
- Firebase integration for persistent data

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12
- [Poetry](https://python-poetry.org/docs/#installation)

### 🔧 Installation

```bash
git clone https://github.com/slightstone/user-api-fastapi.git
cd user-api-fastapi
make install
```

### 🔑 Environment Variables

Create a `.env` file with:

```env
OPENWEATHERMAP_API_KEY=your_api_key_here
GOOGLE_APPLICATION_CREDENTIALS=path/to/firebase_service_account.json
```

Make sure your Firebase Realtime Database URL is set up in your `firebase.py`.

---

## 🏃 Running the Server

```bash
make run
```

Visit:
- Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧪 Running Tests

```bash
make test
```

---

## 🧹 Linting & Formatting

```bash
make lint    # Check with ruff
make format  # Auto-format with black + isort
```

---

## 🧩 Frontend

While the original assignment mentions connecting to a frontend, this project focuses solely on the Python backend. You could easily integrate this API with a React frontend or call it directly from Postman, Swagger UI, or any client.

---

## 📁 Project Structure

```
.
├── users/
│   ├── models.py         # Pydantic models
│   ├── geocode.py        # ZIP code to location
│   ├── firebase.py       # Firebase interaction
│   ├── utils.py          # Helpers for formatting
│   └── router.py         # FastAPI routes
├── tests/
│   ├── test_routers.py
│   ├── test_utils.py
│   └── conftest.py
├── main.py               # FastAPI app instance
├── Makefile
└── README.md
```

---

## 🧠 Author

Samuel Lightstone 
