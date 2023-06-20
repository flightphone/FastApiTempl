import sqlalchemy
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
import model
import modelext

#engine = sqlalchemy.create_engine("postgresql+psycopg2://postgres:aA12345678@localhost/sales")
SQLALCHEMY_DATABASE_URL = "sqlite:///./app.db"
engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SessionsLocal = dict()


model.createbase(engine)


def get_engine():
    yield engine


async def get_api_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token in SessionsLocal:
        return SessionsLocal[token]
    else:
        raise credentials_exception
    
async def get_current_user(request: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = request.cookies.get("access_token")
    if not token:
        raise credentials_exception
    if token in SessionsLocal:
        return SessionsLocal[token]
    else:
        raise credentials_exception
