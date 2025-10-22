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
from sqlalchemy import select

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
    Role_id: Mapped[int] = mapped_column(ForeignKey(Roles.Id))
    Created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP())

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

def add_new_user(Tg_user_id: int, Role_id: int, Created_at: str) -> None:
    if not(check_smth_on_exists(tableName=Users, columnName=Users.Tg_user_id, id=Tg_user_id)):
        newUser = Users(Tg_user_id=Tg_user_id, Role_id=Role_id, Created_at=Created_at)
        with Session() as session:
            try:
                session.add(newUser)
            except:
                session.rollback()
                raise
            else:
                session.commit()

def check_smth_on_exists(tableName, columnName, id) -> bool:
    with Session() as session:
        try:
            statement = select(tableName).where(tableName.columnName == id)
            db_object = session.scalars(statement).one()
            
            if db_object:
                return True
        except:
            session.rollback()
            raise

with Session() as session:
    pass
