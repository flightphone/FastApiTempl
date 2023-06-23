from fastapi import Request
from sqlalchemy import Engine
from sqlalchemy.orm import Session
from setting import gethtml
from modelext import Nusers
from sqlalchemy import select 
def renderhome(request: Request, engine:Engine):
    stm = select(Nusers)
    with engine.connect() as connection:
        cur = connection.execute(stm)
        data = [e._asdict() for e in cur]
    return gethtml("home.html", {"request": request, "mainTab":data})