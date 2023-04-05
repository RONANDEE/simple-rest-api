import tkinter as tk
import serial

def read_serial_values():
    ser = serial.Serial('COM3', 19200) 
    while True:
        try:
            line = ser.readline().decode().strip().replace('/','')
            values = line.split(',')
            if len(values) == 8:
                #print(values)
                return values
            
        except serial.SerialException:
            pass

root = tk.Tk()
root.geometry('1920x1280')
root.title("Heart in Box V1.0")

sensor1_label = tk.Label(root, text="Sensor 1: ")#,font=('Ansana New',30,'bold'))
sensor1_value = tk.Label(root, text="0")
sensor2_label = tk.Label(root, text="Sensor 2: ")
sensor2_value = tk.Label(root, text="0")
sensor3_label = tk.Label(root, text="Sensor 3: ")
sensor3_value = tk.Label(root, text="0")

sensor1_label.grid(row=0, column=0)
sensor1_value.grid(row=0, column=1)
sensor2_label.grid(row=1, column=0)
sensor2_value.grid(row=1, column=1)
sensor3_label.grid(row=2, column=0)
sensor3_value.grid(row=2, column=1)

def update_values():
    values = read_serial_values()
    if values is not None:
        sensor1_value.config(text=values[0])
        sensor2_value.config(text=values[1])
        sensor3_value.config(text=values[2])
        '''
        sensor1_value.config(text=values[3])
        sensor2_value.config(text=values[4])
        sensor3_value.config(text=values[5])
        sensor1_value.config(text=values[6])
        sensor2_value.config(text=values[7])
        '''
    root.after(100, update_values)

update_values()



root.mainloop()
