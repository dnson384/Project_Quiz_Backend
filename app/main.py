import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.presentation.routers import auth_router, search_router

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PUBLIC_DIR_PATH = os.path.join(BASE_DIR, "public")

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Server is running at http://127.0.0.1:8000"}


app.mount("/static", StaticFiles(directory=PUBLIC_DIR_PATH), name="static")

app.include_router(auth_router.router, prefix="/api", tags=["AUTHENTICATION"])
app.include_router(search_router.router, prefix="/api", tags=["SEARCH"])
