#include <./LibSPI/SPI.h> // delete LibSpi when compile.
#include "nRF24L01.h"
#include <RF24.h>
#include <cstdlib>
// not used in final compile.
#include <cstdint>
// add arduino SPI.
#define DELAY 1000 // 1 second.
#define DIFS 50     // 50 ms

RF24 radio(7,8);

uint8_t RadioAddr = 0; // work as the central node.

uint8_t address[][6] = {"1Node","2Node"};

bool Rxmode = 1; // working as receiver.

typedef struct Payload_clicker{
    char msg[7];
    uint8_t counter;
}clickerload;

void setup() {
    Serial.begin(9600);
    while(!Serial){}

    if (!radio.begin()){
        while(1){}
    }
    radio.openReadingPipe(1, address[RadioAddr]);
    radio.openWritingPipe(address[!RadioAddr]);

    radio.setPALevel(RF24_PA_MIN);
    radio.startListening();
}


void loop(){
    uint8_t pipe;
    clickerload Recv;
    if (radio.available(&pipe)){
        // read the pipe number and the payload.
        uint8_t payload_size = radio.getPayloadSize();
        radio.read(&Recv, payload_size);
        Serial.println(Recv.msg);
    }
}
