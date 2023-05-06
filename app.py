from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from dependencies import gethtml
import appauth
import filemanager

app = FastAPI()
app.include_router(appauth.router)
app.include_router(filemanager.router)

@app.exception_handler(403)
async def custom_http_exception_handler(request, exc):
    return HTMLResponse(gethtml("login.html"))


@app.get("/")
async def root():
     return HTMLResponse(gethtml("home.html"))

app.mount("/", StaticFiles(directory="wwwroot", html=True))