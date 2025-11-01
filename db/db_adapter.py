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
    
class Surveys(Base):
    __tablename__ = "Surveys"
    
    id: Mapped[int] = mapped_column(primary_key=True)   
    survey_text: Mapped[str] = mapped_column(String(500))
    userId_which_created: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP())

class Survey_choice(Base):
    __tablename__ = "Survey_choices"

    id: Mapped[int] = mapped_column(primary_key=True)
    survey_id: Mapped[int] = mapped_column(ForeignKey(Surveys.Id))
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
    survey_id: Mapped[int] = mapped_column(ForeignKey("Surveys.Id"))
    choice_id: Mapped[int] = mapped_column(ForeignKey("Choices.Id"))
    created_at: Mapped[int] = mapped_column(ForeignKey("TIMESTAMP()"))

    def __repr__(self) -> str:
        return f"Users({self.id}, {self.user_id}, {self.survey_id}, {self.choice_id}, {self.created_at})"

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
                Survey = select(Surveys).where(i.survey_id == Surveys.id)
                Survey = session.scalars(Survey).one()
                Choice = select(Choices).where(i.choice_id == Choices.id)
                Choice = session.scalars(Choice).one()
                result.append([Survey.survey_text, Choice.choice_text])
        except:
            session.rollback()
        else:
            return result

def take_the_survey(user: Users) -> list:
    survey_subquery = select(Users_statistic).where(user.id == Users_statistic.user_id)
    survey_mainquery = select(Surveys).where(Surveys.id.not_(survey_subquery))
    with Session() as session:
        survey = session.scalars(survey_mainquery).first()
    choices_mainquery = select(Choices).where(survey.id == Choices.id)   
    with Session() as session:
        choices = session.scalars(choices_mainquery).all()
    return [survey, choices]

def check_maked_surveys(user_id: int) -> list:
        user = get_user_from_db(user_id)
        if 1 <= user.role_id <= 4:
            maked_surveys_query = select(Surveys).where(user.id == Surveys.userId_which_created)
            with Session() as session:
                execute_query = session.scalars(maked_surveys_query).all()
            return execute_query

def make_survey(user_id: int, survey_text: str, choices: list) -> None:
    user = get_user_from_db(user_id)
    new_survey = Surveys(survey_text=survey_text, userId_which_created=user.id)
    with Session() as session:
        try:
            query = session.add(new_survey)
        except Exception as e:
            print(e)
            session.rollback()
        else:
            session.commit()
            for i in choices:
                new_choice = Choices(choice_text=i, survey_id=new_survey.id)
                try:
                    session.add(new_choice)
                except Exception as e:
                    print(e)
                    session.rollback()
                else:
                    session.commit()

def check_general_statistic() -> dict:
    dictionary = {}
    with Session() as session:
        try:
            query = select(Users)
            users = session.scalars(query).all()
            for i in users:
                dictionary[i.tg_user_id] = check_own_statistic(i)
        except Exception as e:
            print(e)
            session.rollback()
        else:
            return dictionary

def check_survey_makers() -> list:
    with Session() as session:
        try:
            query = select(Users).where(Users.role_id.in_([2]))
            users = session.scalars(query).all()
        except Exception as e:
            print(e)
            session.rollback()
        else:
            return users

def delete_survey(survey_id: int) -> None:
    with Session() as session:
        try:
            survey_query = select(Surveys).where(Surveys.id == survey_id)
            survey = session.scalars(survey_query).one()
            session.delete(survey)
        except Exception as e:
            print(e)
            session.rollback()
        else:
            session.commit()
