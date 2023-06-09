import uuid
from fastapi import Depends, Body, HTTPException, status, Request, Response 
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from sqlalchemy import Engine
import model
from fastapi.responses import RedirectResponse
from dependencies import SessionsLocal, get_api_current_user, get_engine
from setting import gethtml
from fastapi import APIRouter
from testteml import renderhome
router = APIRouter()

appurl = "/app2" 

@router.get(appurl)
async def home(request:Request, engine: Engine = Depends(get_engine)):
    return renderhome(request, engine)
    #return gethtml("home.html", {"request": request})
    #return HTMLResponse(gethtml("/home.html"))

@router.get("/alluser")
async def alluser(eng: Engine = Depends(get_engine)):
    return model.alluser(eng)


@router.post("/adduser")
async def adduser(data = Body(), eng: Engine = Depends(get_engine)):
    username = data["username"]
    password = data["password"]
    name = data["name"]
    return model.createuser(username, password, name, eng)

@router.post("/token")
async def gettoken(response: Response, form_data: OAuth2PasswordRequestForm = Depends(), eng: Engine = Depends(get_engine)):
    user = model.authenticate_user(form_data.username, form_data.password, eng)
    if not user:
        raise HTTPException (
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    tok = str(uuid.uuid4())
    SessionsLocal[tok] = user
    # Set an HttpOnly cookie in the response. `httponly=True` prevents 
    # JavaScript from reading the cookie.
    response.set_cookie(
        key="access_token", 
        value=tok, 
        httponly=True
    )  
    return {"access_token": tok, "token_type": "bearer"}

@router.get("/login", response_class=HTMLResponse)
async def login(request:Request, backUrl:str = ""):
    return gethtml("login.html", {"request": request})

@router.get('/logout')
async def logout(response: Response):
    response.set_cookie(
        key="access_token", 
        value="-", 
        httponly=True
    )
    return RedirectResponse(appurl, headers = response.headers)

@router.get("/user_data")
async def user_data(current_user = Depends(get_api_current_user)):
    return current_user

#====================================auth app=========================================
