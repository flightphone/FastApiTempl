from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from setting import gethtml
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
async def custom_http_exception_handler(request:Request, exc):
    #return HTMLResponse(gethtml("/login.html"))
    return gethtml("login.html", {"request": request})


@app.get("/")
async def root(request: Request):
    #return HTMLResponse(gethtml("/index.html"))
    return gethtml("index.html", {"request": request})

app.mount("/", StaticFiles(directory="wwwroot", html=True))


