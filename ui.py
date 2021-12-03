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
        self.flight = FlightSearch()
        self.window = Tk()
        self.window.config(bg=THEME_COLOR, padx=20, pady=20)
        self.window.title("Sky search")
        self.window.geometry("850x600")

        self.canvas = Canvas(width=600, height=400)
        self.canvas.config(bg='white')
        # self.canvas.config(xpad=20, ypad=20)
        #  self.question_text = self.canvas.create_text(110, 150, text="Pewpew", font=FONT,
        #                                               width=200, fill=THEME_COLOR)
        self.canvas.grid(row=1, column=0, columnspan=2, pady=8)

        Label(self.canvas, text="Город вылета", bg="white").grid(row=0)
        Label(self.canvas, text="Город прилёта", bg="white").grid(row=1)
        Label(self.canvas, text="Дата вылета", bg="white").grid(row=2)
        Label(self.canvas, text="Дата вылета, до", bg="white").grid(row=3)

        entryText = StringVar()
        entryText.set("Москва")
        self.e0 = Entry(self.canvas, textvariable=entryText)
        self.e1 = Entry(self.canvas)

        entryText = StringVar()
        moscow_time = datetime.today() + relativedelta(hours=+3)
        entryText.set(moscow_time.strftime("%d/%m/%Y"))
        self.e2 = Entry(self.canvas, textvariable=entryText)
        self.e3 = Entry(self.canvas)

        self.e0.grid(row=0, column=1)
        self.e1.grid(row=1, column=1)
        self.e2.grid(row=2, column=1)
        self.e3.grid(row=3, column=1)

        Button(self.canvas, text='Quit', command=self.window.quit).grid(row=4, column=0, sticky=W, pady=5, padx=80)
        Button(self.canvas, text='Find', command=self.Del).grid(row=4, column=1, sticky=W, pady=4, padx=60)
        Button(self.window, text='min price sort', command=self.anotherDel).grid(row=2, column=1, sticky=W, pady=4,
                                                                                 padx=0)

        # left_image = PhotoImage(file='./images/false.png')
        #    self.left_button = Button(highlightthickness = 0, bg=THEME_COLOR, command= self.add_item)
        #   self.left_button.grid(row=2, column=0)
        #
        # right_image = PhotoImage(file='./images/true.png')
        # self.right_button = Button(image=right_image, highlightthickness=0, bg=THEME_COLOR, padx=50, pady=50, command=self.press_right_button)
        # self.right_button.grid(row=2, column=1)
        self.table = Listbox(self.window, width=80, height=15, font=FONT_small)
        self.table.grid(row=3, column=1)

        scrollbarY = Scrollbar(self.window, width=20)
        scrollbarY.grid(row=3, column=2)
        scrollbarY.config(command=self.table.yview)
        self.table.config(yscrollcommand=scrollbarY.set)

        scrollbarX = Scrollbar(self.window, orient='horizontal', width=20)
        scrollbarX.grid(row=2, column=1)
        scrollbarX.config(command=self.table.xview)
        self.table.config(xscrollcommand=scrollbarX.set)

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

        self.DATE_FROM = DATE_F[0:2] + '/' + DATE_F[2:4] + '/' + DATE_F[4:]
        self.DATE_TO = DATE_T[0:2] + '/' + DATE_T[2:4] + '/' + DATE_T[4:]

        self.fromPoint = city_name(self.fromPoint)
        departure_city_name = city_name(self.fromPoint)
        self.destPoint = city_name(self.destPoint)
        arriving_city_name = city_name(self.destPoint)

        self.fromPoint = airport_get(self.fromPoint)
        if not self.fromPoint:
            tkinter.messagebox.showinfo("Change home city", "Sorry, looks like there is no major airports in your city")
        self.destPoint = airport_get(self.destPoint)
        if not self.destPoint:
            tkinter.messagebox.showinfo("Change destination city",
                                        "Sorry, looks like in the city you want to get there is no major airports yet")
        full = []
        TEMP_DICT = {}

        for f in self.fromPoint[0:2]:
            for t in self.destPoint[0:2]:
                TEMP_DICT = self.flight.get_another_flight(f, t, self.DATE_FROM, self.DATE_TO)
                if not TEMP_DICT:
                    tkinter.messagebox.showinfo("Check your date", "Check your dates and try again")
                    quit()
                full.append(TEMP_DICT)
                print(TEMP_DICT)
                self.table.insert(END, *TEMP_DICT)
        whole_new_list = [i[0] for i in full]
        self.newlist = sorted(whole_new_list, key=lambda d: d['Price'])

    def Del(self):
        self.table.delete(0, END)
        #       self.table.destroy()
        self.get_entry_fields()

    def sort_and_insert(self):
        self.table.insert(END, *self.newlist)

    def anotherDel(self):
        self.table.delete(0, END)
        #       self.table.destroy()
        self.sort_and_insert()
