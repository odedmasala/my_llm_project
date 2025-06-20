# File: app/models.py
from sqlalchemy import Column, Integer, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class QARecord(Base):
    __tablename__ = "qa_records"
    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    context = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)