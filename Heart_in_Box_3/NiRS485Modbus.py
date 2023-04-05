from Conversions import *
from Constants import *
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time

class RS485Modbus:
    def __init__(self, name, port, baudrate, nMotor):
        self.name = name
        self.port = port
        self.bus = ModbusClient(method='rtu', port=self.port, timeout=1, baudrate=baudrate)
        self.nMotor = nMotor
        self.motors = []
        self.motorAddrs = []

        # Connecting to Serial port and checking the motor bus
        self.bus.connect()
        # Scanning for available motors
        if self.bus.is_socket_open():
            self.motorAddrs = self.scanForMotors(1, self.nMotor)
            # print("Motor Address: {}".format([ addr for addr in self.motorAddrs]))
    
    def addMotor(self):
        return
        
    def isConnected(self):
        if not self.bus.is_socket_open():
            # print("\nThe motor bus on {} is busy and unable to be connected".format(self.port))
            return False
        # print("\nThe motor bus on {} is successfully connected.".format(self.port))
        return True
    
    def closePort(self):
        if self.bus.is_socket_open():
            self.bus.close()
            return True

    def scanForMotors(self, firstID, lastID):
        _motors = [] 
        '''wating for implementation'''
        for motorID in range(firstID,lastID+1):
            id, connection = self.pingMotor(motorID)
            if connection:
                self.motors.append(self.Motor(self.bus, id, "NiMotion BLM:0{}".format(id)))
                _motors.append(str(id))
        return _motors
    
    def pingMotor(self, id):
        assert self.bus.connect(), "Unable to connect to {}". format(self.port)
        if not self.bus.is_socket_open():
            return id, False
        request = self.bus.read_holding_registers(SERVO_ID,1,unit=id)
        if request.isError():
            return id, False
        addr = request.registers[0]
        return id, True
    
    class Motor:
        def __init__(self, busObj, id, name):
            self.device = busObj
            self.id = id
            self.name = name
            # Initial Values
            self.actualSpeed = 0
            self.actualTemp = 0
            self.busVoltage = 0
            
            self.id = self.getMotorID()
            self.mode = self.getOpMode()
            self.accCurve = self.getAccCurveType()
            self.maxSpeed = self.getMaxSpeed()
            self.maxTorque = self.getMaxTorquePercent()

            self.updateValue()
        
        def updateValue(self):
            # if not self.device.connect():
            #     return False
            self.ratedCurrent = self.getRatedCurrent()
            self.temp = self.getTemp()
            self.status, self.statusDict = self.getStatusWord()
            self.actualCurrent = self.getActualCurrent()
            self.busVoltage = self.getBusVoltage()
            self.power = self.getPower()
            self.actualSpeed, self.rotation = self.getActualSpeed()

        def start(self):
            # START
            if not self.device.connect():
                return False
            self.getStatusWord()
            self.stop()
            self.getStatusWord()
            # SWTCH ON
            self.switchOn()
            self.getStatusWord()
            # DRIVE
            self.driveEnable()
            self.getStatusWord()
            return True
        
        def stop(self):
            # STOP
            if not self.device.connect():
                return False
            request = self.device.write_register(CONTROL_WORD,STOP,unit=self.id)
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            # print("{} is stopping" .format(self.name))
            return True
    
        def switchOn(self):
            # SWITCH ON
            if not self.device.connect():
                return False
            request = self.device.write_register(CONTROL_WORD,SWITCH_ON,unit=self.id) 
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            return True
        
        def driveEnable(self):
            # DRIVE
            if not self.device.connect():
                return False
            request = self.device.write_register(CONTROL_WORD,DRIVE,unit=self.id) 
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            return True

        def ping(self):
            if not self.device.connect():
                return False
            request = self.device.read_input_registers(MCU_ID,1,unit=self.id)
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            # print("{} is connected, MCU ID: {}". format(self.name, decListToHexList(request.registers)))
            return True
        
        def getMotorID(self):
            if not self.device.connect():
                return False
            request = self.device.read_holding_registers(SERVO_ID,1,unit=self.id)
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            addr = request.registers[0]
            # print("Motor Address: {}". format(addr))
            return addr
            
        def setMotorId(self,newID):
            # waiting for implementation
            return True

        def getAccCurveType(self):
            if not self.device.connect():
                return False
            request = self.device.read_holding_registers(ACC_CURVE,1,unit=self.id)
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            regValues = decListToHexList(request.registers)
            # print("Acc. Curve Type: {}". format(ACC_CURVE_DICT[regValues[0]]))
            return ACC_CURVE_DICT[regValues[0]]
    
        def setAccCurveType(self, curveType):
            # waiting for implementation
            return True

        def getOpMode(self):
            if not self.device.connect():
                return False
            request = self.device.read_holding_registers(MODE_OPER,1,unit=self.id)
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            regValues = decListToHexList(request.registers)
            # print("Mode: {}". format(OPMODE_DICT[regValues[0]]))
            return OPMODE_DICT[regValues[0]]
        
        def setOpMode(self, newMode):
            # waiting for implementation
            return True

        def getStatusWord(self):
            if not self.device.connect():
                return False
            request = self.device.read_holding_registers(STATUS_WORD,1,unit=self.id)
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            status = decListToHexList(request.registers)
            # print("\t>>>> Status Word: {}: {}\n". format(status, STATUS_DICT[status[0]]))
            return status[0], STATUS_DICT[status[0]] 

        def setTargetSpeed(self, speed, rotation='CW'):
            if not self.device.connect():
                return False
            # print("Setting target speed to {} RPM, direction: {}" .format(speed,rotation))
            rpm = calRPM(speed, rotation=rotation)
            request = self.device.write_registers(TARGET_SPEED,rpm,unit=self.id)
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            self.getStatusWord()
            return True
        
        def getActualSpeed(self):
            if not self.device.connect():
                return False
            request = self.device.read_input_registers(ACTUAL_SPEED,2,unit=self.id)
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            [speed, rotation] = listToRPM(request.registers)
            # print(">> Actual Speed: {} RPM, Direction: {}". format(speed, rotation))
            self.getStatusWord()
            return speed, rotation
        
        def getMaxSpeed(self):
            if not self.device.connect():
                return False
            request = self.device.read_input_registers(MAX_SPEED,2,unit=self.id)
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            regValues = request.registers
            # print("Max. Speed: {} RPM". format(regValues[1]))
            return regValues[1]

        def setMaxSpeed(self, maxSpeed):
            # waiting for implementation
            return True

        def getMaxTorquePercent(self):
            if not self.device.connect():
                return False
            request = self.device.read_input_registers(MAX_TORQUE,1,unit=self.id)
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            regValues = request.registers
            # print("Max. Torque: {} %". format(regValues[0]/10))
            return regValues[0]/10

        def setMaxTorquePercent(self, maxTorque):
            # waiting for implementation
            return True

        def getAccel(self):
            # waiting for implementation
            return True

        def setAccel(self, accel):
            # waiting for implementation
            return True
        
        def getDecel(self):
            # waiting for implementation
            return True

        def setDecel(self, decel):
            # waiting for implementation
            return True    
        
        def getBrakeResist(self):
            # waiting for implementation
            return True
        
        def setBreakResist(self,breakResist):
            # waiting for implementation
            return True

        def getBaudRate(self):
            # wait for implementation
            return True
        
        def setBaudRate(self, baudRate):
            # wait for implementation
            return True
        
        def getRatedCurrent(self):
            if not self.device.connect():
                return False
            request = self.device.read_input_registers(RATED_CURRENT,1,unit=self.id)
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            regValues = request.registers
            # print("Rated Current: {:.2f} A". format(regValues[0] * 0.01))
            return regValues[0]*0.01


        def getActualCurrent(self):
            if not self.device.connect():
                return False
            actual_current = 0
            self.ratedCurrent = self.getRatedCurrent()
            request = self.device.read_input_registers(ACTUAL_CURRENT,1,unit=self.id)
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            regValues = request.registers
            actual_current = self.ratedCurrent * ((regValues[0] * 0.1) / 100)
            # print("Actual Current: {:.5f} A". format(actual_current))
            return actual_current

        
        def getBusVoltage(self):
            if not self.device.connect():
                return False
            request = self.device.read_input_registers(BUS_VOLTAGE,1,unit=self.id)
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            regValues = request.registers
            # print("Bus Voltage: {:.2f} V". format(regValues[0] * 0.1))
            return regValues[0]*0.1
        
        def getPower(self):
            if not self.device.connect():
                return False
            actual_power = self.getActualCurrent() * self.getBusVoltage()
            # print("Power: {:.5f} Watt". format(actual_power))
            return actual_power
        
        def getTemp(self):
            if not self.device.connect():
                return False
            request = self.device.read_input_registers(TEMPERATURE,1,unit=self.id)
            if request.isError():
                print('Error message: {}' .format(request))
                return False
            regValues = request.registers
            # print("Temperature: {:.2f} °C". format(regValues[0]))
            return regValues[0]


'''=============== Main ==============='''

if __name__ == "__main__":
    TIMEOUT = 10
    motorbus = RS485Modbus(name='NiMotorBus',port='COM3',nMotor=4)
    if len(motorbus.motorAddrs):
        motorbus.motor[0].setTargetSpeed(2000, rotation='cw')
        motorbus.motor[1].setTargetSpeed(1000, rotation='ccw') 
        motorbus.motor[2].setTargetSpeed(100, rotation='cw')

    for id in range(3): 
        print(id)
        print(motorbus.motor[id].name)
        motorbus.motor[id].start()

    time.sleep(TIMEOUT)
    for id in range(3):
        motorbus.motor[id].stop()
    # motorbus.motor1.setTargetSpeed(2000, rotation='cw') 
    # motorbus.motor2.setTargetSpeed(500, rotation='cw')
    # motorbus.motor3.setTargetSpeed(100, rotation='cw')

    # motorbus.motor1.start()
    # motorbus.motor2.start()
    # motorbus.motor3.start()
    # time.sleep(TIMEOUT)

    # motorbus.motor1.stop()
    # motorbus.motor2.stop()
    # motorbus.motor3.stop()



