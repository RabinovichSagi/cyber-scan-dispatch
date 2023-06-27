import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')


class DatabaseEngine:
    _engine = None

    @staticmethod
    def engine():
        '''
        not really thread safe implementation of a singletone
        '''
        if not DatabaseEngine._engine:
            DatabaseEngine._engine = create_engine('sqlite:///mock_database.db', echo=True)
            Base.metadata.create_all(DatabaseEngine._engine)

        return DatabaseEngine._engine


class Base(DeclarativeBase):
    pass
