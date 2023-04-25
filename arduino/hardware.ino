/*
  LiquidCrystal Library - Hello World

 Demonstrates the use a 16x2 LCD display.  The LiquidCrystal
 library works with all LCD displays that are compatible with the
 Hitachi HD44780 driver. There are many of them out there, and you
 can usually tell them by the 16-pin interface.

 This sketch prints "Hello World!" to the LCD
 and shows the time.

  The circuit:
 * LCD RS pin to digital pin 12
 * LCD Enable pin to digital pin 11
 * LCD D4 pin to digital pin 5
 * LCD D5 pin to digital pin 4
 * LCD D6 pin to digital pin 3
 * LCD D7 pin to digital pin 2
 * LCD R/W pin to ground
 * LCD VSS pin to ground
 * LCD VCC pin to 5V
 * 10K resistor:
 * ends to +5V and ground
 * wiper to LCD VO pin (pin 3)

 Library originally added 18 Apr 2008
 by David A. Mellis
 library modified 5 Jul 2009
 by Limor Fried (http://www.ladyada.net)
 example added 9 Jul 2009
 by Tom Igoe
 modified 22 Nov 2010
 by Tom Igoe
 modified 7 Nov 2016
 by Arturo Guadalupi

 This example code is in the public domain.

 http://www.arduino.cc/en/Tutorial/LiquidCrystalHelloWorld

*/

// include the library code:
#include <LiquidCrystal.h>
#include <SPI.h>
#include <string.h>
#include "nRF24L01.h"
#include <RF24.h>
RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";

int timeReleased = 0;    
int startPressed = 0;    
int buttonState1 = 0;
int buttonState2 = 0;
int buttonState3 = 0;
int buttonState4 = 0;
int sendState = 0;
const int buttonPin4 = 18;
const int buttonPin3 = 17;
const int buttonPin2 = 16;
const int buttonPin1 = 15;
const int buttonsend = 14;
//int contrast = 6;
int val = 0;
int posx = 0;
int posy = 1;
const char msg1[] = ""; 

// initialize the library by associating any needed LCD interface pin
// with the arduino pin number it is connected to
const int rs = 10, en = 9, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


void setup() {
  //pinMode(contrast, OUTPUT); // 配置 引脚模式为输出模式
  pinMode(en, OUTPUT); // 配置 引脚模式为输出模式
  pinMode(rs, OUTPUT); // 配置 引脚模式为输出模式
//  pinMode(d4, OUTPUT); // 配置 引脚模式为输出模式
//  pinMode(d5, OUTPUT); // 配置 引脚模式为输出模式
//  pinMode(d6, OUTPUT); // 配置 引脚模式为输出模式
//  pinMode(d7, OUTPUT); // 配置 引脚模式为输出模式
  pinMode(buttonPin4, INPUT);
  pinMode(buttonPin3, INPUT);
  pinMode(buttonPin2, INPUT);
  pinMode(buttonPin1, INPUT);
  pinMode(buttonsend, INPUT);
//  analogWrite(contrast,130); // 该引脚一个固定频率的PWM信号，例如130
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  // Print a message to the LCD.
  lcd.print("I-clicker for ZJUI");

  // initialize the pushbutton pin as an input:
  Serial.begin(9600);
  radio.begin();
  radio.openWritingPipe(address);
  radio.setPALevel(RF24_PA_MIN);
  radio.stopListening();
}

void loop() {
  buttonState1 = digitalRead(buttonPin1);
  buttonState2 = digitalRead(buttonPin2);
  buttonState3 = digitalRead(buttonPin3);
  buttonState4 = digitalRead(buttonPin4);
  sendState = digitalRead(buttonsend);
  // set the cursor to column 0, line 1  
  // (note: line 1 is the second row, since counting begins with 0):
  lcd.setCursor(posx, posy);
  // print the number of seconds since reset:
  // lcd.print(1000/1000);
  
  if (buttonState1 == 1) {
    // turn LED on:
    timeReleased = millis() - startPressed;
    if (timeReleased < 300) {
      lcd.print("A");
//      char str[] = "A";
//      strcat((char*)msg1, str);
      const char msg1[] = "A"; 
      delay(300); 
    }
  }
  if (buttonState2 == 1) {
    // turn LED on:
    timeReleased = millis() - startPressed;
    if (timeReleased < 300) {
      lcd.print("B");
      const char msg1[] = "B"; 
      delay(300); 
    }
  }
  if (buttonState3 == 1) {
    // turn LED on:
    timeReleased = millis() - startPressed;
    if (timeReleased < 300) {
      lcd.print("C");
      const char msg1[] = "C"; 
      delay(300); 
    }
  }
  if (buttonState4 == 1) {
    // turn LED on:
    timeReleased = millis() - startPressed;
    if (timeReleased < 300) {
      lcd.print("D");
      const char msg1[] = "D"; 
      delay(300); 
    }
  }
  if (sendState == 1) {
//    timeReleased = millis() - startPressed;
//    if (timeReleased < 300) {
      radio.write(&msg1, sizeof(msg1));
      lcd.clear();
      lcd.setCursor(0, 0);
      lcd.print("I-clicker for ZJUI");
      posx = 0;
      posy = 1;
      delay(500);
//    }
  }
//    if (timeReleased >= 3000) {
//      lcd.clear();
//      lcd.setCursor(0, 0);
//      lcd.print("hello, world!");
//      posx = 0;
//      posy = 1;
//    }
  startPressed = millis();
  delay(100);  
}
