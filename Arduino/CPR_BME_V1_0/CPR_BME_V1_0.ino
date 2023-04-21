#include "Arduino.h"
#include <Wire.h> // I2C library
#include "DFRobotDFPlayerMini.h"

//////////////Distance sensor///////////
#include "Adafruit_VL6180X.h"
Adafruit_VL6180X vl = Adafruit_VL6180X();

///////////////Bluetooth Module////////////////
#include "BluetoothSerial.h"
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run make menu config to and enable it
#endif
BluetoothSerial SerialBT;

///////////////MP3 Module////////////////
DFRobotDFPlayerMini myDFPlayer;
void printDetail(uint8_t type, int value);

//******************************************************************************
#define Red 2
#define Blue 18 //LED set pin numbers 
#define Green 5
#define Yellow 23 

void setup() {
  pinMode(Red,OUTPUT);  
  pinMode(Blue,OUTPUT);
  pinMode(Green,OUTPUT);
  pinMode(Yellow,OUTPUT); // status
  
  Serial.begin(115200); // sensor
  Wire.begin(); //I2C Start 
  if (! vl.begin()) 
  {
    Serial.println("Failed to find sensor");
    while (1);
  }   
  delay(100); 
  SerialBT.begin("ESP32test"); //Bluetooth device name

  Serial2.begin(9600);
  if (!myDFPlayer.begin(Serial2)) 
  {  
    Serial.println(F("Unable to begin:"));
    Serial.println(F("1.Please recheck the connection!"));
    Serial.println(F("2.Please insert the SD card!"));
    while(true){delay(0);} // Code to compatible with ESP8266 watch dog.    
  }
  myDFPlayer.play(1); // welcome CPR
  digitalWrite(Yellow,HIGH); // status OK   
}

//******************************************************************************
 void loop() {
  
  int sensorValue = analogRead(4);
  sensorValue = map(sensorValue,1023,0,0,30);
  myDFPlayer.volume(sensorValue); // MP3 Volume 0-30   
  delay(100);

  uint16_t samples[512] = {0};
  uint32_t start = micros();
  for (int i=0; i<512; ++i) 
  {
    samples[i] = vl.readRange();
    delayMicroseconds(1500);
  }
  uint32_t elapsed_uS = micros() - start;
  float elapsed = elapsed_uS / 1000000.0;  // Elapsed time in seconds.
  
  // Find the min and max values in the collected samples.
  uint16_t minval = samples[0];
  uint16_t maxval = samples[0];
  for (int i=1; i<512; ++i) {
    minval = min(minval, samples[i]);
    maxval = max(maxval, samples[i]);
  }
  uint16_t amplitude = maxval - minval;
  if (amplitude < 30) {
      return;
  }
   
  uint16_t midpoint = minval + (amplitude/2);// Compute midpoint of the signal.

  int crossings = 0;
  for (int i=1; i<512; ++i) {
    uint16_t p0 = samples[i-1];
    uint16_t p1 = samples[i];
    if ((p1 == midpoint) || 
        ((p0 < midpoint) && (p1 > midpoint)) ||
        ((p0 > midpoint) && (p1 < midpoint))) {
      crossings += 1;
    }
  }

  float period = elapsed / (crossings / 1 / 2.0); 
  float frequency = 1.0 / period;
  int bpm = frequency * 60.0; 
  
  digitalWrite(Green,LOW);
  digitalWrite(Blue,LOW);
  digitalWrite(Red,LOW);
  
  if (amplitude > 45 ){ // good depth 
    digitalWrite(Blue,HIGH);
    }
  else {
    digitalWrite(Red,HIGH); 
  }
  
  if (bpm > 120 ){
    myDFPlayer.play(3);    //fast   
    }
  else if(bpm < 100 ){
    myDFPlayer.play(2); //slow
    }
  else{ 
   //myDFPlayer.play(4); //good
   digitalWrite(Red,LOW);  
    }

  SerialBT.println((amplitude+4)/10);
  SerialBT.println(bpm);
 }
 
