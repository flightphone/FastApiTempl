from sqlalchemy import text
from sqlalchemy import Engine
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def createbase(engine: Engine):
    sql = ['drop table users', '''
    create table users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        password TEXT,
        name TEXT
    )
    ''']
    with engine.connect() as connection:
        for e in sql:
            cur = connection.execute(text(e))
            connection.commit()



def createuser(username:str, password:str, name:str, engine: Engine):
    try:
        sql = text("select username from users where username = :u")
        with engine.connect() as connection:
            cur = connection.execute(sql, parameters = {"u": username})
            r = cur.fetchall()
            if len(r) > 0:
                return {"message":"this email alredy use"}        
            
        sql = text("insert into users (username, password, name) values (:u, :p, :n)")
        with engine.connect() as connection:
            cur = connection.execute(sql, parameters = {"u":username, "p": get_password_hash(password), "n":name})
            connection.commit()
        return {"message":"ok"}    
    except Exception as ex:
        return {"message":ex}

def authenticate_user(username: str, password: str, engine: Engine):
    sql = text("select id, username, password, name from users where username = :u")
    with engine.connect() as connection:
        cur = connection.execute(sql, parameters = {"u": username})
        r = cur.fetchall()
    if len(r) == 0:
        return False

    hashed_password = r[0][2]
    if not verify_password(password, hashed_password):
        return False
    return {"id":r[0][0], "username": r[0][1] , "name": r[0][3]}            