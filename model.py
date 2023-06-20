from sqlalchemy import Engine, Column, Integer, String
from sqlalchemy.orm import DeclarativeBase, Session
from passlib.context import CryptContext

class Base(DeclarativeBase): pass
  
# создаем модель, объекты которой будут храниться в бд
class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String)
    password = Column(String)
    name = Column(String)
  

t_rpdeclare = dict()
t_rpdeclare["users"] = Users


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def createbase(engine: Engine):
    # создаем таблицы
    Base.metadata.create_all(bind=engine)
    

def createuser(username:str, password:str, name:str, engine: Engine):
    try:
        with Session(autoflush=False, bind=engine) as db:
            r = db.query(t_rpdeclare["users"]).filter(t_rpdeclare["users"].__dict__["username"] == username).first()
            if r:
                return {"message":"this email alredy use"}            
            user = t_rpdeclare["users"]()
            user.__dict__["username"] = username
            user.__dict__["password"] = get_password_hash(password)
            user.__dict__["name"] = name
            db.add(user)
            db.commit()
            db.refresh(user)
        return {"message": user.__dict__["id"]}    

    except Exception as ex:
        return {"message":ex}

def authenticate_user(username: str, password: str, engine: Engine):
    with Session(autoflush=False, bind=engine) as db:
        #r = db.query(Users).filter(Users.__dict__["username"] == username).first()
        r = db.query(t_rpdeclare["users"]).filter(t_rpdeclare["users"].__dict__["username"] == username).first()
    if r is None:
        return False
    row = r.__dict__    
    hashed_password = row["password"]
    if not verify_password(password, hashed_password):
        return False
    return row


def alluser(engine: Engine):
    with Session(autoflush=False, bind=engine) as db:
    # получение всех объектов
        result = db.query(t_rpdeclare["users"]).all()
    return result
    