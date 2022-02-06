from tkinter import *
import tkinter.messagebox
from flight_search import FlightSearch
from IATA_extraction import city_name, airport_get
from datetime import datetime
from dateutil.relativedelta import relativedelta

THEME_COLOR = "#375362"
FONT = ("italic", 20, 'bold')
FONT_small = ("italic", 12, 'bold')




class FlightUi:
    def __init__(self):
     #   self.whole_new_list = [{'Price': 149, 'Departure_Time': '2021-12-04 5:30', 'Arriving Time': '2021-12-05 9:35', 'Arriving City': 'Paris', 'id': '01880a7c4a150000df2e641b_0|01880a7c4a150000df2e641b_1', 'flyFrom': 'DME', 'flyTo': 'ORY', 'duration': '1h 17m', 'distance': 2511.28}, {'Price': 153, 'Departure_Time': '2021-12-05 2:05', 'Arriving Time': '2021-12-05 1:25', 'Arriving City': 'Paris', 'id': '0188219b4a160000805a2468_0|219b25c34a16000081147871_0|219b25c34a16000081147871_1', 'flyFrom': 'DME', 'flyTo': 'CDG', 'duration': '0h 20m', 'distance': 2484.52}, {'Price': 183, 'Departure_Time': '2021-12-05 7:45', 'Arriving Time': '2021-12-07 7:20', 'Arriving City': 'Paris', 'id': '273e0b774a160000906f042b_0|0b77091e4a17000026af3385_0|091e25584a1700004ce3b9be_0|25580a7c4a180000a65788d2_0', 'flyFrom': 'ZIA', 'flyTo': 'ORY', 'duration': '5h 16m', 'distance': 2527.4}, {'Price': 195, 'Departure_Time': '2021-12-05 7:45', 'Arriving Time': '2021-12-07 7:10', 'Arriving City': 'Paris', 'id': '273e0b774a160000906f042b_0|0b77091e4a17000026af3385_0|091e13d44a180000ade6f66e_0|13d425c34a180000b88b2433_0', 'flyFrom': 'ZIA', 'flyTo': 'CDG', 'duration': '5h 16m', 'distance': 2500.5}]

        global plane_img
        self.flight = FlightSearch()
        self.window = Tk()
        self.window.config(bg="#C2DCDE", padx=20, pady=20)
        self.window.title("Sky search")
        self.window.geometry("1300x900")
        self.window.minsize(1300, 900)
        self.window.maxsize(1300, 900)

        plane_img = PhotoImage(file=r'./ui_files/airplane.png')
        labelBG = Label(self.window, bg="#C2DCDE", image=plane_img).place(x=-70, y=-50)

        self.frame = Frame(self.window)

        # self.canvas = Canvas(self.window, width=960, height=120)
        # self.canvas.config(bg='white')
        #
        # self.canvas.create_image((0, 0), image=plane_img)
        # self.canvas.image = plane_img
        # self.canvas.grid(row=1, column=0, columnspan=2, pady=20)
    #    self.canvas.update()
 #       Label(self.window, image=plane_img).grid(row=1, column=1)
        # self.canvas.config(xpad=20, ypad=20)
        #  self.question_text = self.canvas.create_text(110, 150, text="Pewpew", font=FONT,
        #                                               width=200, fill=THEME_COLOR)

        depart_img = PhotoImage(file=r'./ui_files/departing.png')
        Label(image=depart_img, bg="#C2DCDE").place(x=5, y=150)

        arrive_img = PhotoImage(file=r'./ui_files/arriving.png')
        Label(image=arrive_img, bg="#C2DCDE").place(x=5, y=200)

        dep_int_img = PhotoImage(file=r'./ui_files/dep_time.png')
        Label(image=dep_int_img, bg="#C2DCDE").place(x=5, y=250)
