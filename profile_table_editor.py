# -*- coding: utf-8 -*-

'''Editing window to change profiles'''

import tkinter as Tkinter
import colours as c
import strings as s
from termite_profile import Profile

TEXT_FONT_1 = ("Arial", 10, "bold")
TEXT_FONT_2 = ("Arial", 16, "bold")
TEXT_FONT_3 = ("Arial", 8, "bold")

class LabelWidget(Tkinter.Entry):
    '''columns and row label'''
    def __init__(self, master, x, y, text):
        self.text = Tkinter.StringVar()
        self.text.set(text)
        Tkinter.Entry.__init__(self, master=master)
        self.config(relief="flat", font=TEXT_FONT_1,
                    bg="#ffffff000", fg="#fffffffff",
                    readonlybackground=c.readonlybackground,
                    justify='center', width=5,
                    textvariable=self.text,
                    state="readonly")
        self.grid(column=x, row=y)

class EntryWidget(Tkinter.Entry):
    '''editable entry'''
    def __init__(self, master, x, y):
        Tkinter.Entry.__init__(self, master=master)
        self.value = Tkinter.StringVar()
        self.config(textvariable=self.value, width=5,
                    relief="flat", font=TEXT_FONT_1,
                    bg="#fffffffff", fg="#000000000",
                    justify='center')
        self.grid(column=x, row=y)
        self.value.set("")

class ProfileEntryGrid(Tkinter.Tk):
    ''' Dialog box with Entry widgets arranged in columns and rows.'''
    def __init__(self, col_list, row_list, profile):
        self.cols = col_list[:]
        self.col_list = col_list[:]
        self.col_list.insert(0, "")
        self.row_list = row_list
        Tkinter.Tk.__init__(self)
        self.title("Editor: " + a.name)

        self.profile = profile

        #The MenuBar
        menubar = Tkinter.Menu(self)
        menubar.add_command(label="Hello", command=self.hello)
        menubar.add_command(label="Quit", command=self.destroy)

        self.mainframe = Tkinter.Frame(self)
        self.mainframe.config(padx='0.0m', pady='0.0m', bg=c.bg)
        self.mainframe.grid()
        self.make_header()

        self.config(menu=menubar)

        self.grid_dict = {}
        for i in range(1, len(self.col_list)):
            for j in range(len(self.row_list)):
                w = EntryWidget(self.mainframe, i, j+1)
                self.grid_dict[(i-1, j)] = w.value
                def handler(event, col=i-1, row=j):
                    return self.__entryhandler(col, row)
                w.bind(sequence="<FocusOut>", func=handler)
        self.populate()
        self.mainloop()

    def hello(self):
        print("Hello World")

    def populate(self):
        '''populate the grid with the profile information'''
        print("populating")
        for i in range(len(self.cols)):
            for j in range(len(self.row_list)):
               #sleep(0.25)
                self.set(i, j, "")
                self.update_idletasks()
                #sleep(0.1)
                self.set(i, j, self.profile.values[j, i])
                self.update_idletasks()


    def make_header(self):
        self.hdr_dict = {}
        for i, label in enumerate(self.col_list):
            def handler(event, col=i, row=0, text=label):
                return self.__headerhandler(col, row, text)
            w = LabelWidget(self.mainframe, i, 0, label)
            self.hdr_dict[(i, 0)] = w
            w.bind(sequence="<KeyRelease>", func=handler)

        for i, label in enumerate(self.row_list):
            def handler(event, col=0, row=i+1, text=label):
                return self.__headerhandler(col, row, text)
            w = LabelWidget(self.mainframe, 0, i+1, label)
            self.hdr_dict[(0, i+1)] = w
            w.bind(sequence="<KeyRelease>", func=handler)

    def __entryhandler(self, col, row):
        s = self.grid_dict[(col, row)].get()
        if s.upper().strip() == "EXIT":
            self.destroy()
        elif s.upper().strip() == "DEMO":
            self.demo()
        elif s.strip():
            print(s)
            self.profile.values[row, col] = float(s)


    def demo(self):
        ''' enter a number into each Entry field '''
        #a = Profile()
        #a.set_always_on()
        for i in range(len(self.cols)):
            for j in range(len(self.row_list)):
               #sleep(0.25)
                self.set(i, j, "")
                self.update_idletasks()
                #sleep(0.1)
                self.set(i, j, 1+j+i)
                self.update_idletasks()

    def __headerhandler(self, col, row, text):
        ''' has no effect when Entry state=readonly '''
        self.hdr_dict[(col, row)].text.set(text)

    def get(self, x, y):
        return self.grid_dict[(x, y)].get()

    def set(self, x, y, v):
        if v is None or "":
            val = "→"
        else:
            val = v
        self.grid_dict[(x, y)].set(val)
        return v

if __name__ == "__main__":
    a = Profile()
    a.set_always_on()
    cols = s.TIMESOFDAY
    rows = s.DAYSOFTHEWEEK
    app = ProfileEntryGrid(cols, rows, a)
    print(a.values)
