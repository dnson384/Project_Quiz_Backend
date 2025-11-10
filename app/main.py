from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.endpoints import user, auth, search

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Server is running at http://127.0.0.1:8000"}


app.include_router(user.router, prefix="/api/user", tags=["USER"])
app.include_router(auth.router, prefix="/api/auth", tags=["AUTHENTICATION"])
app.include_router(search.router, prefix="/api/search", tags=["SEARCH"])
