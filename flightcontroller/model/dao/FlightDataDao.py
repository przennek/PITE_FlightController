from sqlalchemy import select

from flightcontroller.model.DBConnector import DBConnector
from flightcontroller.model.DBSchema import DBSchema
from flightcontroller.model.dao.AbstractDao import AbstractDao
from flightcontroller.model.dao.FlightDao import FlightDao
from flightcontroller.model.entity.FlightData import FlightData
from flightcontroller.wsfdr.FDM import FDM


class FlightDataDao(AbstractDao):
    def insert_data(self, flight_data):
        session = self.connector.create_session()
        data = self.prepare_data(flight_data)
        flight_data = FlightData()
        id = FlightDao().get_id_by_floc(data[FDM.floc])
        flight_data.flight_id = id
        flight_data.LATITUDE = data[FDM.latitude]
        flight_data.LONGTITUDE = data[FDM.longtitude]
        flight_data.TRACK = data[FDM.track]
        flight_data.CALIBRATED_ATTITUDE = data[FDM.cattitude]
        flight_data.GROUND_SPEED = data[FDM.gspeed]
        session.add(flight_data)
        session.flush()
        session.commit()

    def get_flight_data(self, fid):
        dbSchema = DBSchema.instance()
        flight_data_table = dbSchema.get_flight_data_table()
        sel = select([flight_data_table.c.LATITUDE, flight_data_table.c.LONGTITUDE]).where(flight_data_table.c.flight_id == fid)
        connector = DBConnector.instance().get_engine().connect()
        result = connector.execute(sel)
        rows = result.fetchall()
        result.close()
        return rows
