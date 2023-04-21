#include "Arduino.h"
#include <Wire.h>

//////////////Distance sensor///////////
#include "Adafruit_VL6180X.h"
Adafruit_VL6180X vl = Adafruit_VL6180X();

///////////////MP3 Module////////////////
#include "SoftwareSerial.h"
#include "DFRobotDFPlayerMini.h"
SoftwareSerial mySoftwareSerial(2,3); // pin RX, TX
DFRobotDFPlayerMini myDFPlayer;
void printDetail(uint8_t type, int value);

///////////////Bluetooth Module////////////////
#include "BluetoothSerial.h"
#if !defined(CONFIG_BT_ENABLED) || !defined(CONFIG_BLUEDROID_ENABLED)
#error Bluetooth is not enabled! Please run `make menuconfig` to and enable it
#endif
BluetoothSerial SerialBT;
////////////LED // set pin numbers
    #define Red 2
    #define Blue 18
    #define Green 5
    #define Yellow 23 

//const int ledCount = 3;
//int ledPins[] = {2, 5, 18};  // an array of pin numbers to which LEDs are attached

//******************************************************************************
void setup() {
  pinMode(Red,OUTPUT);  // initialize the LED pin as an output:
  pinMode(Blue,OUTPUT);
  pinMode(Green,OUTPUT);
  pinMode(Yellow,OUTPUT);
  
  Serial.begin(115200); // sensor
  if (! vl.begin()) 
  {
    Serial.println("Failed to find sensor");
    while (1);
  }
  Wire.begin(); //Start I2C library
  delay(100); // delay .1s
  SerialBT.begin("ESP32test"); //Bluetooth device name
  Serial.println("The device started, now you can pair it with bluetooth!");

  Serial2.begin(9600); 
  Serial.println();
  Serial.println(F("Initializing DFPlayer ... (May take 3~5 seconds)"));  
   if (!myDFPlayer.begin(Serial2)) {  //Use softwareSerial to communicate with mp3.
    Serial.println(F("Unable to begin:"));
    Serial.println(F("1.Please recheck the connection!"));
    Serial.println(F("2.Please insert the SD card!"));
    while(true){
      delay(0); // Code to compatible with ESP8266 watch dog.
    }
  }
  myDFPlayer.play(1); // welcome CPR
  digitalWrite(Yellow,HIGH); // status OK   
}

 void loop() {
  
  int sensorValue = analogRead(4);
  sensorValue = map(sensorValue,0,1023,0,30);
  myDFPlayer.volume(sensorValue); // MP3 Volume 0-30
      
  delay(1000);
  uint16_t samples[512] = {0};
  uint32_t start = micros();
  for (int i=0; i<512; ++i) {
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
  uint16_t amplitude = maxval - minval;//*********************
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

  float period = elapsed / (crossings / 1 / 2.0); //*************************
  float frequency = 1.0 / period;
  int bpm = frequency * 60.0; 
  
  digitalWrite(Green,LOW);
  digitalWrite(Blue,LOW);
  digitalWrite(Red,LOW);
  
  if (amplitude > 45 ){ // good depth **************
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

  // Print out the measured values!
  //Serial.print("Frequency: ");
  //Serial.print(frequency, 3);
  Serial.print("Distance: "); 
  Serial.print(amplitude);
  Serial.print(" (mm)\tRate: ");
  Serial.print(bpm);
  Serial.println(" (bpm)");
  SerialBT.println((amplitude+4)/10);
  SerialBT.println(bpm);
  //Serial.print(period, 3);
  //Serial.println(" (seconds)");
 }
 
