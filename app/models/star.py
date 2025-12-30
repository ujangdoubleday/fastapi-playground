from sqlalchemy import Column, Integer, String
from app.db.base import Base

class Star(Base):
    __tablename__ = "stars"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    galaxy = Column(String, index=True)
    system = Column(String, index=True)
