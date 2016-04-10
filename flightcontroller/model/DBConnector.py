import threading

from sqlalchemy import create_engine, orm
from flightcontroller.model.DBSchema import DBSchema


class DBConnector:
    engine = None
    schema = None

    __singleton_lock = threading.Lock()
    __singleton_instance = None

    @classmethod
    def instance(cls):
        if not cls.__singleton_instance:
            with cls.__singleton_lock:
                if not cls.__singleton_instance:
                    cls.__singleton_instance = cls()
        return cls.__singleton_instance

    def __init__(self):
        self.schema = DBSchema.instance()

    def setup_database(self):
        # Create an engine and create all the tables we need
        DBSchema.metadata.bind = self.get_engine()
        DBSchema.metadata.create_all()

    def create_session(self):
        # Set up the session
        sm = orm.sessionmaker(bind=self.engine, autoflush=True, autocommit=False, expire_on_commit=True)
        session = orm.scoped_session(sm)
        session.configure(bind=self.get_engine())
        return session

    def get_engine(self):
        if self.engine is None:
            self.engine = create_engine('sqlite:///flights.db', echo=False)
        return self.engine