#        Label(text="Дата вылета, до", bg="#C2DCDE").place(x=5, y=300)

        entryText = StringVar()
        entryText.set("Москва")
        self.e0 = Entry(textvariable=entryText, bg='#F0F0F0')
        self.e1 = Entry(bg='#F0F0F0')

        entryText = StringVar()
        moscow_time = datetime.today()
        entryText.set(moscow_time.strftime("%d/%m/%Y"))
        self.e2 = Entry(textvariable=entryText, bg='#F0F0F0')
        self.e3 = Entry(bg='#F0F0F0')

        self.e0.place(x=100, y=158)
        self.e1.place(x=100, y=208)
        self.e2.place(x=100, y=251)
        self.e3.place(x=100, y=283)

        exit_image = PhotoImage(file='./ui_files/exit1.png')
        Button(text='Exit', command=self.window.quit, image=exit_image, foreground='#575b5e', bg='#C2DCDE', highlightbackground = "green", highlightthickness = 2, bd=0).place(x=5, y=330)

        search_image = PhotoImage(file='./ui_files/search2.png')
        Button(text='Search', command=self.Del, image=search_image, foreground='#575b5e', bg='#C2DCDE', highlightbackground = "green", highlightthickness = 2, bd=0).place(x=120, y=330)

        # left_image = PhotoImage(file='./images/false.png')
        #    self.left_button = Button(highlightthickness = 0, bg=THEME_COLOR, command= self.add_item)
        #   self.left_button.grid(row=2, column=0)
        #
        # right_image = PhotoImage(file='./images/true.png')
        # self.right_button = Button(image=right_image, highlightthickness=0, bg=THEME_COLOR, padx=50, pady=50, command=self.press_right_button)
        # self.right_button.grid(row=2, column=1)
        self.table = Listbox(width=80, height=15, font=FONT_small, bg="#C2DCDE", foreground='#575b5e', bd=0, highlightthickness=0)
        self.table.place(x=5, y=510)



        self.window.mainloop()

    def get_entry_fields(self):
        try:
            self.fromPoint = self.e0.get()
            self.destPoint = self.e1.get()
            char_list = ["!", "@", "#", "$", "%", "^", "&", "*", "(", ")", "[", "]", "{", "}", ';', ':', ',', '.', '/',
                         '<', '>', '?', "|", "`", "~", '-', ',', "_", "+"]
            DATE_F = self.e2.get()
            for i in char_list:
                DATE_F = DATE_F.replace(i, "")

            DATE_T = self.e3.get()
            for i in char_list:
                DATE_T = DATE_T.replace(i, "")
        except TypeError:
            pass

        self.DATE_FROM = DATE_F[0:2] + '/' + DATE_F[2:4] + '/' + DATE_F[4:8]
        self.DATE_TO = DATE_T[0:2] + '/' + DATE_T[2:4] + '/' + DATE_T[4:8]

        self.fromPoint = city_name(self.fromPoint)
        departure_city_name = city_name(self.fromPoint)
        self.destPoint = city_name(self.destPoint)
        arriving_city_name = city_name(self.destPoint)

        self.fromPoint = airport_get(self.fromPoint)
        if not self.fromPoint:
            tkinter.messagebox.showinfo("Change home city", "Sorry, looks like there are no major airports in your city")
        self.destPoint = airport_get(self.destPoint)
        if not self.destPoint:
            tkinter.messagebox.showinfo("Change destination city",
                                        "Sorry, looks like in the city you want to get there are no major airports yet")
        full = []
        TEMP_DICT = {}

        scrollbarY = Scrollbar(width=20)
        scrollbarY.place(x=730, y=630)
        scrollbarY.config(command=self.table.yview)
        self.table.config(yscrollcommand=scrollbarY.set)

        scrollbarX = Scrollbar(orient='horizontal', width=20)
        scrollbarX.place(x=280, y=490)
        scrollbarX.config(command=self.table.xview)
        self.table.config(xscrollcommand=scrollbarX.set)
        self.whole_new_list = []

        for f in self.fromPoint:
            for t in self.destPoint:
                TEMP_DICT = self.flight.get_another_flight(f, t, self.DATE_FROM, self.DATE_TO)
                if not TEMP_DICT:
                    tkinter.messagebox.showinfo("Check your date", "Check your dates and try again")
                    quit()
                full.append(TEMP_DICT)
                self.table.insert(END, *TEMP_DICT)
        #self.whole_new_list = [i[0] for i in full]
        for i in full:
            for j in i:
                self.whole_new_list.append(j)
        self.newlist = sorted(self.whole_new_list, key=lambda d: d['Price'])
        self.create_flight(self.whole_new_list)

        self.sort_image = PhotoImage(file='./ui_files/sort_min.png')
        self.sort_button = Button(text='min price sort', image=self.sort_image, command=self.anotherDel, foreground='#C2DCDE', bg='#C2DCDE', highlightbackground = "green", highlightthickness = 2, bd=0).place(x=5, y=480)


    def Del(self):
        self.table.delete(0, END)
        #       self.table.destroy()
        self.get_entry_fields()

    def sort_and_insert(self):
        self.table.insert(END, *self.newlist)
        self.create_flight(self.newlist)

    def anotherDel(self):
        self.table.delete(0, END)
        #       self.table.destroy()
        self.sort_and_insert()

    def create_flight(self, flight_list):
        self.flight_list = flight_list
        self.canvas1 = Canvas(bg="#C2DCDE", width=500, height=802, bd=0, highlightthickness=0)
        self.canvas1.place(x=760, y=5)
        X = 30
        Y = 0
        self.BACKGROUND = "#C2DCDE"

        self.im = PhotoImage(file='./ui_files/flight_label.png')

        y = 0
        for flight in self.flight_list:
            self.label = Label(self.canvas1, image=self.im, compound=LEFT, bg=self.BACKGROUND)
            self.canvas1.create_window(15, y, window=self.label, anchor=NW)

            self.label1 = Label(text=flight['Departure_Time'][-5:], bg=self.BACKGROUND)
            self.canvas1.create_window(25 + X, 45 + Y + y, window=self.label1, anchor=NW)

            self.label2 = Label(text=flight['flyFrom'], bg=self.BACKGROUND)
            self.canvas1.create_window(28 + X, 110 + Y + y, window=self.label2, anchor=NW)

            self.label3 = Label(text=flight['Arriving Time'][-5:], bg=self.BACKGROUND)
            self.canvas1.create_window(290 + X, 45 + Y + y, window=self.label3, anchor=NW)

            self.label4 = Label(text=flight['flyTo'], bg=self.BACKGROUND)
            self.canvas1.create_window(293 + X, 110 + Y + y, window=self.label4, anchor=NW)

            self.label5 = Label(text=f"Time in air {flight['duration']}", bg=self.BACKGROUND)
            self.canvas1.create_window(115 + X, 45 + Y + y, window=self.label5, anchor=NW)

            self.label6 = Label(text=f"Price {flight['Price']} eur ", bg=self.BACKGROUND)
            self.canvas1.create_window(125 + X, 110 + Y + y, window=self.label6, anchor=NW)

            self.label7 = Label(text=f"Departure date  {flight['Departure_Time'][8:10]}-{flight['Departure_Time'][5:7]}", bg=self.BACKGROUND)
            self.canvas1.create_window(105 + X, 15 + Y + y, window=self.label7, anchor=NW)


            y += 200

        scrollbar = Scrollbar(self.canvas1, orient=VERTICAL, command=self.canvas1.yview)
        scrollbar.place(relx=1, rely=0, relheight=1, anchor=NE)
        self.canvas1.config(yscrollcommand=scrollbar.set, scrollregion=(0, 0, 0, y))

