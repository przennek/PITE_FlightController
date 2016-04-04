from sqlalchemy import orm, create_engine
from sqlalchemy import schema, types

from flightcontroller.FDR.FDM import FDM


class FlightDao:
    def insert_data(self, flight_data):
        connector = DBConnector()
        session = connector.create_session()
        data = self.prepare_data(flight_data)
        flight_data = FlightData()
        flight_data.LATITUDE = data[FDM.latitude]
        flight_data.LONGTITUDE = data[FDM.longtitude]
        flight_data.TRACK = data[FDM.track]
        flight_data.CALIBRATED_ATTITUDE = data[FDM.cattitude]
        flight_data.GROUND_SPEED = data[FDM.gspeed]
        session.add(flight_data)
        session.flush()
        session.commit()

    def insert_flight(self, flight_data):
        connector = DBConnector()
        session = connector.create_session()
        data = self.prepare_data(flight_data)
        flight = Flight()
        flight.MODE_S_CODE = data[FDM.modescode]
        flight.RADAR = data[FDM.radar]
        flight.PLANE_TYPE = data[FDM.planetype]
        flight.REGI = data[FDM.registr]
        flight.FROM = data[FDM.flyfrom]
        flight.TO = data[FDM.flyto]
        flight.FLOC = data[FDM.floc]
        session.add(flight)
        session.flush()
        session.commit()

    def prepare_data(self, flight_data):
        data = flight_data[str(flight_data).find("["):]
        return str(data).replace("\"", "").replace("]", "").replace("[", "").split(",")

class Flight(object):
    pass


class FlightData(object):
    pass


class DBSchema:
    metadata = schema.MetaData()
    flight_table = None
    flight_data_table = None

    def __init__(self):
        self.flight_table = schema.Table('flight', self.metadata,
                                         schema.Column('id', types.Integer,
                                                       schema.Sequence('flight_seq_id', optional=True),
                                                       primary_key=True),
                                         schema.Column('FLOC', types.Unicode(32), nullable=False, unique=True),
                                         schema.Column('MODE_S_CODE', types.Unicode(32), nullable=True),
                                         schema.Column('RADAR', types.Unicode(32), nullable=True),
                                         schema.Column('PLANE_TYPE', types.Unicode(32), nullable=True),
                                         schema.Column('REGI', types.Unicode(32), nullable=True),
                                         schema.Column('FROM', types.Unicode(32), nullable=True),
                                         schema.Column('TO', types.Unicode(32), nullable=True))

        self.flight_data_table = schema.Table('flight_data', self.metadata,
                                              schema.Column('id', types.Integer,
                                                            schema.Sequence('flight_seq_id', optional=True),
                                                            primary_key=True),
                                              schema.Column('flight_id', types.Integer,
                                                            schema.ForeignKey('flight.id'), nullable=False),
                                              schema.Column('LATITUDE', types.Float, nullable=False),
                                              schema.Column('LONGTITUDE', types.Float, nullable=False),
                                              schema.Column('TRACK', types.Float, nullable=False),
                                              schema.Column('CALIBRATED_ATTITUDE', types.Float, nullable=False),
                                              schema.Column('GROUND_SPEED', types.Float, nullable=False))
        orm.mapper(Flight, self.flight_table, properties={
            'flight_data': orm.relation(FlightData, backref='flight')
        })
        orm.mapper(FlightData, self.flight_data_table)


class DBConnector:
    engine = None
    schema = None

    def __init__(self):
        self.schema = DBSchema()

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
            self.engine = create_engine('sqlite:///flights.db', echo=True)
        return self.engine
