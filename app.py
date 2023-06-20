from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from util import gethtml
import appauth
import filemanager
import reactrout

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(appauth.router)
app.include_router(filemanager.router)
app.include_router(reactrout.app)

@app.exception_handler(403)
async def custom_http_exception_handler(request, exc):
    return HTMLResponse(gethtml("login.html"))


# @app.get("/app")
# async def app():
#      return HTMLResponse(gethtml("/home.html"))

@app.get("/")
async def root():
     return HTMLResponse(gethtml("index.html"))

app.mount("/", StaticFiles(directory="wwwroot", html=True))