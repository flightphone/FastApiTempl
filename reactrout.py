import json
from fastapi.responses import HTMLResponse
from fastapi import Depends, Form 
from sqlalchemy import Engine
from dependencies import get_engine
import PyFinder

from fastapi import APIRouter
app = APIRouter()


@app.get("/ustore/gettree")
@app.post("/ustore/gettree")
async def gettree():    
    with open('JSON/gettree.json') as f:
        result = json.load(f)
    return result        

@app.get("/React/Banner")
@app.post("/React/Banner")
async def Banner():
    with open('JSON/Banner.json') as f:
        result = json.load(f)
    return result

@app.get("/React/FinderStart")    
@app.post("/React/FinderStart")
async def FinderStart(id = Form(default="132"), mode = Form(default ="new"), page = Form(default = 1), Fc = Form(default = ""), engine: Engine = Depends(get_engine)):  
    pf = PyFinder.Finder()
    return pf.start_db(id, page, Fc, engine)
    #return pf.start(id, Fc)
    
@app.post("/React/exec")
async def exec(SQLParams = Form(default = ""), KeyF = Form(default=""), IdDeclare = Form(default=""), mode = Form(defauld="data"), engine: Engine = Depends(get_engine)):
    pf = PyFinder.Finder()
    res = pf.save(SQLParams, KeyF, IdDeclare, mode, engine)
    return res
