import threading

from sqlalchemy import orm
from sqlalchemy import schema, types

from flightcontroller.model.entity.Flight import Flight
from flightcontroller.model.entity.FlightData import FlightData


class DBSchema:
    metadata = schema.MetaData()
    flight_table = None
    flight_data_table = None

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
        self.get_flight_table()
        self.get_flight_data_table()

        orm.mapper(Flight, self.flight_table, properties={
            'flight_data': orm.relation(FlightData, backref='flight')
        })
        orm.mapper(FlightData, self.flight_data_table)

    def get_flight_table(self):
        if self.flight_table is None:
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
        return self.flight_table

    def get_flight_data_table(self):
        if self.flight_data_table is None:
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
        return self.flight_data_table
