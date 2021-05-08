# -*- coding: utf-8 -*-

from tkinter import *
import echolot


def click():
    print("click!")

root = Tk()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

w = Label(root, text="▼ Hier kannst du die Links zu den Terminseiten einfügen ▼\n(Wenn du mehrere Seiten prüfen möchtest: Trenne die Links mit einem Ausrufezeichen (LinkzuImpfseite!LinkzuImpfseite!LinkzuImpfseite)")
w.pack()


e =Entry(root, width=500)
e.pack()

b = Button(root, text="Terminsuche starten", command=click)
b.pack()

b = Button(root, text="Alarm stoppen", command=click)
b.pack()

b = Button(root, text="Impftermin verwerfen", command=click)
b.pack()

#w.config(text="neuer text")

#root.mainloop()

root.update()
root.update_idletasks()

w.config(text="neuer text")

while True:
    root.update()
    root.update_idletasks()
