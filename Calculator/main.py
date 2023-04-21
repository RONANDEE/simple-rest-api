import tkinter as tk
from tkinter import *
from tkinter import ttk

import datetime


# Create a new tkinter window
root = tk.Tk()
root.title("Heart In Box V1.0.0_Demo")
root.geometry("1920x1080")
#root.state('zoomed') #Full screen
root.minsize(1920,1080)
root.configure(background = '#122738')


# Create a widget

class ClockFrame(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)

        self.clock_label = tk.Label(self, font=('Arial Black', 30),bg='#122738',fg='#ff0088')
        self.clock_label.pack()
        self.update_clock()

    def update_clock(self):
        now = datetime.datetime.now()
        dt_string = now.strftime("%Y/%m/%d   %H:%M:%S")
        self.clock_label.config(text=dt_string)
        self.clock_label.after(1000, self.update_clock)

class Timer(tk.Frame):
    def __init__(self, master):   
        tk.Frame.__init__(self, master)     
        self.master = master
        self.time = 0
        self.running = False
        
        # create label to display time
        self.label = tk.Label(self, text=" Case Time : 00:00:00 ", bg='#122738',fg='white',font=('Arial Black', 40),highlightbackground="white", highlightthickness=5)
        self.label.pack(side="left",padx=10,pady=10)
        
        # create buttons to control timer
        self.start_button = tk.Button(self, text="Start",font=('Arial Black', 28), command=self.start)
        self.start_button.pack(side="left", padx=10,pady=10)
        
        self.stop_button = tk.Button(self, text="Stop",font=('Arial Black', 28), command=self.stop)
        self.stop_button.pack(side="left", padx=10)
        self.stop_button.config(state="disabled") # disable stop button at start
        
        self.reset_button = tk.Button(self, text="Reset",font=('Arial Black', 28), command=self.reset)
        self.reset_button.pack(side="left", padx=10)
        self.reset_button.config(state="disabled") # disable reset button at start
        
    def start(self):
        self.running = True
        self.start_button.config(state="disabled")
        self.stop_button.config(state="normal")
        self.reset_button.config(state="disabled")
        self.update_time()
        
    def stop(self):
        self.running = False
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.reset_button.config(state="normal")
        
    def reset(self):
        self.running = False
        self.time = 0
        self.label.config(text=" Case Time : 00:00:00 ")
        self.start_button.config(state="normal")
        self.stop_button.config(state="disabled")
        self.reset_button.config(state="disabled")
        
    def update_time(self):
        if self.running:
            self.time += 1
            minutes, seconds = divmod(self.time, 60)
            hours, minutes = divmod(minutes, 60)
            time_string = f" Case Time : {hours:02d}:{minutes:02d}:{seconds:02d} "
            self.label.config(text=time_string)
            self.master.after(1000, self.update_time)



clock_frame = ClockFrame(root)
clock_frame.grid(row=0,column=0,padx=10,pady=10)
timer = Timer(root)
timer.grid(row=0,column=1,padx=10,pady=10)
timer.config(bg='#122738')

# Create a LabelFrame COM
label_frame_serial = tk.LabelFrame(root,text=' Serial Monitor(RS-232) ',font=('Arial', 30,'bold'),labelanchor='n',bd=10 ,bg='#122738',fg='#ffc600')
# Add a Label to the LabelFrame
label1 = tk.Label(label_frame_serial, text="Serial Port :")
label1.pack(pady=10)
label2 = tk.Label(label_frame_serial, text="Serial Port :")
label2.pack()
# Create a LabelFrame COM
label_frame = tk.LabelFrame(root,text=' Modbus (RS-485) ',font=('Arial', 30,'bold'),labelanchor='n',bd=10,bg='#122738',fg='#ffc600')
# Add a Label to the LabelFrame
label = tk.Label(label_frame, text="Serial Port :")
label.pack()




