from tkinter import*
#from tkinter import ttk
#import tkinter as tk
import serial

from Conversions import *
from Constants import *
from pymodbus.client.sync import ModbusSerialClient as ModbusClient
import time
import simple_pid


# Open the serial connection to the motor controller
client = ModbusClient(method='rtu', port='COM12', baudrate=115200,timeout=1)
client.connect()

root = Tk()
root.geometry('1920x1280')
root.title("Heart in Box V1.0")

# Create label for displaying sensor value
value_label0 = Label(root, text="Temperature : ",font=('Ansana New',30,'bold'),fg='red')
value_label0.pack()
value_label1 = Label(root, text="Pressure #1 : ",font=('Ansana New',30,'bold'),fg='green')
value_label1.pack()
value_label2 = Label(root, text="Pressure #2 : ",font=('Ansana New',30,'bold'),fg='green')
value_label2.pack()
value_label3 = Label(root, text="Pressure #3 : ",font=('Ansana New',30,'bold'),fg='green')
value_label3.pack()
value_label4 = Label(root, text="Pressure #4 : ",font=('Ansana New',30,'bold'),fg='green')
value_label4.pack()
value_label5 = Label(root, text="Pressure #5 : ",font=('Ansana New',30,'bold'),fg='green')
value_label5.pack()
value_label6 = Label(root, text="Pressure #6 : ",font=('Ansana New',30,'bold'),fg='green')
value_label6.pack()
value_label7 = Label(root, text="Pressure #7 : ",font=('Ansana New',30,'bold'),fg='green')
value_label7.pack()

# Create Serial object with appropriate settings
ser = serial.Serial('COM3', 19200)

# Define function to update label with new sensor value
def update_label():
    # Read data from serial port
    line = ser.readline().decode().strip() .replace('/','')
    my_list = line.split(',')
    data0 = my_list[0]
    data1 = my_list[1]
    data2 = my_list[2]
    data3 = my_list[3]    
    data4 = my_list[4]
    data5 = my_list[5]
    data6 = my_list[6]
    data7 = my_list[7]    

    # Update label text with new sensor value
    value_label0.config(text="Temperature : " + data0 + " °C")    
    value_label1.config(text="Pressure #1 : " + data1 + " mmHg")
    value_label2.config(text="Pressure #2 : " + data2 + " mmHg")
    value_label3.config(text="Pressure #3 : " + data3 + " mmHg")
    value_label4.config(text="Pressure #4 : " + data4 + " mmHg")
    value_label5.config(text="Pressure #5 : " + data5 + " mmHg")
    value_label6.config(text="Pressure #6 : " + data6 + " mmHg")
    value_label7.config(text="Pressure #7 : " + data7 + " mmHg")
   
    root.after(100, update_label)    # Schedule next update in 100 milliseconds

# Schedule first update
root.after(100, update_label)


def start():
    request = client.write_register(CONTROL_WORD,SWITCH_ON,unit=3) # SWITCH ON
    request = client.write_register(CONTROL_WORD,DRIVE,unit=3) # Drive
    print('start')

def stop():
    request = client.write_register(CONTROL_WORD,STOP,unit=3) 
    print("Motor#1 is stopping")
    

def getActualSpeed():
    request = client.read_input_registers(ACTUAL_SPEED,2,unit=3)
    [speed, rotation] = listToRPM(request.registers)
    print(">> Actual Speed: {} RPM, Direction: {}". format(speed, rotation))    

def setTargetSpeed(speed, rotation='CW'):
    rpm = calRPM(speed, rotation=rotation)
    request = client.write_registers(TARGET_SPEED,rpm,unit=3)
    print(">> Speed setting: {} RPM, Direction: {}". format(speed, rotation))  

def PID_update():
    line = ser.readline().decode().strip() .replace('/','')
    my_list = line.split(',')
   
    values =  my_list[1]
    Kp = 1.0
    Ki = 0.1
    Kd = 0.05
    setpoint = 50  # Pressure
    sample_time = 0.01  # Sample time in seconds 
    output_limits = (0, 100)  # Output limits of the PID controller in % 

    # Create a PID 
    pid = simple_pid.PID(Kp, Ki, Kd, setpoint, output_limits=output_limits, sample_time=sample_time)

    current_temp = values[1]  # Get the variable from a sensor 
    control_output = pid(current_temp)  # Calculate the output of the PID controller 
    setTargetSpeed(control_output, rotation='CW')
    # return control_output
    # Use control output to actuator 



btn1 = Button(root,text='Start',font=('Ansana New',20,'bold'),fg='white',bg='green',command=start).pack()
btn2 = Button(root,text='Stop',font=('Ansana New',20,'bold'),fg='white',bg='red',command=stop).pack()
btn3 = Button(root,text='Speed',font=('Ansana New',20,'bold'),fg='white',bg='red',command=getActualSpeed).pack()
#btn4 = Button(root,text='set Speed',font=('Ansana New',20,'bold'),fg='white',bg='red',command=setTargetSpeed(1000,'CW')).pack()

# Start Tkinter event loop
root.mainloop()



