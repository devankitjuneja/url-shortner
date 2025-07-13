from sqlalchemy import (
    Column, Integer, String,
    DateTime, BigInteger, TIMESTAMP,
    func
)
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class URL(Base):
    __tablename__ = 'urls'

    id = Column(BigInteger, primary_key=True, index=True)
    url = Column(String, nullable=False)
    shortCode = Column(String, unique=True, nullable=False)
    createdAt = Column(DateTime, server_default="CURRENT_TIMESTAMP")
    updatedAt = Column(TIMESTAMP, server_default="CURRENT_TIMESTAMP", onupdate=func.now())
    accessCount = Column(Integer, default=0)
