from datetime import datetime, timedelta
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

        now = datetime.today()
        some_time = datetime(now.year, now.month, now.day)
        new_time = some_time + relativedelta(days=+1)
        # print(datetime.today().strftime("%d/%m/%Y"))
        # print(new_time.strftime("%d/%m/%Y"))

        self.HEADERS = {'Content-Encoding': 'gzip', 'apikey': self.FLIGHT_API_KEY}

        self.BODY = {"fly_from": self.fromPoint, 'fly_to': self.destPoint, 'date_from': self.dateF,
                     'date_to': self.dateT}

        response = requests.get(url=self.URL, params=self.BODY, headers=self.HEADERS)
        print(response)

        #      print(response.json()[0]["duration"]['price'])
        try:
            flight_num = len(response.json()['data'])
        except KeyError:
            empty_list = []
            return empty_list

        self.DICT = []

        for flight in range(flight_num):
            price = response.json()['data'][0]['price']
            dTime = response.json()['data'][0]['utc_departure']
            aTime = response.json()['data'][0]['utc_arrival']
            cityTo = response.json()['data'][0]['cityTo']
            #            equipment = response.json()['data'][0]['equipment']
            id = response.json()['data'][0]['id']
            item = self.item_dict(price, dTime, aTime, id, cityTo)
            self.DICT.append(item)
        #        print(self.DICT)
        seen = set()
        newDict = []
        for d in self.DICT:
            t = tuple(d.items())
            if t not in seen:
                seen.add(t)
                newDict.append(d)
        return newDict

    def item_dict(self, price, dtime, atime, id, cityTo):
        self.price = price
        self.dtime = dtime
        self.atime = atime
        self.id = id
        self.cityTo = cityTo

        item = {}
        item["Price"] = price
        item["Departure_Time"] = self.dtime[0:10] + " " + self.dtime[12:16]
        item["Arriving Time"] = self.atime[0:10] + " " + self.atime[12:16]
        item["Arriving City"] = cityTo
        item["id"] = id
        return item
