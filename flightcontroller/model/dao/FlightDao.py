from sqlalchemy import select

from flightcontroller.model.DBConnector import DBConnector
from flightcontroller.model.DBSchema import DBSchema
from flightcontroller.model.dao.AbstractDao import AbstractDao
from flightcontroller.model.entity.Flight import Flight
from flightcontroller.wsfdr.FDM import FDM


class FlightDao(AbstractDao):
    def insert_flight(self, flight_data):
        session = self.connector.create_session()
        data = self.prepare_data(flight_data)

        fid = self.get_id_by_floc(data[FDM.floc])
        if fid is None:
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

    def get_id_by_floc(self, floc):
        dbSchema = DBSchema.instance()
        flight_table = dbSchema.get_flight_table()
        sel = select([flight_table.c.id]).where(flight_table.c.FLOC == floc)
        connector = DBConnector.instance().get_engine().connect()
        result = connector.execute(sel)
        fid = result.fetchone()
        result.close()
        if fid is None:
            return None
        else:
            return fid[0]

    def availble_flights(self):
        dbSchema = DBSchema.instance()
        flight_table = dbSchema.get_flight_table()
        sel = select([flight_table.c.FLOC])
        connector = DBConnector.instance().get_engine().connect()
        result = connector.execute(sel)
        flights = result.fetchall()
        result.close()
        return flights