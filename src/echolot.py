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


stop_alarm = False

class echolot:
    def __init__ (self, url):
        self.url=url

        #options = webdriver.ChromeOptions()
        #options.add_argument("/home/jonas/.config/chromium/Default")

        #self.driver=webdriver.Chrome(executable_path='../impfecholot/chromedriver', options=options)
        self.driver=webdriver.Chrome(executable_path='../impfecholot/chromedriver')

        self.driver.minimize_window()

        self.driver.implicitly_wait(10)

        self.driver.get(self.url)

        self.driver.implicitly_wait(10)

        try:
            self.elem=self.driver.find_element_by_xpath("/html/body/app-root/div/div/div/div[2]/div[2]/div/div[1]/a")#("html body app-root div.app-wrapper app-page-its-login div.d-flex.flex-column div.page-ets div.container app-its-login-user div.row.no-gutters div.col-10.offset-1 app-corona-vaccination div.row.no-gutters div.col-12 div.ets-radio-wrapper.cv-radio-wrapper label.ets-radio-control input.form-check-input.ng-untouched.ng-valid.ng-dirty")
            self.elem.click()
        except Exception:
            pass    

    
    def detect(self):
        try:
            self.elem=self.driver.find_element_by_xpath("/html/body/app-root/div/app-page-its-login/div/div/div[2]/app-its-login-user/div/div/app-corona-vaccination/div[2]/div/div/label[2]")#("html body app-root div.app-wrapper app-page-its-login div.d-flex.flex-column div.page-ets div.container app-its-login-user div.row.no-gutters div.col-10.offset-1 app-corona-vaccination div.row.no-gutters div.col-12 div.ets-radio-wrapper.cv-radio-wrapper label.ets-radio-control input.form-check-input.ng-untouched.ng-valid.ng-dirty")
            self.elem.click()
        except Exception:
            pass

        time.sleep(6)

        if "keine freien Termine" in self.driver.page_source:
            print("Nix da")

        elif  "Krankenversicherung" in self.driver.page_source or "Lebensjahr" in self.driver.page_source or "landesspezifischen" in self.driver.page_source: #"Krankenversicherung"
            print(".")
            global stop_alarm
            thread = threading.Thread(target=alarm)
            thread.start()
            self.driver.maximize_window()
            input("Termiiiiiin!!!!!!!!!!!!!!!\nEnter stoppt den Alarm!")
            stop_alarm=True
            input("Mit Enter das Impfangebot verlassen und weiter machen...")
            stop_alarm=False
            
            
        else:
            print("ERROR!")


def alarm():
    wave_obj = sa.WaveObject.from_wave_file("alarm.wav")
    play_obj = wave_obj.play()
    while play_obj.is_playing():
        #print("Playing...")
        if stop_alarm:
            #print("stopping")
            play_obj.stop()
            break



"""urls=["https://003-iz.impfterminservice.de/impftermine/service?plz=72072", 
"https://229-iz.impfterminservice.de/impftermine/service?plz=70629", 
"https://229-iz.impfterminservice.de/impftermine/service?plz=72469", 
"https://005-iz.impfterminservice.de/impftermine/service?plz=72762", 
"https://229-iz.impfterminservice.de/impftermine/service?plz=89584"]"""


def end():
    print("Ending..")
    for detector in detectors:
        detector.driver.quit()


def start(urls):
    while True:
        detectors=[]

        for url in urls:
            detectors.append(echolot(url))

        for _ in range(15):
            for detector in detectors:
                state=detector.detect()
                time.sleep(7)

        end()