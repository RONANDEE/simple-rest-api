import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

import pyhrv
import pyhrv.time_domain as td
import pyhrv.frequency_domain as fd
import pyhrv.tools as tools

import statistics

# Create a Tkinter window
window = tk.Tk()
window.title("HRV Graph in Tkinter")

# Create a Matplotlib figure
fig = Figure(figsize=(6, 4), dpi=100)
ax1 = fig.add_subplot(211)
ax2 = fig.add_subplot(212)

data = pd.read_csv('Hemodynamic-beats.txt',sep=';',skiprows=7)
nni = data['Pulse Interval (ms)']
nni_HR = data['Heart rate (bpm)']


# Plot the graph

x = data['Time (s)']
y1 = data['Pulse Interval (ms)']
y2 = data['Heart rate (bpm)']
ax1.plot(y1)
ax2.hist(y1/1000, bins=30, density=True, alpha=0.7, color='blue')

# Create a FigureCanvasTkAgg object and add it to the Tkinter window
canvas = FigureCanvasTkAgg(fig, master=window)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

df = pd.DataFrame(nni)
label = tk.Label(window, text=df.to_string(index=False))
label.pack()

# Start the Tkinter event loop
window.mainloop()

