from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Optional
from sqlalchemy import create_engine
from sqlalchemy import TIMESTAMP
import os
from dotenv import load_dotenv
from sqlalchemy.orm import sessionmaker

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)

class Base(DeclarativeBase):
    pass

class Choices(Base):
    __tablename__ = "Choices"
    
    Id: Mapped[int] = mapped_column(primary_key=True)
    Choice_text: Mapped[str] = mapped_column(String(100))
    Created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP())
    
class Questions(Base):
    __tablename__ = "Questions"
    
    Id: Mapped[int] = mapped_column(primary_key=True)
    Question_text: Mapped[str] = mapped_column(String(500))
    Created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP())

class Question_choice(Base):
    __tablename__ = "Question_choices"
    
    Id: Mapped[int] = mapped_column(primary_key=True)
    Question_id: Mapped[int] = mapped_column(ForeignKey(Questions.Id))
    Choice_id: Mapped[int] = mapped_column(ForeignKey(Choices.Id))
    Created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP())

class Roles(Base):
    __tablename__ = "Roles"
    
    Id: Mapped[int] = mapped_column(primary_key=True)
    Name: Mapped[str] = mapped_column(String(100))
    Created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP())

class Users(Base):
    __tablename__ = "Users"
    
    Id: Mapped[int] = mapped_column(primary_key=True)
    Tg_user_id: Mapped[int] = mapped_column(int())
    Created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP())
    Role_id: Mapped[int] = mapped_column(ForeignKey(Roles.Id))

class Users_statistic(Base):
    __tablename__ = "Users_statistic"
    
    Id: Mapped[int] = mapped_column(primary_key=True)
    User_id: Mapped[int] = mapped_column(ForeignKey(Users.Id))
    Question_id: Mapped[int] = mapped_column(ForeignKey(Questions.Id))
    Choice_id: Mapped[int] = mapped_column(ForeignKey(Choices.Id))
    Created_at: Mapped[int] = mapped_column(ForeignKey(TIMESTAMP()))

def create_tables_in_db() -> None:
    Base.metadata.create_all(engine)
    
Session = sessionmaker(engine)

with Session() as session:
    pass
