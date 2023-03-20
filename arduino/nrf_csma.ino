// CSMA/CA Algorithm test coding on arduino board
// Mainly refer from example code for basic setup.
#include <./LibSPI/SPI.h> // delete LibSpi when compile.
#include <nRF24L01.h>
#include <RF24.h>
#include <cstdlib>
// not used in final compile.
#include <cstdint>
// add arduino SPI.
#define DELAY 1000 // 1 second.
#define DIFS 50     // 50 ms
// constructor RF24
RF24 radio(7,8); // enable Chip-enable and Chip select.

// create logical address for RF.
uint8_t address[][6] = {"1Node","2Node"};

uint8_t radioAddr = 1; // Using # address to Transmit

uint8_t NodeID = 0;

uint8_t count_down = 0;

uint8_t col_count = 0;

uint8_t window[7] = {1,7,15,31,63,127,255};

bool Rxmode = 0; // True for rx mode, false for Tx mode.


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

void backoff(bool success){

    if (success){
        col_count = 0;
    } else{
        col_count ++;
    }
    // calculate the current backoff count.
    if (!NodeID){
        // NodeID not been set!
        srand(radio.getChannel());
    }
    if (col_count>6){
        col_count = 6;
    }
    count_down = rand()%(window[col_count]);
}

void setup(){

    // set in the python code.
    Serial.begin(9600);
    while (!Serial){
        // wait until serial response.
    }

    // call radio begin to setup chip.
    if (!radio.begin()){
        Serial.println(F("code example!"))
        while(1){};
        // need to restart the chip.
    }

    // State have already set to Tx mode.
    Serial.println(F("Chip Start With CSMA.ino"));

    // may set to automatic issued ID in the future
    Serial.println(F("Enter The node id. Default is 0. "));
    while (!Serial.available()){};

    // TODO: check the IClicker bottom setting.

    char input = Serial.parseint();
    NodeID = (int)input;
    srand(NodeID);
    Serial.print(F("NodeID = "));
    Serial.println(NodeID);

    // set radio parameters.
    // set payload
    radio.setPayloadSize(sizeof(clickerload));
    // remember test b4 set to max !!
    radio.setPALevel(RF24_PA_MIN);

    // set read and write pipeline. radio Addr = 1
    // avoid using pipe 0 to RP.
    radio.openReadingPipe(1,address[radioAddr]);
    radio.openWritingPipe(address[!radioAddr]);

    radio.startListening();
    setPayload(Test_load,"123456");
}

// if included the printf.h, we can call some debug
// functions here.

void loop(){
    // check the carrier status.
    if (count_down == 0){
        count_down = 1;
        // increase the countdown to 1.
    }

    if (!radio.testRPD()){
        // channel empty. Transmit to Node 0.
        count_down --;
        if (!count_down){
            radio.stopListening();
            delay(DIFS);
            bool report = radio.write(Test_load, sizeof(clickerload));
            if (report){
                Serial.print(F("Sent. count: "));
                Serial.println(Test_load.counter);
                Test_load.counter++;
                // reset the counter.
                backoff(1);
            } else {
                Serial.println(F("Trans Timeout!"));
                // reset the counter.
                backoff(0);
            }
            radio.startListening();
        }
    }

    delay(DELAY);
}


