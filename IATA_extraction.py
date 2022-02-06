import pandas as pd
from googletrans import Translator

translator = Translator()
data = pd.read_csv(r'./airport-codes_csv.csv', delimiter=',')

def city_name(name):
  city = translator.translate(text=name, dest='en',  src='auto')
  city = city.text.capitalize()
  return city

def airport_get(city):
  data = pd.read_csv(r'./airport-codes_csv.csv', delimiter=',')
  a = data[data['municipality'] == city][data.type == 'large_airport']
  b = data[data['municipality'].astype(str).str.contains(city)][data.type == 'large_airport']
  iata_list = [i for i in a.ident]
  airport_short = [i for i in a.iata_code]
  airport_shortB = [i for i in b.iata_code]
  joined_air = airport_short + airport_shortB
  joined_air = list(dict.fromkeys(joined_air))
  print(joined_air)
  return joined_air



