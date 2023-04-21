/*****************************************************************************************
 This coding was created for Heart in a Box (Trans-Cardia) Project
 Belong to IQMED innovation co.,ltd.
 The controller used is DOIT ESP32 DevKit V1 30pin
 It contained the monitoring of Pressure, which will control the rpm of pump,
 and Temperatue, which will control the voltage (pwm) of warming peltier.
 This system is not using the PID because of uncontrollable temp change.
 All data output -  temp,pressure,flow
 ******************************************************************************************/

#include "HX711.h"
#include <OneWire.h>
#include <DallasTemperature.h>

// HX711 pressure set up
const int HX711_SCK_PIN = 14;
const int HX711_A_PIN = 33;
const int HX711_B_PIN = 32;
const int HX711_C_PIN = 35;
const int HX711_D_PIN = 34;
const int HX711_E_PIN = 39;
float pressure_a, pressure_b,pressure_c, pressure_d, pressure_e ;
HX711 pressure_A, pressure_B,pressure_C, pressure_D, pressure_E ;

//flow set up
double Flow_v1 = 0,Flow_v2 = 0, Flow_1 = 0,Flow_2 = 0 ;
const int F1_PIN = 15;
const int F2_PIN = 2;

// temp set up
#define ONE_WIRE_BUS 4 
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
DeviceAddress insideThermometer;
float tempC;

// Board Drive for peltier controlling
const int PWMPin = 13;
const int EN = 12;
const int freq = 5000; // PWM frequency (not experimented the best condition yet)
const int PWMChannel = 0; //
const int resolution = 8; // can be 0-16 bit
double SetTemp,Output;

String strTemp = "", strPA = "", strPB = "", strPC = "", strPD = "", strPE = "", strF1 = "",strF2 = "", strAll = "";  

int i = 0;

void setup() {
  Serial.begin(19200); //start serial port
  analogReadResolution(12);
  
  //Dallas Temperature Sensor
  sensors.begin(); // Start up the library for temp sen
  sensors.setResolution(insideThermometer, 12);
  if (!sensors.getAddress(insideThermometer, 0)) Serial.println("Unable to find address for Device 0"); 

  //Pressure Aortic
  pressure_A.begin(HX711_A_PIN, HX711_SCK_PIN);
  pressure_A.set_scale(10800.f); 
  
  //Pressure Blood in 
  pressure_B.begin(HX711_B_PIN, HX711_SCK_PIN);
  pressure_B.set_scale(10800.f); 
  
  //Pressure Blood out
  pressure_C.begin(HX711_C_PIN, HX711_SCK_PIN);
  pressure_C.set_scale(10800.f);
   
  //Pressure Dialysate in
  pressure_D.begin(HX711_D_PIN, HX711_SCK_PIN);
  pressure_D.set_scale(10800.f); 
  
  //Pressure Dialysate out
  pressure_E.begin(HX711_E_PIN, HX711_SCK_PIN);
  pressure_E.set_scale(10800.f); 
  
     pressure_A.tare(); 
     pressure_B.tare();
     pressure_C.tare(); 
     pressure_D.tare();  
     pressure_E.tare(); 

  //Board Drive for Peltier
  SetTemp = 32;//temperature set point for aluminium plate
  ledcSetup(PWMChannel, freq, resolution); // PWM chn 0 fq 5000mhz res 0-255
  ledcAttachPin(PWMPin, PWMChannel);//
  pinMode(EN, OUTPUT);
  digitalWrite(EN, HIGH);
  
}

void loop() {

  //Temperature from Dialysate's Plate
  sensors.requestTemperatures();
  tempC = sensors.getTempC(insideThermometer);
  strTemp.concat(tempC);

  if (SetTemp-tempC >=2)
     {  Output = 255;  }
  else if (tempC-SetTemp >0)
     {  Output = 100;  }
  else
     {  Output = 200;  }      
  ledcWrite(PWMChannel, Output);
  
  // Pressure from Fluid Tube in average of 4 points
    pressure_a = pressure_A.get_units(4);
    strPA.concat(pressure_a);
    
    pressure_b = pressure_B.get_units(4);
    strPB.concat(pressure_b);

    pressure_c = pressure_C.get_units(4);
    strPC.concat(pressure_c);
    
    pressure_d = pressure_D.get_units(4);
    strPD.concat(pressure_d);

    pressure_e = pressure_E.get_units(4);
    strPE.concat(pressure_e);

  //Flow from Fluid Tube F1 = Oxygenator line F2 = Dialysis line
  Flow_v1 = 0;Flow_v2 = 0;
  while (i<5)
  {
  Flow_v1 = analogRead(F1_PIN)+Flow_v1;
  Flow_v2 = analogRead(F2_PIN)+Flow_v2;
  i++;
  }
  i = 0;
  Flow_1= 0.0016*(Flow_v1/5);
  Flow_2= 0.0016*(Flow_v2/5);     
  strF1.concat(Flow_1);
  strF2.concat(Flow_2);  

   strAll = "";
   strAll = strTemp + "," + strPA + "," + strPB + "," + strPC + "," + strPD + "," + strPE + "," + strF1  + "," + strF2 + "/";
   Serial.println(strAll);
   strTemp = ""; strPA = ""; strPB = ""; strPC = ""; strPD = ""; strPE = "";strF1 = ""; strF2 = "";
}