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

#include <printf.h>
RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";
const byte addr1[6] = "22222";
void setup() {
  Serial.begin(9600);
  printf_begin();
  radio.begin();
  radio.setChannel(0);
  // radio.setAutoAck(1,false);
  radio.openReadingPipe(0, address);
  radio.openReadingPipe(1, address);

  radio.setPALevel(RF24_PA_MIN);
  radio.startListening();
  radio.printPrettyDetails();
}
void loop() {
  if (radio.available()) {
    char text[32] = "";
    radio.read(&text, sizeof(text));
    Serial.println(text);
  }
}