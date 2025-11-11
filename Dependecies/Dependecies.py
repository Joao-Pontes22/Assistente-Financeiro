from sqlalchemy.orm import sessionmaker
from Models.Models import db
def init_session():
    session =   None
    try:
        Session = sessionmaker(bind=db)
        session = Session()
        yield session
    finally:
        session.close()