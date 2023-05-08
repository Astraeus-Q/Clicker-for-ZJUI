#include <SPI.h> // delete LibSpi when compile.
#include <nRF24L01.h>
#include <RF24.h>
#include <Wire.h>
// not used in final compile.

typedef struct Payload_clicker{
    char msg[7];
    uint8_t counter;
}payload;

String Read_package(payload packet);
int8_t unslotted_trans(void* payload ,int8_t id);

RF24 radio(7,8);

uint8_t RadioAddr = 0; // work as the central node.

// TODO: packet structure modification !!!!

uint8_t address[][6] = {"00001","00002"};

bool Rxmode = 1; // working as receiver.

bool sign_in = false;       // default in idle mode.
bool poll_in = false;
bool test_   = false;

void setup() {
    Serial.begin(9600);
    while(!Serial){}

    if (!radio.begin()){
        Serial.println(F(" nRF24 not connected! Reboot. "));
        while(1){}
    }
    // radio settings
    radio.setPALevel(RF24_PA_MAX);
//    radio.setPayloadSize(sizeof(payload));
    radio.openWritingPipe(address[!RadioAddr]);
    radio.openReadingPipe(1, address[RadioAddr]);
}


void loop()
{
    uint8_t pipe;
    payload Recv;
    // toy response
    uint8_t counter = 0;
    // Serial variables/buffers.
    uint8_t serial_in;
    String sin, first, second;
    char input[20];
    // loop control

    if (Serial.available()){
        delay(1000);       // wait for all frames.
        // Read from Serial at every loop start.
        serial_in = Serial.available();
        if (serial_in != 0){
             // read control instruction.
             for (int i = 0;i < serial_in; i++){
                 // note that serial read only one char per frame.
                 input[i] = Serial.read();
             }
        }
        // read the settings.
        // TODO: Assume the setting messages would be like:
        // Sign-in: |   Poll:
        // s|1      |   p|1
        // s|0      |   p|0
        sin = String(input);
        first = sin.substring(0, 1);
        second = sin.substring(2, 3);
        if (first == String("s")){
             // sign_in option
             if (second.toInt()) {
                 // enable
                 sign_in = true;
                 Serial.println(F(" Enter Check-in Mode. "));
             } else {
                 sign_in = false;
                 Serial.println(F(" Exit  Check-in Mode. "));
             }
        } else if (first == String("p")) {
             // poll option
             if (second.toInt()) {
                 // enable
                 poll_in = true;
                 Serial.println(F(" Enter Poll Mode. "));
             } else {
                 poll_in = false;
                 Serial.println(F(" Exit  Poll Mode. "));
             }
        } else if (first == String("t")) {
             test_ = true;
        }
    }
    // enters main loop.
    if (sign_in == true) {

        radio.startListening();
        if (radio.available(&pipe)){
             // read the pipe number and the payload.
             uint8_t payload_size = radio.getPayloadSize();
             radio.read(&Recv, payload_size);
             String content = Read_package(Recv);
             // report the sign-in data to database.
             Serial.println(content[0]);
             // reply to the TX clicker.
             payload Cirmfirm;
             memcpy(Cirmfirm.msg, "Ok ",3);
             Cirmfirm.counter = counter;
             counter ++;

             // TODO: need to check the pipeline address in the future.

             radio.openWritingPipe(address[1]);
             radio.stopListening();
             radio.writeFast(&Cirmfirm,sizeof(payload));
             bool report = radio.txStandBy(100); // keep retrying for 100 seconds.
             radio.startListening();
             // We dont need to verity the report.
             if (!report){
                 Serial.println("Response failed. ");
             }
        }
    }
    else if (poll_in){
        // poll mode do not need response.
        radio.startListening();
        if (radio.available(&pipe)){
//             uint8_t payload_size = radio.getPayloadSize();
             char raw_content[32] = "";
             radio.read(&raw_content, 31);
//             String* content = Read_package(Recv);
             Serial.println(raw_content);
        }
        delay(50);
    }

    else if (test_){
        char answer;
        Serial.println(F("Input Answer. "));
        while (!Serial.available()){}
        answer = Serial.read();
        radio.stopListening();
        char ans[8] = "ans:";
        ans[4] = answer;
        bool report = radio.write(&ans, sizeof(ans));
        if (!report){
             Serial.println(ans);
            Serial.println(F("Transmission Failed. "));
        }
        else {
            Serial.println(F("Answer Transmitted:"));
            Serial.println(ans);
        }
        radio.txStandBy();
        test_ = false;
    }

    else {
        // enter sleep mode.
        radio.stopListening();
        radio.txStandBy();
        delay(100);
    }

}


