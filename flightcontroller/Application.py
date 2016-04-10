import glob
import threading
from sqlite3 import IntegrityError
from time import sleep

import sys

from flightcontroller.model.DBConnector import DBConnector
from flightcontroller.model.dao.FlightDao import FlightDao
from flightcontroller.model.dao.FlightDataDao import FlightDataDao
from flightcontroller.wsfdr.FDR import FDR

class Collector:
    collect = None
    floc = None
    interval = None

    def __init__(self, floc, interval):
        self.collect = True
        self.floc = floc
        self.interval = interval
        self.t = None

    def start(self):
        self.t = threading.Thread(target=self.__collect)
        self.t.start()
        print "Started collecting flight (" + str(self.floc) + "), " + "with int_val = " + str(self.interval) + "."

    def __collect(self):
        try:
            fdao.insert_flight(flightDataReader.read_flight_data(self.floc))
        except IntegrityError:
            print "Flight with given floc, already in DB!"
        except IndexError:
            print "Collection won't start, invalid data from WS."
            self.collect = False

        while self.collect:
            print str(self) + " retrieved data from remote WS."
            try:
                fdatadao.insert_data(flightDataReader.read_flight_data(self.floc))
            except IndexError:
                "<WS went insane on this one, skipping>"
            sleep(self.interval)

    def stop(self):
        self.collect = False

    def __str__(self):
        return "<Collector> (" + self.floc + ")"

def print_menu():
    print "---------------------------------------"
    print "0) List flights."
    print "1) Add flight collector (by flight num)."
    print "2) List collectors."
    print "3) Kill collector (by collector num)."
    print "other) Kill collectors and quit."
    print "---------------------------------------"

if __name__ == "__main__":
    files = glob.glob("*.db")
    if 'flights.db' not in files:
        connector = DBConnector.instance()
        connector.setup_database()

    DEFAULT_INTERV = 30
    fdao = FlightDao()
    fdatadao = FlightDataDao()
    flightDataReader = FDR()

    collectors = []
    program_on = True
    try:
        while program_on:
            print_menu()
            menu = int(raw_input(": "))
            flocs = None
            if menu == 0:
                flocs = list(flightDataReader.load_flights_list())
                print "Availble flights: "
                counter = 0
                for floc in flocs:
                    print str(counter) + ") " + floc
                    counter += 1
            elif menu == 1:
                flocs = list(flightDataReader.load_flights_list())
                floc = raw_input("floc number: ")
                floc = flocs.pop(int(floc))
                colec = Collector(floc, DEFAULT_INTERV)
                collectors.append(colec)
                colec.start()
            elif menu == 2:
                coun = 0
                for collector in collectors:
                    print str(coun) + ") " + str(collector)
                    coun += 1
            elif menu == 3:
                colec = raw_input("Collector number: ")
                try:
                    colec = collectors.pop(int(colec))
                    colec.stop()
                except IndexError:
                    print "<Out of range, collection won't stop>"
            elif menu == 42:
                # in case FBI knocking at your door
                sys.exit()
            else:
                # exit gracefully
                program_on = False
                for collector in collectors:
                    collector.stop()
                print "WAITING FOR THREADS TO BE CLOSED GRACEFULLY."
    except (KeyboardInterrupt, SystemExit):
        for collector in collectors:
            collector.stop()
        print "THREADS WILL BE CLOSED GRACEFULLY."