label_frame1 = tk.LabelFrame(root, text=" Monitor ",font=('Arial', 30,'bold'),labelanchor='n',bd=10,bg='#122738',fg='#ffc600')
label_temp = tk.Label(label_frame1, text=" Temperature      °C \n\n\n",font=('Arial', 24,'bold'),bg='#122738',fg='yellow',highlightbackground="yellow",highlightthickness=5)
label_temp.grid(row=0, column=0,padx=10,pady=10,sticky='nswe')

label1 = tk.Label(label_frame1, text=" Pressure # 1   mmHg \n\n\n",font=('Arial', 24,'bold'),bg='black',fg='green',highlightbackground="red",highlightthickness=5)
label1.grid(row=1, column=0,padx=10,pady=10,sticky='nswe')

label2 = tk.Label(label_frame1, text=" Pressure # 2   mmHg \n\n\n",font=('Arial', 24,'bold'),bg='black',fg='green',highlightbackground="green",highlightthickness=5)
label2.grid(row=0, column=1,padx=10,pady=10,sticky='nswe')
label3 = tk.Label(label_frame1, text=" Pressure # 3   mmHg \n\n\n",font=('Arial', 24,'bold'),bg='black',fg='green',highlightbackground="green",highlightthickness=5)
label3.grid(row=1, column=1,padx=10,pady=10,sticky='nswe')

label4 = tk.Label(label_frame1, text=" Pressure # 4   mmHg \n\n\n",font=('Arial', 24,'bold'),bg='black',fg='green',highlightbackground="green",highlightthickness=5)
label4.grid(row=0, column=2,padx=10,pady=10,sticky='nswe')
label5 = tk.Label(label_frame1, text=" Pressure # 5   mmHg \n\n\n",font=('Arial', 24,'bold'),bg='black',fg='green',highlightbackground="green",highlightthickness=5)
label5.grid(row=1, column=2,padx=10,pady=10,sticky='nswe')

label6 = tk.Label(label_frame1, text=" Flow # 1     LPM \n\n\n",font=('Arial', 24,'bold'),bg='black',fg='blue',highlightbackground="blue",highlightthickness=5)
label6.grid(row=0, column=3,padx=10,pady=10,sticky='nswe')
label7 = tk.Label(label_frame1, text=" Flow # 2     LPM \n\n\n",font=('Arial', 24,'bold'),bg='black',fg='white',highlightbackground="blue",highlightthickness=5)
label7.grid(row=1, column=3,padx=10,pady=10,sticky='nswe')


label_frame3 = tk.LabelFrame(root, text=" Pump Control ",font=('Arial', 30,'bold'),labelanchor='n',bd=10,bg='#122738',fg='#ffc600',width=200,height=200)
# Add a Label to the LabelFrame
label1 = tk.Label(label_frame3, text=" Status \nActual Speed Pump (rpm) \n2000\nsetting\n 50\n set\n start\n\n",font=('calibri', 20,'bold'),bg='brown',fg='white')
label1.grid(row=0, column=0,pady=20,padx = 10)
label2 = tk.Label(label_frame3, text=" Actual Speed Pump (rpm) ",font=('calibri', 20,'bold'))
label2.grid(row=0, column=1,padx=20,pady=10)
label3 = tk.Label(label_frame3, text=" Actual Speed Pump (rpm) ",font=('calibri', 20,'bold'))
label3.grid(row=0, column=2,padx=20)
label4 = tk.Label(label_frame3, text=" Actual Speed Pump (rpm) \n\n\n\n\n\n\n\n\n\n",font=('calibri', 20,'bold'))
label4.grid(row=0, column=3,padx=20,pady=10)



# Pack the LabelFrame onto the root window
label_frame_serial.grid(row=1,column=0,padx=5,sticky='nsew')
label_frame.grid(row=2,column=0,padx=5,sticky='nsew')
label_frame1.grid(row=1,column=1,sticky='nsew')
label_frame3.grid(row=2,column=1,sticky='nsew')


# Start the tkinter event loop
root.mainloop()