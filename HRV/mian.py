import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

import pyhrv
import pyhrv.time_domain as td
import pyhrv.frequency_domain as fd
import statistics



# Sample DataFrame
BP_HB = pd.read_csv('Hemodynamic-beats.txt',sep=';',skiprows=7)
nni = BP_HB['Pulse Interval (ms)']
nni_HR = BP_HB['Heart rate (bpm)']

# Compute parameters
NNI = statistics.mean(nni)
NNI_HR = statistics.mean(nni_HR)

STD = td.sdnn(nni)
STD_HR = td.sdnn(nni_HR)

RMSSD = td.rmssd(nni)
NN50 = td.nn50(nni)

# Create a new DataFrame for the report

report_df = pd.DataFrame({
                            'Variable':['Mean RR', 'STD RR', 'Mean HR', 'STD HR','RMSSD', 'NN50', 'pNN50'],
                            'Unit':['ms', 'ms', 'bpm', 'bpm', 'ms','count', '%'], 

                            'Value':[NNI, STD['sdnn'], NNI_HR, STD_HR['sdnn'],RMSSD['rmssd'], NN50['nn50'], NN50['pnn50']]
                                })

#plt.rcParams['toolbar'] = 'None'


fig = plt.figure()
fig.suptitle('Time Domain Results',fontsize=20,color="blue")

ax1 = fig.add_subplot(211,title='Pulse Interval')
ax1.plot(nni/1000,'r')
ax1.set_ylabel('NN (s)')


'''
ax2 = fig.add_subplot(213)
# Hide axis
ax2.axis('off')
# Create a table on the figure and display the DataFrame
table = plt.table(cellText=report_df.values, colLabels=report_df.columns, cellLoc='center', loc='center')
# Set the table properties
table.auto_set_font_size(False)
table.set_fontsize(20)
table.scale(1.2, 1.2)
'''

data = nni  # Random normally distributed data

# Calculate statistical measures
mean = np.mean(data)
std = np.std(data)
min_val = np.min(data)
max_val = np.max(data)

# Create a figure
ax3 = fig.add_subplot(212)

# Plot a histogram
ax3.hist(data/1000, bins=30, density=True, alpha=0.7, color='blue')

# Add statistical report as text
report = f"Mean: {mean:.2f}\nSTD: {std:.2f}\nMin: {min_val:.2f}\nMax: {max_val:.2f}"
ax3.text(0.7, 0.9, report, transform=ax3.transAxes, fontsize=10, verticalalignment='top')

# Add labels and title
ax3.set_xlabel('Value')
ax3.set_ylabel('Frequency')
ax3.set_title('Histogram with Statistical Report')


result = fd.welch_psd(nni,show_param=True)

# Show the figure
#plt.show()


