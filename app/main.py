from fastapi import FastAPI
from app.api.endpoints import user, auth

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Server is running at http://127.0.0.1:8000"}


app.include_router(user.router, prefix="/api/user", tags=["USER"])
app.include_router(auth.router, prefix="/api/auth", tags=["AUTHENTICATION"])
