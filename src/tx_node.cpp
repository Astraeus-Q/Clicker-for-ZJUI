#include <Wire.h>
#include <SPI.h>
#include <string.h>
#include <nRF24L01.h>
#include <RF24.h>
#include <avr/boot.h>
#include <stdlib.h>
#define SPI_CLOCK 4000000

// 引入驱动OLED0.96所需的库
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
RF24 radio(9, 10); // CE, CSN
#define SCREEN_WIDTH 128 // 设置OLED宽度,单位:像素
#define SCREEN_HEIGHT 64 // 设置OLED高度,单位:像素
#define MIN_CLOCK 100/26 // 设置OLED高度,单位:像素
int sendState = 0;
const int buttonsend = 3;
const int buttonPin4 = 17;
const int buttonPin3 = 16;
const int buttonPin2 = 15;
const int buttonPin1 = 14;
const int buttonreturn = 2;
int startPressed = 0;
int timeReleased = 0;
char msg1[] = " ";
int buttonState1 = 0;
int buttonState2 = 0;
int buttonState3 = 0;
int buttonState4 = 0;
int returnState = 0;
#define OLED_RESET 19
const byte address[6] = "00001";

Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, OLED_RESET);

void words_display();

void setup()
{
    // 初始化Wire库
    //  Wire.begin();
    SPCR |= bit (MSTR);
    digitalWrite(SS, HIGH);
    pinMode(SS, OUTPUT);
    SPI.begin();
    SPISettings spiSettings (SPI_CLOCK, MSBFIRST, SPI_MODE0);
    SPI.beginTransaction (spiSettings);
    pinMode(buttonPin4, INPUT);
    pinMode(buttonPin3, INPUT);
    pinMode(buttonPin2, INPUT);
    pinMode(buttonPin1, INPUT);
    pinMode(buttonreturn, INPUT);
    pinMode(buttonsend, INPUT);

    // 初始化OLED并设置其IIC地址为 0x3C
    display.begin(SSD1306_SWITCHCAPVCC, 0x3C);
    //  display.setCursor(0, 0);
    //  display.print("Clicker for ZJUI");
    radio.begin();
    radio.openWritingPipe(address);
    radio.setPALevel(RF24_PA_MAX);
    radio.stopListening();
}

void loop()
{
    uint32_t deviceID = ((uint32_t)boot_signature_byte_get(0x00) << 16) |
                        ((uint32_t)boot_signature_byte_get(0x01) << 8) |
                        ((uint32_t)boot_signature_byte_get(0x02));
    char dataID[10];
    dtostrf(deviceID, 10, 0, dataID);// TRANSFER THE DATA FORM TO CHAR.
    sendState = digitalRead(buttonsend);
    buttonState1 = digitalRead(buttonPin1);
    buttonState2 = digitalRead(buttonPin2);
    buttonState3 = digitalRead(buttonPin3);
    buttonState4 = digitalRead(buttonPin4);
    returnState = digitalRead(buttonreturn);

    if (buttonState1 == 0) {
        words_display();
        strcpy(msg1, "A");
        display.print("A");

    }
    if (buttonState2 == 0) {
        strcpy(msg1, "B");
        words_display();
        display.print("B");
    }
    if (buttonState3 == 0) {
        strcpy(msg1, "C");
        words_display();
        display.print("C");
    }
    if (buttonState4 == 0) {
        strcpy(msg1, "D");
        words_display();
        display.print("D");
    }
    if (returnState == 0) {
        words_display();
    }
    if (sendState == 0) {
        uint8_t len = strlen(dataID);
        uint8_t packet[len + 1];
        memcpy(packet, msg1, strlen(msg1));
        memcpy(packet + 1, dataID, len);
        radio.write(&packet, sizeof(packet));
        strcpy(msg1, "");
        words_display();
    }
    //display.display();
    display.display();
    startPressed = millis();
    //  delay(0.1*MIN_CLOCK);
}

void words_display()
{
    display.clearDisplay();
    display.setTextColor(WHITE);
    display.setTextSize(1.5);
    display.setCursor(0, 0);
    display.print("Clicker for ZJUI");
    display.setCursor(0, 20);
    display.print("Your Answer: ");
    //  display.setCursor(0, 40);
    //  display.print("Author: ");
    //  display.print("Dapenson");
}
