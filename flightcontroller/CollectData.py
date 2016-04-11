import glob
import sys
from flightcontroller.model.DBConnector import DBConnector
from flightcontroller.util.Collector import Collector
from flightcontroller.wsfdr.FDR import FDR

collectors = []
def clean_up_collectors():
    global collectors
    collectors_2 = []
    for collector in collectors:
        if collector.collect == True:
            collectors_2.append(collector)

    collectors = collectors_2

if __name__ == "__main__":
    files = glob.glob("*.db")
    if 'flights.db' not in files:
        connector = DBConnector.instance()
        connector.setup_database()

    flightDataReader = FDR()
    DEFAULT_INTERV = 30
    program_on = True
    try:
        while program_on:
            clean_up_collectors()
            print "---------------------------------------"
            print "0) List flights."
            print "1) Add flight collector (by flight num)."
            print "2) List collectors."
            print "3) Kill collector (by collector num)."
            print "other) Kill collectors and quit."
            print "---------------------------------------"
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
                    collectors[int(colec)].stop()
                    clean_up_collectors()
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
                clean_up_collectors()
                print "WAITING FOR THREADS TO BE CLOSED GRACEFULLY."
    except (KeyboardInterrupt, SystemExit):
        for collector in collectors:
            collector.stop()
        clean_up_collectors()
        print "THREADS WILL BE CLOSED GRACEFULLY."