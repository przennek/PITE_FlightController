from sqlalchemy import func

from flightcontroller.model.DBConnector import DBConnector


class AbstractDao:
    connector = DBConnector.instance()

    def prepare_data(self, flight_data):
        data = flight_data[str(flight_data).find("["):]
        return str(data).replace("\"", "").replace("]", "").replace("[", "").split(",")

    def get_max_id(self, table):
        session = self.connector.create_session()
        r = session.query(func.max(table.column))
        session.flush()
        return r
