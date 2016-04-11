import urllib2

from flightcontroller.wsfdr.FDM import FDM


class FDR:
    url = None
    hdr = None
    end_mark = None

    def __init__(self):
        self.url = "https://data-live.flightradar24.com/zones/fcgi/feed.js" \
                   "?bounds=83.61663982810687,-80.500767898898,6346.0546875,523.4765625&faa=1&mlat=1&" \
                   "flarm=1&adsb=1&gnd=1&air=1&vehicles=1&estimated=1&maxage=900&gliders=1&stats=1&"

        self.hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 '
                                  '(KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                       'Accept-Encoding': 'none',
                       'Accept-Language': 'en-US,en;q=0.8',
                       'Connection': 'keep-alive'}

        self.end_mark = "}"

    def load_all_flights(self):
        request = urllib2.Request(self.url, headers=self.hdr)
        tries = 0
        try:
            content_result = urllib2.urlopen(request).read()
        except urllib2.URLError:
            if tries < 3:
                content_result = urllib2.urlopen(request).read()
            else:
                raise urllib2.URLError('WS retrieve failed.')
        content_result = content_result.split('\n')
        return content_result

    def read_flight_data(self, floc):
        content_result = self.load_all_flights()
        for line in content_result:
            if floc in str(line):
                return line
        return "Flight with given floc wasn't found."

    def load_flights_list(self):
        floc_set = set()
        content_result = self.load_all_flights()
        for line in content_result:
            if self.end_mark not in str(line):
                floc = str(str(line)[str(line).find("["):].split(",")[FDM.floc]).replace("\"", "")
                if floc != '':
                    floc_set.add(floc)
        return floc_set
