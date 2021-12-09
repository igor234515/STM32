import sys
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel
from PyQt5.QtSerialPort import QSerialPort, QSerialPortInfo
from PyQt5.QtCore import QIODevice
from pyqtgraph import PlotWidget
import pyqtgraph as pg

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        uic.loadUi("terminal.ui", self)
        self.setWindowTitle('GUI')
       
        self.serial = QSerialPort()
        self.serial.setBaudRate(115200)
        portList = []
        portType = []
        ports = QSerialPortInfo().availablePorts()
        for port in ports:
            portList.append(port.portName())
            portType.append(port.description())

        print(portList)
        print(portType)
        self.comL.addItems(portList)
        self.OpenB.clicked.connect(self.onOpen)
        self.CloseB.clicked.connect(self.onClose)
        self.serial.readyRead.connect(self.onRead)
        self.LED_blue.stateChanged.connect(self.ledControl_blue)
        self.LED_red.stateChanged.connect(self.ledControl_red)
        self.LED_green.stateChanged.connect(self.ledControl_green)
        self.listX = []
        self.listY = []
        for i in range(100): self.listX.append(i)
        for i in range(100): self.listY.append(0)

    def onOpen(self):
        self.serial.setPortName(self.comL.currentText())
        self.serial.open(QIODevice.ReadWrite)
        print('Serial port COM8 opened')

    def onClose(self):
        self.serial.close()
        print('Serial port COM8 closed')

    def onRead(self):
        rx = self.serial.readLine()
        rxs = str(rx, 'utf-8').strip()
        data = rxs.split('.')
        self.listY = self.listY[1:]
        self.listY.append(int(data[0]))
        self.graph.clear()
        self.graph.plot(self.listX, self.listY)


    def serialSend(self, data):
        txs = data
        self.serial.write(txs)

    def ledControl_blue(self, val):
        message = b'\xAB\xA1\x01'
        self.serialSend(message)

    def ledControl_red(self, val):
        message = b'\xAB\xA2\x01'
        self.serialSend(message)

    def ledControl_green(self, val):
        message = b'\xAB\xA3\x01'
        self.serialSend(message)

def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec())

application()