#include <Wire.h> 
#include <LiquidCrystal_I2C.h>

// Set the LCD address to 0x27 in PCF8574 by NXP and Set to 0x3F in PCF8574A by Ti
LiquidCrystal_I2C lcd(0x3F, 16, 2);

void setup() {
	// initialize the LCD
	lcd.begin();
	lcd.print("This LCD I2C");
	lcd.setCursor(0, 1);
	lcd.print("www.ioxhop.com");
}

void loop() {
	// Do nothing here...
}
