// include the library code:
#include <LiquidCrystal.h>
#include <SPI.h>
#include <string.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <avr/boot.h>
#include <stdlib.h>

void init_nrf(bool state);

RF24 radio(7, 8); // CE, CSN
const byte address[6] = "00001";
#define TIMESET 100 //
bool lcdstate = HIGH;

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
const int contrast = 6;
int val = 0;
int posx = 0;
int posy = 1;
char msg1[] = " ";
int timer = 100;
const int rs = 10, en = 9, d4 = 5, d5 = 4, d6 = 3, d7 = 2;
LiquidCrystal lcd(rs, en, d4, d5, d6, d7);


void setup() {
    pinMode(contrast, OUTPUT); // 配置 引脚模式为输出模式
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
    lcd.print("Clicker for ZJUI");

    // initialize the pushbutton pin as an input:
    Serial.begin(9600);
    radio.begin();
    radio.openWritingPipe(address);
    radio.setPALevel(RF24_PA_MAX);
    radio.stopListening();
}

void loop() {
    uint32_t deviceID = ((uint32_t)boot_signature_byte_get(0x00) << 16) |
                        ((uint32_t)boot_signature_byte_get(0x01) << 8) |
                        ((uint32_t)boot_signature_byte_get(0x02));
    char dataID[10];
    dtostrf(deviceID, 10, 0, dataID);// TRANSFER THE DATA FORM TO CHAR.
    buttonState1 = digitalRead(buttonPin1);
    buttonState2 = digitalRead(buttonPin2);
    buttonState3 = digitalRead(buttonPin3);
    buttonState4 = digitalRead(buttonPin4);
    sendState = digitalRead(buttonsend);

    digitalWrite(contrast,lcdstate);

    // set the cursor to column 0, line 1
    // (note: line 1 is the second row, since counting begins with 0):
    lcd.setCursor(posx, posy);
    // print the number of seconds since reset:
    // lcd.print(1000/1000);

    if (buttonState1 == 1) {
        // turn LED on:
        timeReleased = millis() - startPressed;
        if (timeReleased < 300) {
            strcpy(msg1, "A");
            lcd.print(msg1);
            timer = TIMESET;
            init_nrf(lcdstate);
            delay(300);
        }
    }
    if (buttonState2 == 1) {
        // turn LED on:
        timeReleased = millis() - startPressed;
        if (timeReleased < 300) {
            lcd.print("B");
            strcpy(msg1, "B");
            timer = TIMESET;
            init_nrf(lcdstate);
            delay(300);
        }
    }
    if (buttonState3 == 1) {
        // turn LED on:
        timeReleased = millis() - startPressed;
        if (timeReleased < 300) {
            lcd.print("C");
            strcpy(msg1, "C");
            timer = TIMESET;
            init_nrf(lcdstate);
            delay(300);
        }
    }
    if (buttonState4 == 1) {
        // turn LED on:
        timeReleased = millis() - startPressed;
        if (timeReleased < 300) {
            lcd.print("D");
            strcpy(msg1, "D");
            timer = TIMESET;
            init_nrf(lcdstate);
            delay(300);
        }
    }
    if (sendState == 1) {
        uint8_t len = strlen(dataID);
        uint8_t packet[len + 1];
        memcpy(packet, msg1, strlen(msg1));
        memcpy(packet + 1, dataID, len);
        radio.write(&packet, sizeof(packet));
        //radio.write((const uint8_t*)&msg1, sizeof(msg1)); // 发送字符串
        strcpy(msg1, "");
        //radio.write((const uint8_t*)&dataID, sizeof(dataID)); // 发送字符串
        lcd.clear();
        lcd.setCursor(0, 0);
        lcd.print("Clicker for ZJUI");
        //lcd.print(dataID);
        timer = TIMESET;
        init_nrf(lcdstate);
        posx = 0;
        posy = 1;
        delay(300);
    }

    startPressed = millis();
    timer -=1;
    if (timer <=0){
        lcd.noDisplay();
        lcdstate = LOW;
        radio.powerDown();
    }
    else{
        lcdstate = HIGH;
        lcd.display();
    }
    delay(100);
}

void init_nrf(bool state){
    if (state == LOW){
        Serial.begin(9600);
        radio.begin();
        radio.openWritingPipe(address);
        radio.setPALevel(RF24_PA_MAX);
        radio.stopListening();
    }
}