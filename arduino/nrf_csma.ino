// CSMA/CA Algorithm test coding on arduino board
// Mainly refer from example code for basic setup.
#include "../include/SPI.h" // delete LibSpi when compile.
#include "nRF24L01.h"
#include <RF24.h>
#include "arduino/Libs/EEPROM.h"
#include <cstdlib>
#include <cstring>
// modify the library before compile.
#include "../include/SPI.h"
// not used in final compile.
#include <cstdint>
// add arduino SPI.
#define DELAY 1000 // 1 second.
#define DIFS 50     // 50 ms
#define CCA 1      // 1ms for CCA window.
// constructor RF24
RF24 radio(7,8); // enable Chip-enable and Chip select.

// create logical address for RF.
uint8_t address[][6] = {"1Node","2Node"};

uint8_t radioAddr = 1; // Using # address to Transmit

int8_t NodeID = -1;

char classID[8]; // class ID would take 1 bytes. stored in string.

uint8_t channelID = 0; // default running on 2.400 Ghz.

typedef struct Payload_clicker{
    char msg[7];
    uint8_t counter;
}clickerload; // struct with 8 bytes work as out payload. Need to be larger?

clickerload Test_load;

void setPayload(clickerload& pay, char* message) {
    int length = sizeof(message)/sizeof(char);
    if (length > 7){
        length = 7;
    }
    for (int i=0;i< length;i++){
        pay.msg[i] = message[i];
    }
    pay.counter = 0;
}


// we can modify the void* to a list then we can transmit multiple payload.

/*
 *  unslotted_trans
 *  transmit the given payload packet using csma/ca By IEEE.
 *
 *  @param payload the given payload packet.
 *  @param NodeID given node ID to transmit.
 *
 *  @return
 *  - 'counts' collision counts if success,
 *  - '-1' if failure.
 */
int8_t unslotted_trans(void* payload ,int8_t NodeID = -1){

    uint8_t count_down = 0;
    int8_t col_count = 0;
    const uint8_t max_col = 10;
    const uint8_t win_size = 7;
    uint8_t window[7] = {1,7,15,31,63,127,255};

    bool approve = false;
    bool success = false;

    radio.flush_tx();
    radio.startListening();

    // First Transmission Trial.
    if (!radio.testRPD()){
        delayMicroseconds(CCA);
        if (!radio.testRPD()){
            approve = true;
        } else {
            // collision in CCA window. Maybe useful in further enhancement.
        }
    }
    // First trial failed. Add a backoff window.
    if (!approve){
        if (NodeID != -1){
            srand(NodeID);
        }else{
            srand(rand());
        }
        col_count ++;
        count_down = rand()%(window[col_count]);
    }

    // Loop Trial until success or max count
    while(!success || col_count >= max_col){
        if (!approve){
            delayMicroseconds(DIFS);
            if (!radio.testRPD()){
                delayMicroseconds(CCA);
                if (!radio.testRPD()){
                    count_down--;
                }
            }
        }
        // count down drop to zero.
        if (!count_down){
            radio.stopListening();
            bool report = radio.write(&payload, sizeof(clickerload));
            if (report){
                success = true;
            }else{
                // Timeout happened. collision.
                col_count ++;
                if (col_count < win_size){
                    count_down = rand()%window[col_count];
                } else{
                    count_down = rand()%window[win_size];
                }
                success = false;
                approve = false;
                radio.reUseTX();
                radio.startListening();
            }
        }
    }
    // finalize transmission.
    radio.txStandBy();
    if (success) {
        return col_count;
    } else{
        return -1;
    }
}


void setup(){

    // set in the python code.
    Serial.begin(9600);
    while (!Serial){
        // wait until serial response.
    }

    // call radio begin to setup chip.
    if (!radio.begin()){
        Serial.println(F("Testing Code for CSMA function "))
        while(1){};
        // need to restart the chip.
    }

    // State have already set to Tx mode.
    Serial.println(F("Chip Start With CSMA testing mode. "));

    // may set to automatic issued ID in the future
    Serial.println(F("Enter The node id. Default is 0. "));
    while (!Serial.available()){}

    char input = Serial.parseInt();
    NodeID = (int)input;

    Serial.print(F("NodeID = "));
    Serial.println(NodeID);

    // set radio parameters.
    // set payload
    radio.setPayloadSize(sizeof(clickerload));
    // remember test b4 set to max !!
    radio.setPALevel(RF24_PA_LOW);
    // set read and write pipeline. radio Addr = 1
    radio.openReadingPipe(1,address[radioAddr]);
    radio.openWritingPipe(address[!radioAddr]);

    radio.startListening();
    setPayload(Test_load,"123456");
}

// if included the printf.h, we can call some debug
// functions here.

void loop(){
    int test = unslotted_trans(&Test_load,NodeID);
    if (test != -1){
        Serial.print(F("Trans Success! Collision times = "));
        Serial.println((int)test);
        Test_load.counter++;
    } else{
        Serial.println(F("Max retried times reached!"));
    }
    delay(DELAY);
}

// Handshake with the server and read about the node ID and current class.
// using default channel to communicate with the
// @global parameters affected: NodeID, channelID, classID.
// @return: return the status of the communication.

uint8_t pair(uint8_t* base_addr){
    // assume an ID was attached to the arduino flash.
    radio.toggleAllPipes(false);
    radio.openWritingPipe(base_addr); // always use pipe 0;
    radio.openReadingPipe(1,base_addr);

    clickerload handshake;
    char message = NodeID+'0';
    setPayload(handshake,&message);

    // transmit the payload to the base address.
    int8_t report = unslotted_trans(&handshake,NodeID);
    if (report >= 0){
        // handshake successful.
        radio.startListening();
        Rxmode = 1;
        // drop into rx mode.
    }else{
        return -1;
    }

    // receive for the handshake message.

    // TODO: Under investigation. We need to design the pairing model

}