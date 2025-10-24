from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy import String
from sqlalchemy import ForeignKey
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
    Role_id: Mapped[int] = mapped_column(ForeignKey("Roles.Id"))
    Created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP())

class Users_statistic(Base):
    def __init__(self):
        super().__init__()

    __tablename__ = "Users_statistic"

    Id: Mapped[int] = mapped_column(primary_key=True)
    User_id: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    Question_id: Mapped[int] = mapped_column(ForeignKey("Questions.Id"))
    Choice_id: Mapped[int] = mapped_column(ForeignKey("Choices.Id"))
    Created_at: Mapped[int] = mapped_column(ForeignKey("TIMESTAMP()"))

    def __repr__(self) -> str:
        return f"Users({self.Id}, {self.User_id}, {self.Question_id}, {self.Choice_id}, {self.Created_at})"

    def __str__(self) -> str:
        return f""

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

def check_smth_on_exists(table, columnId, outerId) -> bool:
    with Session() as session:
        try:
            statement = select(table).where(columnId == outerId)
            db_object = session.scalars(statement).first()
            
            if db_object:
                return True
        except Exception as e:
            session.rollback()
            raise e

def add_user_to_db(user: Users) -> None:
    with Session() as session:
        try:
            session.add(user)
        except:
            session.rollback()
        else:
            session.commit()

def get_user_from_db(tg_id: int):
    with Session() as session:
        statement = session.select(Users).where(Users.Tg_user_id == tg_id)
        result = session.scalars(statement).first()
        return result

def check_own_statistic(user: Users):
    with Session() as session:
        try:
            statement = select(Users_statistic).where(user.id == Users_statistic.User_id)
            db_objects = session.scalars(statement).all()
            
            number = 0
            result = []
            for i in db_objects:
                number += 1
                Question = select(Questions).where(i[2] == Questions.id)
                Question = session.scalars(Question).one()
                Choice = select(Choices).where(i[3] == Choices.id)
                Choice = session.scalars(Choice).one()
                result.append([Question.Question_text, Choice.Choice_text])
                
        except:
            session.rollback()
        else:
            return result

with Session() as session:
    pass
