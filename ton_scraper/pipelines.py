#######################################################################
#                               imports                               #
#######################################################################

from sqlalchemy.orm import sessionmaker

from models import Courses, db_connect, create_course_table

#######################################################################
#                               classes                               #
#######################################################################

class TonScraperPipeline(object):
    def __init__(self):
        engine = db_connect()
        create_course_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()
        course = Courses(**item)

        try:
            session.add(course)
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

        return item
