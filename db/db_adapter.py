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
from sqlalchemy import Integer

load_dotenv()

engine = create_engine(os.getenv("DATABASE_URL"), echo=True)

Session = sessionmaker(engine)

class Base(DeclarativeBase):
    pass

class Choices(Base):
    __tablename__ = "Choices"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    choice_text: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP())
    
class Questions(Base):
    __tablename__ = "Questions"
    
    id: Mapped[int] = mapped_column(primary_key=True)   
    question_text: Mapped[str] = mapped_column(String(500))
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP())

class Question_choice(Base):
    __tablename__ = "Question_choices"

    id: Mapped[int] = mapped_column(primary_key=True)
    question_id: Mapped[int] = mapped_column(ForeignKey(Questions.Id))
    choice_id: Mapped[int] = mapped_column(ForeignKey(Choices.Id))
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP())

class Roles(Base):
    __tablename__ = "Roles"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP())

class Users(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(primary_key=True)
    tg_user_id: Mapped[int] = mapped_column(Integer())
    role_id: Mapped[int] = mapped_column(ForeignKey("Roles.Id"))
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP())

class Users_statistic(Base):
    def __init__(self):
        super().__init__()

    __tablename__ = "Users_statistic"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("Users.Id"))
    question_id: Mapped[int] = mapped_column(ForeignKey("Questions.Id"))
    choice_id: Mapped[int] = mapped_column(ForeignKey("Choices.Id"))
    created_at: Mapped[int] = mapped_column(ForeignKey("TIMESTAMP()"))

    def __repr__(self) -> str:
        return f"Users({self.id}, {self.user_id}, {self.question_id}, {self.choice_id}, {self.created_at})"

    def __str__(self) -> str:
        return f""

def create_tables_in_db() -> None:
    Base.metadata.create_all(engine)

def add_new_user(tg_user_id: int, role_id: int, created_at: str) -> None:
    if not(check_smth_on_exists(tableName=Users, columnName=Users.tg_user_id, id=tg_user_id)):
        new_user = Users(tg_user_id=tg_user_id, role_id=role_id, created_at=created_at)
        with Session() as session:
            try:
                session.add(new_user)
            except:
                session.rollback()
                raise
            else:
                session.commit()

def check_smth_on_exists(table, column_id, outer_id) -> bool:
    with Session() as session:
        try:
            statement = select(table).where(column_id == outer_id)
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

def get_user_from_db(tg_id: int) -> Users:
    with Session() as session:
        statement = session.select(Users).where(Users.tg_user_id == tg_id)
        result = session.scalars(statement).one()
        return result

def check_own_statistic(user: Users) -> Users_statistic:
    with Session() as session:
        try:
            statement = select(Users_statistic).where(user.id == Users_statistic.user_id)
            db_objects = session.scalars(statement).all()
            result = []
            for i in db_objects:
                Question = select(Questions).where(i.question_id == Questions.id)
                Question = session.scalars(Question).one()
                Choice = select(Choices).where(i.choice_id == Choices.id)
                Choice = session.scalars(Choice).one()
                result.append([Question.question_text, Choice.choice_text])
        except:
            session.rollback()
        else:
            return result

def take_the_survey(user: Users) -> list:
    question_subquery = select(Users_statistic).where(user.id == Users_statistic.user_id)
    question_mainquery = select(Questions).where(Questions.id.not_(question_subquery))
    with Session() as session:
        question = session.scalars(question_mainquery).first()
    choices_mainquery = select(Choices).where(question.id == Choices.id)   
    with Session() as session:
        choices = session.scalars(choices_mainquery).all()
    return [question, choices]
