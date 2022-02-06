from datetime import datetime
from dateutil.relativedelta import relativedelta
import requests


class FlightSearch:
    def __init__(self):
        self.URL = 'https://tequila-api.kiwi.com/v2/search'
        self.FLIGHT_API_KEY = 'oGsZRbP_OUkV2G7ULnr6tzWnnEWDdl1E'
        self.OFFER_LIST = []

    def get_flight(self, city, code, low_price, id, date):
        self.date = date
        self.HEADERS = {'Content-Encoding': 'gzip', 'apikey': self.FLIGHT_API_KEY}
        self.BODY = {"fly_from": 'MOW', 'fly_to': code, 'date_from': datetime.today().strftime("%d/%m/%Y"),
                     'date_to': self.date}
        #      print(self.BODY)
        response = requests.get(url=self.URL, params=self.BODY, headers=self.HEADERS)
        #      print(response.text)
        if response.json()['data'][0]['price'] < low_price:
            self.OFFER_LIST.append(response.json()['data'])
        #          print(len(self.OFFER_LIST))
        with open('list', mode='a') as file:
            file.write(str(response.json()['data'][0]) + '\n')

    def get_another_flight(self, fromPoint, destPoint, dateF, dateT):
        self.fromPoint = fromPoint
        self.destPoint = destPoint
        self.dateF = dateF
        self.dateT = dateT
        if len(self.dateT) < 3:
            self.dateT = (datetime.today() + relativedelta(days=+1)).strftime("%d/%m/%Y")
     #       self.dateT = datetime.today()
        # now = datetime.today()
        # some_time = datetime(now.year, now.month, now.day)
        # new_time = some_time + relativedelta(days=+1)
        # print(datetime.today().strftime("%d/%m/%Y"))
        # print(new_time.strftime("%d/%m/%Y"))

        self.HEADERS = {'Content-Encoding': 'gzip', 'apikey': self.FLIGHT_API_KEY}

        self.BODY = {"fly_from": self.fromPoint, 'fly_to': self.destPoint, 'date_from': self.dateF,
                     'date_to': self.dateT}

        response = requests.get(url=self.URL, params=self.BODY, headers=self.HEADERS)
        print(response)
        try:
            flight_num = len(response.json()['data'])
            flight_data = response.json()['data']
            print(flight_data)
        except KeyError:
            empty_list = []
            return empty_list
        self.DICT = []
        for flight1 in flight_data:
            names = ['price', 'utc_departure', 'utc_arrival', 'cityTo', 'flyFrom', 'flyTo', 'id', 'distance']
            price = flight1['price']
            dtime = flight1['local_departure']
            atime = flight1['local_arrival']
            cityto = flight1['cityTo']
            flyfrom = flight1['flyFrom']
            flyto = flight1['flyTo']
            duration = flight1['duration']['departure']
            distance = flight1['distance']
           #            equipment = response.json()['data'][0]['equipment']
            id = flight1['id']
            item = self.item_dict(price, dtime, atime, id, cityto, flyfrom, flyto, duration, distance)
            self.DICT.append(item)
        seen = set()
        newdict = []
        for d in self.DICT:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                newdict.append(d)
        return newdict

    def item_dict(self, price, dtime, atime, id, cityto, flyfrom, flyto, duration, distance):
        self.price = price
        self.dtime = dtime
        self.atime = atime
        self.id = id
        self.cityto = cityto
        self.flyfrom = flyfrom
        self.flyto = flyto
        self.duration = duration
        self.distance = distance

        item = {}
        item["Price"] = price
        item["Departure_Time"] = self.dtime[0:10] + " " + self.dtime[11:16]
        item["Arriving Time"] = self.atime[0:10] + " " + self.atime[11:16]
        item["Arriving City"] = self.cityto
        item["id"] = self.id
        item["flyFrom"] = self.flyfrom
        item["flyTo"] = self.flyto
        item["duration"] = self.get_time(self.duration)
        item["distance"] = self.distance
        return item

    def get_time(self, flighttime):
        self.flighttime = flighttime
        self.flighttimeminute= round(int(self.flighttime)%36000*60)
        self.flighttimhour = int(self.flighttime)//36000
        if self.flighttimhour < 1: self.flighttimhour += 1
        self.flighttime = f"{self.flighttimhour}h {str(self.flighttimeminute)[:2]}m"
        return self.flighttime
