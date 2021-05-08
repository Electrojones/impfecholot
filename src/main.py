# -*- coding: utf-8 -*-

from tkinter import *

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

from selenium.webdriver.firefox.options import Options as FirefoxOptions

import json
import time
import random
import os
import threading

import simpleaudio as sa


import keyboard






detectors=[]

class echolot:
    def __init__ (self, url):
        self.url=url

        global stop_alarm
        global discard_appointment

        stop_alarm = False
        discard_appointment = False

        #options = webdriver.ChromeOptions()
        #options.add_argument("/home/jonas/.config/chromium/Default")

        #self.driver=webdriver.Chrome(executable_path='../impfecholot/chromedriver', options=options)
        folder=(os.getcwd().split("/")[-1]).split("\\")[-1]
        self.driver=webdriver.Chrome(executable_path='../'+folder+'/chromedriver')

        self.driver.minimize_window()

        self.driver.implicitly_wait(10)

        self.driver.get(self.url)

        self.driver.implicitly_wait(10)

        try:
            self.elem=self.driver.find_element_by_xpath("/html/body/app-root/div/div/div/div[2]/div[2]/div/div[1]/a")#("html body app-root div.app-wrapper app-page-its-login div.d-flex.flex-column div.page-ets div.container app-its-login-user div.row.no-gutters div.col-10.offset-1 app-corona-vaccination div.row.no-gutters div.col-12 div.ets-radio-wrapper.cv-radio-wrapper label.ets-radio-control input.form-check-input.ng-untouched.ng-valid.ng-dirty")
            self.elem.click()
        except Exception:
            wstatus.config(text="Status: Error! Der Cookiehinweis konnte nicht weggeklickt werde. Vermutlich hängst du im Warteraum. Wenn dies der Fall ist brauchst du nichts weiter zu tun. Wenn dies nicht der Fall ist kann ein Neustart helfen.")
            root.update()
            root.update_idletasks()    

    
    def detect(self):
        try:
            self.elem=self.driver.find_element_by_xpath("/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[2]/div/div/label[2]")#("html body app-root div.app-wrapper app-page-its-login div.d-flex.flex-column div.page-ets div.container app-its-login-user div.row.no-gutters div.col-10.offset-1 app-corona-vaccination div.row.no-gutters div.col-12 div.ets-radio-wrapper.cv-radio-wrapper label.ets-radio-control input.form-check-input.ng-untouched.ng-valid.ng-dirty")
            self.elem.click()
        except Exception:
            wstatus.config(text="Status: Error! Es konnten keine Impftermine abgefragt werden. Vermutlich hängst du im Warteraum. Wenn dies der Fall ist brauchst du nichts weiter zu tun. Wenn dies nicht der Fall ist kann ein Neustart helfen.")
            root.update()
            root.update_idletasks() 

        time.sleep(6)

        if "keine freien Termine" in self.driver.page_source:
            print("Nix da")
            wstatus.config(text="Status: Kein Termin verfügbar")
            root.update()
            root.update_idletasks()

        elif  "Krankenversicherung" in self.driver.page_source or "Lebensjahr" in self.driver.page_source or "landesspezifischen" in self.driver.page_source: #"Krankenversicherung"
            global discard_appointment
            wstatus.config(text="Status: TERMIN VERFÜGBAR!!!!")
            root.update()
            root.update_idletasks()
            thread = threading.Thread(target=alarm)
            thread.start()
            self.driver.maximize_window()
            while True:
                wstatus.config(text="Status: Termin verwerfen?")
                root.update()
                root.update_idletasks()
                print("werfen?")
                if discard_appointment:
                    wstatus.config(text="Status: Termin verworfen")
                    root.update()
                    root.update_idletasks()
                    discard_appointment=False
                    break
            
            
        else:
            wstatus.config(text="Status: Error! (Vermutlich ist der Server überlastet)")
            root.update()
            root.update_idletasks()
            print("ERROR!")


def alarm():
    wave_obj = sa.WaveObject.from_wave_file("alarm.wav")
    play_obj = wave_obj.play()
    """while play_obj.is_playing():
        #print("Playing...")
        if stop_alarm:
            #print("stopping")
            play_obj.stop()
            stop_alarm=False
            break"""



"""urls=["https://003-iz.impfterminservice.de/impftermine/service?plz=72072", 
"https://229-iz.impfterminservice.de/impftermine/service?plz=70629", 
"https://229-iz.impfterminservice.de/impftermine/service?plz=72469", 
"https://005-iz.impfterminservice.de/impftermine/service?plz=72762", 
"https://229-iz.impfterminservice.de/impftermine/service?plz=89584"]"""


def end():
    print("Ending..")
    for detector in detectors:
        detector.driver.quit()

def stop_alarm_meth():
    stop_alarm=True

def discard():
    print("werf")
    global discard_appointment
    discard_appointment= True
    print(discard_appointment)



def start():
    root.update()
    root.update_idletasks()
    urls=e.get().split("!")
    while True:
        

        for url in urls:
            detectors.append(echolot(url))

        for _ in range(15):
            for detector in detectors:
                state=detector.detect()
                time.sleep(7)

        end()

root = Tk()

w, h = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (w, h))

w = Label(root, text="▼ Hier kannst du die Links zu den Terminseiten einfügen ▼\n(Wenn du mehrere Seiten prüfen möchtest: Trenne die Links mit einem Ausrufezeichen (LinkzuImpfseite!LinkzuImpfseite!LinkzuImpfseite)")
w.pack()


e =Entry(root, width=500)
e.pack()

bstart = Button(root, text="Terminsuche starten", command=start)
bstart.pack()

bstop = Button(root, text="Alarm stoppen", command=stop_alarm_meth)
bstop.pack()

bdisc = Button(root, text="Impftermin verwerfen", command=discard)
bdisc.pack()

wstatus = Label(root, text="Status: Bereit")
wstatus.pack()

#w.config(text="neuer text")

#root.mainloop()

root.update()
root.update_idletasks()

"""urls=["https://003-iz.impfterminservice.de/impftermine/service?plz=72072", 
"https://229-iz.impfterminservice.de/impftermine/service?plz=70629", 
"https://229-iz.impfterminservice.de/impftermine/service?plz=72469", 
"https://005-iz.impfterminservice.de/impftermine/service?plz=72762", 
"https://229-iz.impfterminservice.de/impftermine/service?plz=89584"]"""

root.mainloop()

#w.config(text="neuer text")
