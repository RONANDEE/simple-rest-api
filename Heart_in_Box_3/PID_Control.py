import time

# PID constants
Kp = 0.5 # proportional gain
Ki = 0.1 # integral gain
Kd = 0.2 # derivative gain

# setpoint and initial conditions 
setpoint = 100  # desired value of the process variable 
pv_last = 0    # last process variable value 
integral = 0   # integral term 

 while True:

    # read process variable from sensor/controller 
    pv = read_sensor()

    # calculate error between setpoint and process variable 
    error = setpoint - pv

    # calculate integral term 
    integral += error * dt

    # calculate derivative term 
    derivative = (pv - pv_last) / dt

    # calculate output from PID controller  
    output = Kp * error + Ki * integral + Kd * derivative

    # write output to actuator/controller  
    write_actuator(output)

    pv_last = pv

    time.sleep(dt)