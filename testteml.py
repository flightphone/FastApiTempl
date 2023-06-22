from fastapi import Request
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from setting import gethtml
from modelext import Nusers 
def renderhome(request: Request, engine:Engine):
    with Session(autoflush=False, bind=engine) as db:
        data = db.query(Nusers).all()
    return gethtml("home.html", {"request": request, "mainTab":data})