// read the given packet into string list.
String Read_package(payload packet){
    // Assume packet would be like :
    // Sign-in: ID |
    // Answer: ID | Ans |
    // Maybe More packet types.
    uint8_t lengh;
    int counts;
    String msg = String(packet.msg);

    lengh = msg.length();
    String content[3];

    // Assume the length of ID is here.
    // Assume Hash into 5 bytes.
    int ID_size = 4;

    for (int i = 0;i<lengh;i++){
        if (packet.msg[i]=='|'){
            counts ++;
        }
    }

    if (counts == 1){
        // Sign-in packet
        content[0] = msg.substring(0,ID_size);
    } else if (counts == 2){
        // Answer packet.
        content[0] = msg.substring(0,ID_size);
        content[1] = msg.substring(ID_size+1,6);
    }
    return *content;
}


uint8_t enhanced_transmit(RF24 radio, payload* payload1, int8_t id = 0)
{
    // define DIFS value here, in # ms.
    uint8_t DIFS = 10;
    // test radio status
    if (radio.isFifo(true, false)){
        // transmission FIFO is full.
        // ? maybe we can resend them in this way.
        radio.reUseTX();
        return -1;
    }
    // transmission detection.
    uint8_t count_down = 0;
    uint8_t BE = 0;
    uint8_t col_count = 0;
    uint8_t window_size = 0;

    const uint8_t max_retry = 10;
    const uint8_t max_win_size = 7;
    uint8_t window[7] = {1,7,15,31,63,127,255};

    bool CCAtest = false;
    bool loop_count = false;

    randomSeed(id);

    radio.flush_tx();
    radio.startListening();


    while (col_count >= max_retry){
        if (count_down > 0){
            // countdown according to the CCA rules.
            if (!radio.testRPD()){
                 count_down --;
            }
        } else {
            // perform CCA to detect the channel.
            delay(DIFS);
            if (!radio.testRPD()){
                 // CCA test passed.
                 CCAtest = true;
            } else{
                 // check the window type.
                 if (loop_count){
                     loop_count = false;
                     col_count ++;
                     if (col_count >  max_win_size){
                         window_size = max_win_size;
                     } else {
                         window_size = col_count;
                     }
                     // BE counts to zero. reassign values.
                     BE = floor(window[window_size] * random(5,9)/10);
                     count_down = random(0,window[window_size] - BE);
                 }
                 else {
                     loop_count = true;
                     // counts to BE.
                     count_down = random(0,BE);
                 }
            }
        }

        if (CCAtest){
            // transmit the packages.
            radio.stopListening();
            bool report = radio.write(&payload1, sizeof(payload1));
            if (report){
                 return 0;
            }
            else{
                 CCAtest = false;
                 // transmission failed.
                 // DEBUG USAGE
                 Serial.println(F(" Trans Failed. "));

                 loop_count = false;
                 col_count ++;
                 if (col_count >  max_win_size){
                     col_count = max_win_size;
                 } else{
                     window_size = col_count;
                 }
                 BE = floor(window[window_size] * random(5,9)/10);
                 count_down = random(0,window[window_size] - BE);
                 radio.startListening();
            }
        }

        if (col_count > max_retry){
            // transmission failed.
            return -1;
        }
    }
}