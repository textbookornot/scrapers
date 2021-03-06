#######################################################################
#                               imports                               #
#######################################################################

from sqlalchemy import create_engine, Column, Integer, String, PrimaryKeyConstraint
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
    #__table_args__ = (PrimaryKeyConstraint('school', 'subject', 'number'),)

    #id = Column(Integer, primary_key=True)
    school = Column('school', String, primary_key=True, nullable=False)
    subject = Column('subject', String, primary_key=True, nullable=False)
    number = Column('number', String, primary_key=True, nullable=False)
    title = Column('title', String, nullable=False)
    min_units = Column('min_units', Integer, nullable=False)
    max_units = Column('max_units', Integer, nullable=False)
    instructors = Column('instructors', ARRAY(String), nullable=True)
    description = Column('description', String, nullable=True)


class Books(DeclarativeBase):
    """
    Textbook model for db
    """
    __tablename__ = "books"
    isbn13 = Column('isbn13', Integer, primary_key=True, nullable=False)
    # isbn10 = Column('isbn10', Integer, nullable=False)
    amazon_id = Column('amazon_id', Integer)
    # edition = Column('edition', Integer)
    # img_url = Column('img_url', String)




