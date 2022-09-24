import time
from daqmx import NIDAQmxInstrument, AnalogInput

daq = NIDAQmxInstrument()

print(daq)
ai0 = AnalogInput(device='Dev1', analog_input='ai0')

while True:
    print(f'Analog Input AI0 value: {ai0.value:.3f}V')
    time.sleep(0.5)


