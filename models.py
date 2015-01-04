#######################################################################
#                               imports                               #
#######################################################################

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.engine.url import URL

from ton_scraper import settings

#######################################################################
#                              db setup                               #
#######################################################################

DeclarativeBase = declarative_base()

def db_connect():
    return create_engine(URL(**settings.DATABASE))

#######################################################################
#                              functions                              #
#######################################################################

def create_course_table(engine):
    DeclarativeBase.metadata.create_all(engine)
    
#######################################################################
#                               models                                #
#######################################################################

class Subjects(DeclarativeBase):
    """
    Subject model for db
    """
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True)
    school = Column(String, nullable=False)
    subject_title = Column(String, nullable=False)
    subject_code = Column(String, nullable=False)


class Courses(DeclarativeBase):
    """
    Course model for db
    """
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True)
    number = Column('number', String, nullable=False)
    title = Column('title', String, nullable=False)
    instructors = Column('instructors', ARRAY(String), nullable=True)
    description = Column('instructors', String, nullable=True)
    min_units = Column('min_units', Integer, nullable=True)
    max_units = Column('max_units', Integer, nullable=False)
    subject = Column('subject', String, nullable=False)
