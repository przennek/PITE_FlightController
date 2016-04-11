import threading
import urllib2

from flightcontroller.model.dao.FlightDao import FlightDao
from flightcontroller.model.dao.FlightDataDao import FlightDataDao
from flightcontroller.wsfdr.FDR import FDR
from sqlite3 import IntegrityError
from time import sleep

class Collector:
    collect = None
    floc = None
    interval = None
    fdao = FlightDao()
    fdatadao = FlightDataDao()
    flightDataReader = FDR()

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
            self.fdao.insert_flight(self.flightDataReader.read_flight_data(self.floc))
        except IntegrityError:
            print "Flight with given floc, already in DB!"
        except IndexError:
            print "Collection won't start, invalid data from WS."
            self.collect = False
        except urllib2.URLError:
            print "<Collector> ending collection, no data from WS for given floc."
            self.collect = False
        while self.collect:
            print str(self) + " retrieved data from remote WS."
            try:
                self.fdatadao.insert_data(self.flightDataReader.read_flight_data(self.floc))
            except IndexError:
                "<WS went insane on this one, skipping>"
            sleep(self.interval)

    def stop(self):
        print str(self) + " stoping collection."
        self.collect = False

    def __str__(self):
        return "<Collector> (" + self.floc + ")"