from sqlalchemy import Column, Integer, Text, create_engine
from sqlalchemy.ext.declarative import DeclarativeBase
from sqlalchemy.orm import sessionmaker

class Base(DeclarativeBase):
    pass
engine = create_engine("sqlite:///conversations.db", echo=False)
Session = sessionmaker(bind=engine)


class Conversation(Base):
    __tablename__ = "conversations"
    id = Column(Integer, primary_key=True)
    prompt = Column(Text)
    response = Column(Text)


Base.metadata.create_all(engine)
