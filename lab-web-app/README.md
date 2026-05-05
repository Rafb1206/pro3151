# Lab Web App — FastAPI + Streamlit

This lab implements:

- **Backend**: FastAPI REST API with an in-memory “database” (`SELLERS_DB`)
- **Frontend**: Streamlit app that consumes the backend via HTTP (`requests`) and renders a table with `pandas`

## Project structure

```text
lab-web-app
├── backend
│   └── dbfakeapi.py
├── frontend
│   └── dbfakeapp.py
└── README.md
```

## Run the backend (Terminal 1)

From `lab-web-app/backend`:

```bash
python -m pip install -r ..\requirements.txt
uvicorn dbfakeapi:app --reload
```

Backend URLs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Run the frontend (Terminal 2)

From `lab-web-app/frontend`:

```bash
python -m pip install -r ..\requirements.txt
streamlit run dbfakeapp.py
```

Frontend URL:

- `http://localhost:8501`

## What to screenshot for the PDF

- `/docs` showing the `/sellers` endpoints and a successful **Try it out → Execute**
- `/redoc` showing the documented endpoints
- Streamlit page showing the **Sellers table** populated from the API
- (Recommended) Streamlit sidebar showing **Create seller** or **Delete seller** working (proves POST/DELETE client → server)

## Docker Lab (Class 6)

This repo includes a basic 3-tier Docker setup:

- PostgreSQL (service `database`)
- FastAPI backend that checks DB connectivity (`backend/dbbasicapi.py`)
- Streamlit frontend that calls the backend and shows the DB status (`frontend/dbbasicapp.py`)

### Build and run

From the `lab-web-app` folder:

```bash
docker compose up --build
```

### URLs

- Backend docs: `http://localhost:8000/docs` (or `http://localhost:8000/redoc`)
- Frontend: `http://localhost:8501`

