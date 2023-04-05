import sys
import os
import glob
import serial
import numpy as np
import queue

from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5 import uic
from PyQt5.QtCore import pyqtSlot

from NiRS485Modbus import *
from Constants import *

TIMER_UPDATE_INTERVAL = 500 # [msec]

# Define function to import external files when using PyInstaller.
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def ScanforPorts():
    """ Lists serial port names
        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')
    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result

class NiMotorControlUI(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        ''' Load UI Window'''
        self.ui = uic.loadUi(resource_path('MultiMotorUI_V1.0.0.ui'),self) #uic.loadUi('MotorUI_V1.1.0.ui', self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(resource_path('iqmed.ico')), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.setWindowIcon(icon)
        self.setWindowTitle("Heart in Box (Demo version)")
        # self.resize(250,750)
        self.show()

        ''' Detecing available Serial Ports'''
        self.availablePorts = ScanforPorts()
        if len(self.availablePorts):
            self.updatePortList()

        ''' Parameters '''
        self.OPEN_BUTTON_STATE = True
        self.START_ALL_BUTTON_STATE = True
        self.START_SINGLE_BUTTONS_STATE_LIST = [True, True, True, True]
        
        ''' Initilizing RS-485 Modbus Connection'''
        self.motorbus = RS485Modbus

        ''' Slot & Signal Connections'''
        self.btnOpen.clicked.connect(self.open_callback)
        self.btnStartAll.clicked.connect(self.start_all_callback)
        self.btnStart1.clicked.connect(self.start1_callback)
        self.btnStart2.clicked.connect(self.start2_callback)
        self.btnStart3.clicked.connect(self.start3_callback)
        self.btnStart4.clicked.connect(self.start4_callback)
        self.lnTargetSpeed1.returnPressed.connect(self.update_targetSpeed1)
        self.lnTargetSpeed2.returnPressed.connect(self.update_targetSpeed2)
        self.lnTargetSpeed3.returnPressed.connect(self.update_targetSpeed3)
        self.lnTargetSpeed4.returnPressed.connect(self.update_targetSpeed4)
        self.cbRotation1.currentIndexChanged.connect(self.update_rotation1)
        self.cbRotation2.currentIndexChanged.connect(self.update_rotation2)
        self.cbRotation3.currentIndexChanged.connect(self.update_rotation3)
        self.cbRotation4.currentIndexChanged.connect(self.update_rotation4)

        ''' lists of QWidget'''
        self.btnStart = [self.btnStart1, self.btnStart2, self.btnStart3, self.btnStart4]
        self.lnTargetSpeed = [self.lnTargetSpeed1,self.lnTargetSpeed2,self.lnTargetSpeed3,self.lnTargetSpeed4]
        self.cbRotation = [self.cbRotation1,self.cbRotation2,self.cbRotation3,self.cbRotation4]
        self.lslbActualSpeed = [self.lbActualSpeed1,self.lbActualSpeed2,self.lbActualSpeed3,self.lbActualSpeed4]
        self.lslbStatus = [self.lbStatus1,self.lbStatus2,self.lbStatus3,self.lbStatus4]
        self.lslbTemp = [self.lbTemp1,self.lbTemp2,self.lbTemp3,self.lbTemp4]
        self.lslbRatedCurrent = [self.lbRatedCurrent1, self.lbRatedCurrent2, self.lbRatedCurrent3, self.lbRatedCurrent4]
        self.lslbActualCurrent = [self.lbActualCurrent1, self.lbActualCurrent2, self.lbActualCurrent3, self.lbActualCurrent4]
        self.lslbBusVoltage = [self.lbBusVoltage1, self.lbBusVoltage2, self.lbBusVoltage3, self.lbBusVoltage4]
        self.lslbPower = [self.lbPower1, self.lbPower2, self.lbPower3, self.lbPower4]

    ''' Callback Functions'''
    def updatePortList(self):
        self.cbSerialPort.addItems(self.availablePorts)
    
    def open_callback(self):
        if self.OPEN_BUTTON_STATE:
            self.btnOpen.setText("CLOSE")
            self.OPEN_BUTTON_STATE = False
            self.cbSerialPort.setEnabled(False)
            self.cbBaudRate.setEnabled(False)
            # Creating modbus object and check bus connection
            self.motorbus = RS485Modbus(name='NiMotorBus',port=self.cbSerialPort.currentText(),
                                        nMotor=4, baudrate=BAUD_RATE_DICT[self.cbBaudRate.currentIndex()])
            self.uiTimerThread = infoUpdateThread
            if len(self.motorbus.motorAddrs):
                self.lsMotors.setEnabled(True)
                for idx,addr in enumerate(self.motorbus.motorAddrs):
                    self.lsMotors.addItem("Motor {} -- ID: {}".format(idx+1,addr))
                    self.btnStart[idx].setEnabled(True)
                    self.lnTargetSpeed[idx].setEnabled(True)
                    self.cbRotation[idx].setEnabled(True)
                self.btnStartAll.setEnabled(True)

                self.uiTimerThread = infoUpdateThread(self, self.motorbus.motors)
                self.uiTimerThread.moveToThread(QtCore.QThread())
            else:
                self.lsMotors.clear()
                self.lsMotors.addItem("No motor detected")
        else:
            if len(self.motorbus.motorAddrs):
                for idx,motor in enumerate(self.motorbus.motors):
                    motor.stop()
                    self.btnStart[idx].setEnabled(False)
                    self.lnTargetSpeed[idx].setEnabled(False)
                    self.cbRotation[idx].setEnabled(False)
                    self.btnStart[idx].setText("Start")
                    self.START_SINGLE_BUTTONS_STATE_LIST[idx] = True
                self.btnStartAll.setText("Start All Motors")
                self.START_ALL_BUTTON_STATE = True
                self.uiTimerThread.stop()
                self.uiTimerThread.terminate()
                self.uiTimerThread.wait()
            self.lsMotors.clear()
            self.btnOpen.setText("OPEN")
            self.OPEN_BUTTON_STATE = True
            # Closeing modbus object and check bus connection
            self.lsMotors.setEnabled(False)
            self.cbSerialPort.setEnabled(True)
            self.cbBaudRate.setEnabled(True)

            self.setUIToDefault()

            self.btnStartAll.setEnabled(False)
            if self.motorbus.isConnected():
                self.motorbus.closePort()
    
    def start_all_callback(self):
        if self.START_ALL_BUTTON_STATE:
            self.btnStartAll.setText("Stop All Motors")
            self.START_ALL_BUTTON_STATE = False
            # Start all connecting motors with configured speeds
            _listTargetSpeed = self.getAllSpeeds()
            _listRotation = self.getAllRotations()
            for idx,motor in enumerate(self.motorbus.motors):
                motor.setTargetSpeed(speed=_listTargetSpeed[idx] , rotation=_listRotation[idx])
                motor.start()
                self.btnStart[idx].setText("Stop")
                self.START_SINGLE_BUTTONS_STATE_LIST[idx] = False
        else:
            self.btnStartAll.setText("Start All Motors")
            self.START_ALL_BUTTON_STATE = True
            # Start all connecting motors with configured speeds
            for idx,motor in enumerate(self.motorbus.motors):
                motor.stop()
                self.btnStart[idx].setText("Start")
                self.START_SINGLE_BUTTONS_STATE_LIST[idx] = True
    
    def closeEvent(self, event):
        if not self.OPEN_BUTTON_STATE:
            for motor in self.motorbus.motors:
                motor.stop()
            self.btnStartAll.setText("Start All Motors")
            self.START_ALL_BUTTON_STATE = True
            self.lsMotors.clear()
            self.OPEN_BUTTON_STATE = True
            # Creating modbus object and check bus connection
            self.lsMotors.setEnabled(False)
            self.btnStartAll.setEnabled(False)
            self.uiTimerThread.stop()
            self.uiTimerThread.terminate()
            self.uiTimerThread.wait()   
            if self.motorbus.isConnected():
                self.motorbus.closePort()
    
    def setUIToDefault(self):
        for idx,motor in enumerate(self.motorbus.motors):
            self.lslbActualSpeed[idx].setText("0")
            self.lslbStatus[idx].setText("N/A")
            self.lslbTemp[idx].setText("0")
            self.lslbRatedCurrent[idx].setText("0")
            self.lslbActualCurrent[idx].setText("0")
            self.lslbBusVoltage[idx].setText("0")
            self.lslbPower[idx].setText("0")

    ''' Individual Motor Starting related functions'''
    def startSingleMotor(self,motorIdx, btnStartObj, lnSpeedObj, cbRotationObj):
        if self.START_SINGLE_BUTTONS_STATE_LIST[motorIdx]:
            # Button Status
            btnStartObj.setText("Stop")
            self.START_SINGLE_BUTTONS_STATE_LIST[motorIdx] = False
            self.btnStartAll.setText("Stop All Motors")
            self.START_ALL_BUTTON_STATE = False
            # Starting a motor
            _rotation = cbRotationObj.currentText()
            _speed = int(lnSpeedObj.text())
            self.motorbus.motors[motorIdx].setTargetSpeed(_speed,rotation=_rotation)
            self.motorbus.motors[motorIdx].start()
        else:
            # Button Status
            btnStartObj.setText("Start")
            self.START_SINGLE_BUTTONS_STATE_LIST[motorIdx] = True
            if all(self.START_SINGLE_BUTTONS_STATE_LIST):
                self.btnStartAll.setText("Start All Motors")
                self.START_ALL_BUTTON_STATE = True
            # Stopping a motor
            self.motorbus.motors[motorIdx].stop()
    def start1_callback(self):
        self.startSingleMotor(0, self.btnStart1, self.lnTargetSpeed1, self.cbRotation1)
        return True
    def start2_callback(self):
        self.startSingleMotor(1, self.btnStart2, self.lnTargetSpeed2, self.cbRotation2)
        return True
    def start3_callback(self):
        self.startSingleMotor(2, self.btnStart3, self.lnTargetSpeed3, self.cbRotation3)
        return True
    def start4_callback(self):
        self.startSingleMotor(3, self.btnStart4, self.lnTargetSpeed4, self.cbRotation4)
        return True

    ''' Changing Target Speed related functions'''
    def set_targetSpeed(self,motorIdx, lnSpeedObj, cbRotationObj):
        try:
            _targetSpeed = int(lnSpeedObj.text())
            if _targetSpeed >= self.motorbus.motors[motorIdx].maxSpeed:
                _targetSpeed = self.motorbus.motors[motorIdx].maxSpeed-1
                lnSpeedObj.setText(str(_targetSpeed))
            self.motorbus.motors[motorIdx].setTargetSpeed(_targetSpeed, rotation=cbRotationObj.currentText())
            return
        except:
            pass
    def update_targetSpeed1(self):
        self.set_targetSpeed(0, self.lnTargetSpeed1, self.cbRotation1)
        return True
    def update_targetSpeed2(self):
        self.set_targetSpeed(1, self.lnTargetSpeed2, self.cbRotation2)
        return True
    def update_targetSpeed3(self):
        self.set_targetSpeed(2, self.lnTargetSpeed3, self.cbRotation3)
        return True
    def update_targetSpeed4(self):
        self.set_targetSpeed(3, self.lnTargetSpeed4, self.cbRotation4)
        return True 
    
    ''' Changing Rotational Direction related functions'''
    def set_rotation(self,motorIdx, lnSpeedObj, cbRotationObj):
        _rotation = cbRotationObj.currentText()
        _speed = int(lnSpeedObj.text())
        try:
            self.motorbus.motors[motorIdx].setTargetSpeed(_speed,rotation=_rotation)
        except:
            pass
    def update_rotation1(self):
        self.set_rotation(0, self.lnTargetSpeed1, self.cbRotation1)
        return True
    def update_rotation2(self):
        self.set_rotation(1, self.lnTargetSpeed2, self.cbRotation2)
        return True
    def update_rotation3(self):
        self.set_rotation(2, self.lnTargetSpeed3, self.cbRotation3)
        return True
    def update_rotation4(self):
        self.set_rotation(3, self.lnTargetSpeed4, self.cbRotation4)
        return True
    
    ''' Coleecting all related QWidgets Functions'''
    def getAllSpeeds(self):
        return [int(self.lnTargetSpeed1.text()),int(self.lnTargetSpeed2.text()),int(self.lnTargetSpeed3.text()),int(self.lnTargetSpeed4.text())]
    
    def getAllRotations(self):
        return [self.cbRotation1.currentText(),self.cbRotation2.currentText(),self.cbRotation3.currentText(),self.cbRotation4.currentText()]

class infoUpdateThread(QtCore.QThread):
    def updateInfo(self):
        for idx,motor in enumerate(self.Motors):
            motor.updateValue()
            self.MainWindow.lslbActualSpeed[idx].setText("{}".format(motor.actualSpeed))
            self.MainWindow.lslbStatus[idx].setText("{}, [{}]".format(motor.statusDict, motor.status))
            self.MainWindow.lslbTemp[idx].setText("{}".format(motor.temp))
            self.MainWindow.lslbRatedCurrent[idx].setText("{:.3f}".format(motor.ratedCurrent))
            self.MainWindow.lslbActualCurrent[idx].setText("{:.5f}".format(motor.actualCurrent))
            self.MainWindow.lslbBusVoltage[idx].setText("{:.2f}".format(motor.busVoltage))
            self.MainWindow.lslbPower[idx].setText("{:.5f}".format(motor.power))
    
    def __init__(self, mainWindowObj,lsMotorObj):
        self.Motors = lsMotorObj
        self.MainWindow = mainWindowObj
        super(infoUpdateThread, self).__init__()
        self.timerInterval = TIMER_UPDATE_INTERVAL
        self.uiTimer = QtCore.QTimer()
        self.uiTimer.setInterval(self.timerInterval)
        # self.uiTimer.moveToThread(self)
        self.uiTimer.timeout.connect(self.updateInfo)
        self.run()
    
    def run(self):
        self.uiTimer.start()
    
    def stop(self):
        self.uiTimer.stop()


'''=============== Main ==============='''
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = NiMotorControlUI()
    mainWindow.show()
    sys.exit(app.exec_())
    
    