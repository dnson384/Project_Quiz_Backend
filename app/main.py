from fastapi import FastAPI

from app.presentation.routers import auth_router, search_router

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Server is running at http://127.0.0.1:8000"}


app.include_router(auth_router.router, prefix="/api", tags=["AUTHENTICATION"])
app.include_router(search_router.router, prefix="/api", tags=["SEARCH"])
