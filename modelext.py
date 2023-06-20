from sqlalchemy import Column, Integer, String, Float, Identity
from model import Base, t_rpdeclare

#id,date,store_nbr,family,sales,onpromotion
class Train(Base):
    __tablename__ = "train"
    id = Column(Integer, primary_key=True, autoincrement=True)
    date = Column(String)
    store_nbr = Column(Integer)
    family = Column(String)
    sales = Column(Float) 
    onpromotion = Column(Integer)


class Nusers(Base):
    __tablename__ = "t_ntusers"
    username = Column(String, primary_key=True) 
    fullname = Column(String) 
    description = Column(String) 
    orgs = Column(String) 
    email = Column(String)  
    icq = Column(String) 
    skype = Column(String) 


t_rpdeclare["132"] = {"key":"id", "table":Train}
t_rpdeclare["120"] = {"key":"username", "table":Nusers}
