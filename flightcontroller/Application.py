from flightcontroller.FDR.FDR import FDR
from flightcontroller.Model.Flight import DBConnector, FlightDao

if __name__ == "__main__":
    # connector = DBConnector()
    # connector.setup_database()
    fdao = FlightDao()
    fdao.insert_flight(FDR().read_flight_data("TYW411"))
