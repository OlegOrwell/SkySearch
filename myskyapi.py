from flask import Flask, render_template, redirect, request, url_for, session, flash
from flight_search import FlightSearch
from IATA_extraction import city_name, airport_get
from datetime import datetime
import time
import datetime
#a = datetime.now.strftime("%Y-%m-%d")
flight = FlightSearch()

appy = Flask(__name__)
appy.secret_key = "mug"


def get_entry_fields(fly_from, fly_to, date_from, date_to):

  #  try:
    char_list = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "[", "]", "{", "}", ';', ':', ',', '.', '/',
                 '<', '>', '?', "|", "`", "~", '-', ',', "_", "+"]
    DATE_F = date_from
    for i in char_list:
        DATE_F = DATE_F.replace(i, "")

    DATE_T = date_to
    for i in char_list:
        DATE_T = DATE_T.replace(i, "")
 #   except TypeError:
  #      pass

    DATE_FROM = DATE_F[6:8] + '/' + DATE_F[4:6] + '/' + DATE_F[0:4]
    DATE_TO = DATE_T[6:8] + '/' + DATE_T[4:6] + '/' + DATE_T[0:4]

    fromPoint = city_name(fly_from)
    departure_city_name = city_name(fromPoint)
    destPoint = city_name(fly_to)
    arriving_city_name = city_name(destPoint)
    fromPoint = airport_get(fromPoint)
    destPoint = airport_get(destPoint)
    print(DATE_FROM, DATE_TO, fromPoint, destPoint)
    # Check if input data is correct

    full = []
    TEMP_DICT = {}


    whole_new_list = []

    for f in fromPoint[0:2]:
        for t in destPoint[0:2]:
            TEMP_DICT = flight.get_another_flight(f, t, DATE_FROM, DATE_TO)
            if not TEMP_DICT:
                # tkinter.messagebox.showinfo("Check your date", "Check your dates and try again")
                quit()
            full.append(TEMP_DICT)
     #       table.insert(END, *TEMP_DICT)
    # self.whole_new_list = [i[0] for i in full]
    for i in full:
        for j in i:
            whole_new_list.append(j)
    print(whole_new_list)
    newlist = sorted(whole_new_list, key=lambda d: d['Price'])
    #create_flight(whole_new_list)
    return whole_new_list


@appy.route("/", methods=["POST", "GET"])
def main_page():
    if request.method == "GET":
        # if "flights" in session:
        #     session.pop("flights")
        #     session.clear()
        return render_template("index.html")
    if request.method == "POST":
        # if "flights" in session:
        #     session.pop("flights")
        #     session.clear()
        fly_from = request.form["from"]
        fly_to = request.form["to"]
        date_from = request.form["fly_from"]
        date_to = request.form["fly_to"]
        session["fly_from"] = fly_from
        session["fly_to"] = fly_to
        session["date_from"] = date_from
        session["date_to"] = date_to
        print(type(session["fly_to"]), type(fly_to), fly_to)
        session["flights"] = get_entry_fields(fly_from, fly_to, date_from, date_to)

        return render_template('data_page.html')
 #       return redirect(url_for("data_page"))

@appy.route('/data/')
def data_page():
    #fl = session["flights"]

    return render_template('data_page.html')


if __name__ == '__main__':
    appy.run(debug=True)