# python-3.7.6-amd64

import sys
from PySide6.QtWidgets import *
from PySide6.QtCore import *
from multiprocessing import Process, Queue, pool
import csv
import os
import configparser
import pyautogui as pag

#DWM Serial Parser by Brian H. | Updated 3/6/19
import serial
import time
import datetime
from scipy.spatial import distance
import numpy as np
from datetime import datetime

import tag_position
import dwm1001
#import uart_shell_commands

#config.ini
#parser = configparser.SafeConfigParser() # for ini file
#parser.read("config.ini") # deployment for ini fil
#sleep_loop = parser.get("sleep", "loop")
#sleep_alarm = parser.get("sleep", "alarm") # threshold value
#sleep_logger = parser.get("sleep", "logger")
#name00 = parser.get("name", "name00") # worker name
#name01 = parser.get("name", "name01") # worker name
#name02 = parser.get("name", "name02") # worker name
#filepath_txt ="data\\管理番号.txt" #filepath for "管理番号": tempolarly path, not important

# while loop, data from MITUTOYO degimatic guage
def loop(q): #OK
    i = []
    #DWM=serial.Serial(port="COM6", baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=0.1, xonxoff=True, rtscts=True, dsrdtr=True) # maximum update rate = 10Hz (0.1s)
    s = dwm1001.shell('COM6') #change this number to suit different setup
    s.dEnter()
    while True:
        s.loop('les')
    s.close()
    print(s)

    #q.put(value)
    #print(value)

# data logger from MITUTOYO device
def logger(q):

    filepath_csv = "D:\\Desktop\\a.txt"

    # read 管理番号 from the txt file
    #f = open(filepath_txt, "r")
    #filepath_csv = f.readline()

    # csv file
    while True:
        value = q.get()
        f = open(filepath_csv, "a")
        writer =csv.writer(f, lineterminator='\n')
        writer.writerow([value])
        f.close()

#necessary file for multiprocessing
class Consumer(QThread):

    poped = Signal(str)

    def __init__(self, q):
        super().__init__()
        self.q = q

    def run(self):
        while True:
            self.poped.emit(q.get())

# GUI
class MyWindow(QMainWindow):

    def __init__(self, q):
        super().__init__()

        self.wo01 = QLineEdit("", self)
        self.wo01.move(20,10)
        self.wo01.resize(400*0.8, 80)
        self.wo01.setPlaceholderText(' 作業用番号') # 透かしで表示
        self.wo01.setStyleSheet("color: black; font: 20pt Arial; border-color: black; "
                                "border-style:solid; border-width: 1.5px; border-radius:10px") # 文字の大きさなど


        self.wk01 = QComboBox(self)
        #self.wk01.addItem(name00)
        self.wk01.move(390,10)
        self.wk01.resize(400*0.8, 80)
        self.wk01.setStyleSheet("color: black; font: 20pt Arial; border-color: white; "
                                "border-style:solid; border-width: 1.5px; border-radius:10px") # 文字の大きさなど

        self.btn01 = QPushButton("計測開始", self)
        self.btn01.move(750, 10)
        self.btn01.resize(400*0.8, 80)
        self.btn01.setStyleSheet("color: black; font: 20pt Arial; border-color: black; "
                                 "border-style:solid; border-width: 1.5px; border-radius:10px") # 文字の大きさなど
        self.btn01.clicked.connect(self.header)

        self.setGeometry(200, 200, 300, 200)

        self.label = QLabel(self)
        self.label.move(0, 100)
        self.label.resize(1366, 400)

        HBox = QHBoxLayout()
        HBox.addWidget(self.wo01)
        HBox.addWidget(self.wk01)
        HBox.addWidget(self.btn01)
        HBox.addWidget(self.label)
        HBox.addStretch(0)

    # header for CSV + logger start
    def header(self):
        # csv header
        self.filepath_csv = filepath_csv + self.wo01.text() + ".csv"

        # to change the file name if the self.wo01.text() is in blank
        if "\.csv" in self.filepath_csv:
            dt = datetime.datetime.now()
            dt1 = dt.strftime('%Y%m%d')
            dt2 = dt.strftime('%H%M%S')
            self.filepath_csv =str(self.filepath_csv).replace('.csv', '')
            filename = str(dt1) + str(dt2) + ".csv"
            self.filepath_csv = filepath_csv + filename

        else:
            pass

        # check the file has been already existed or not, if not save headers.
        if not os.path.exists(self.filepath_csv):
            # write the header
            csvlist = []
            f = open(self.filepath_csv, 'w')
            writer = csv.writer(f, lineterminator='\n')

            writer.writerow(["作業番号", self.wo01.text()])
            writer.writerow(["作業者名", self.wk01.currentText()])
            writer.writerow(["日付","時間","熱変形量[mm]","闘値超え"])

            writer.writerow(csvlist)
            f.close()

        else:
            pass

        # to pass the 作業用番号 to the "def logger": saved in txt file
        with open(filepath_txt, mode="w") as f:
            f.write(self.filepath_csv)

        # thread for data consumer
        self.consumer = Consumer(q)
        self.consumer.poped.connect(self.print_data)
        self.consumer.start()

        # multiprocessing p2 start
        p2.start()

    #@pyqtSlot(str)
    def print_data(self, data):
        #self.statusBar().showMessage(data)

        #print(type(data))
        #if 0 <= float(data) < 0.045:
        #self.label.setText("  " + data)
        #self.styleA = "QWidget{background-color:%s; font: 300pt Arial}" % ("green")
        #self.label.setStyleSheet(self.styleA)

        #elif 0.045 <= float(data) <= 0.049:
        #self.label.setText("  " + data)
        #self.styleA = "QWidget{background-color:%s; font: 300pt Arial}" % ("yellow")
        #self.label.setStyleSheet(self.styleA)

        #elif 0.050 <= float(data) < 100:
        #self.label.setText("  " + data)
        #self.styleA = "QWidget{background-color:%s; font: 300pt Arial}" % ("brown")
        #self.label.setStyleSheet(self.styleA)



        if -100 <= float(data) < 0:
            self.label.setText(" " + data)
            self.styleA = "QWidget{font: 250pt}"
            self.label.setStyleSheet(self.styleA)

        if 0 <= float(data) < 10:
            self.label.setText("  " + data)
            self.styleA = "QWidget{font: 250pt}"
            self.label.setStyleSheet(self.styleA)

        if 10 <= float(data) < 100:
            self.label.setText(" " + data)
            self.styleA = "QWidget{font: 250pt}"
            self.label.setStyleSheet(self.styleA)

        elif float(data) == -100:
            data = " 異常発生"
            self.label.setText(data)
            self.styleA = "QWidget{color:%s; font: 180pt Arial}" % ("brown")
            self.label.setStyleSheet(self.styleA)


if __name__ == "__main__":

    q = Queue()

    with pool.Pool(processes=3) as p:

        #multiprocessing
        p0 = p.Process(target=loop, args=(q, ), daemon=True)
        #p1 = p.Process(target=alarm, args=(q, ), daemon=True)
        p1 = p.Process(target=logger, args=(q, ), daemon=True)

        p0.start()
        p1.start()

    # Main process
    app = QApplication(sys.argv)
    mywindow = MyWindow(q)
    mywindow.setWindowTitle("熱変形量監視ソフト Version 0.0.0") # windowのtitle
    #mywindow.showFullScreen()

    scr_w,scr_h= pag.size() #LCD resolution

    mywindow.setFixedSize(scr_w*0.8, scr_h*0.8)  # windows size based on LCD resolution
    mywindow.show()
    app.exec()