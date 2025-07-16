from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship, declarative_base, Mapped

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'
    id: Mapped[int] = Column(Integer, primary_key=True)
    tg_id: Mapped[int] = Column(BigInteger, unique=True)
    name: Mapped[str] = Column(String)
   
