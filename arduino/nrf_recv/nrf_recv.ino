/*
* Arduino Wireless Communication Tutorial
*       Example 1 - Receiver Code
*                
* by Dejan Nedelkovski, www.HowToMechatronics.com
* 
* Library: TMRh20/RF24, https://github.com/tmrh20/RF24/
*/
#include <SPI.h>
#include "nRF24L01.h"
#include <RF24.h>
RF24 radio(7, 8); // CE, CSN
const byte address[6] = "10000";
void setup() {
  Serial.begin(9600);
  radio.begin();
  radio.setChannel(100);
  radio.setDataRate(RF24_250KBPS);
  radio.openReadingPipe(1, address);
  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
}
void loop() {
  if (radio.available()) {
    char text[32] = "";
    radio.read(&text, sizeof(text));
    Serial.println(text);
  }
}