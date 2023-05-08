//
// Created by jordan on 23-4-20.
//
#include <SPI.h>
#include <Arduino.h>
#include <RF24.h>
#include <Wire.h>
// testing tx node transmission.


// control the tx node with the

uint8_t enhanced_transmit(void* payload1, size_t size, int8_t id);

typedef struct Payload_clicker{
    char msg[7];
    uint8_t counter;
}payload;

void Read_package(payload packet, String* result);

RF24 radio(7,8);

uint8_t RadioAddr = 1; // clicker simulation

uint8_t address[][6] = {"00001","00002"};

bool Rxmode = false;

payload Sign_in_test;

char device_id[11] = "arduino ";


void setup() {
    Serial.begin(9600);
    while(!Serial){}

    if (!radio.begin()){
        Serial.println(F(" nRF24 not connected! Reboot. "));
        while(1){}
    }

    radio.setPALevel(RF24_PA_MIN);

    radio.openWritingPipe(address[!RadioAddr]);
    radio.openReadingPipe(1, address[RadioAddr]);

    radio.startListening();
//    radio.setPayloadSize(sizeof(payload));
//
//    // Serial testing
//    Serial.println(F(" Please Enter the Role for this node. T for TX, R for RX."));
//    while (!Serial.available()){}
//    delay(100);
//    char input = toupper(Serial.read());
//    if (input == 'T'){
//        // tx node.
//        Serial.print(F(" This is currently a Tx node. "));
//        RadioAddr = 1;
//    }
//    else{
//        // rx mode.
//        Serial.print(F(" This is a Rx node. "));
//        RadioAddr = 0;
//        Rxmode = true;
//    }
//
//    radio.openReadingPipe(1, address[RadioAddr]);
//    radio.openWritingPipe(address[!RadioAddr]);
//
//    // we then "ASSIGN" the reading pipe as the RX node's address.
//
//    memcpy(Sign_in_test.msg, address[RadioAddr],5);
//    Serial.println(Sign_in_test.msg);
//
//    Sign_in_test.msg[5] = '|';
//    Sign_in_test.msg[6] = 0;
//
//    if (Rxmode){
//        // set up package.
//        radio.startListening();
//    }
//    else{
//        // start as TX node.
//        radio.stopListening();
//    }

}

void loop(){
    // ________________________________ DISPLAY TEST ___________________________________
    device_id[8] = '\0';
    Serial.println(F("INPUT ANSWER! "));
    while(!Serial.available()){
        delay(100);
    }

    char input;
    input = Serial.read();


    switch (input) {
        case 'a':
            device_id[8] = 'A';
            break ;
        case 'b':
            device_id[8] = 'B';
            break ;
        case 'c':
            device_id[8] = 'C';
            break ;
        case 'd':
            device_id[8] = 'D';
            break ;
        default:
            break ;
    }

    Serial.print(device_id);
    Serial.println(F(" Would be transmitted. Press to SEND. "));
    while (!Serial.available()){
        delay(100);
    }
    uint8_t trash = Serial.available();
    while (trash){
        Serial.read();
        trash--;
    }

    radio.stopListening();
//
    uint8_t uid = 12345;
    uint8_t report = enhanced_transmit(device_id, sizeof(device_id),uid);
//    bool report = radio.write(device_id, sizeof(device_id));
    if (report){
        Serial.println(F("Trans Success. "));
    } else {
        Serial.println(F("Trans Failed. "));
    }
    delay(100);

    Serial.println(F("Wait for correct answer. "));

    radio.startListening();
    while (!radio.available()){
        delay(100);
    }

    char raw_content[32] = "";
    radio.read(&raw_content, 31);
    //             String* content = Read_package(Recv);
    Serial.println(raw_content);

    // _________________________________ OLD TEST ______________________________________
//    if (Rxmode){
//        // work as RX mode.
//        uint8_t pipe;
//        if (radio.available(&pipe)){
//            payload received;
//            radio.read(&received, sizeof(received));
//            radio.stopListening();
//
//            radio.writeFast(&Sign_in_test, sizeof(Sign_in_test));
//            bool report = radio.txStandBy(400);
//
//            Serial.println(F(" Received Successful from"));
//            Serial.print(pipe);
//            Serial.println(F(" Content: "));
//            String pharse[3];
//            Read_package(received, pharse);
//            Serial.print(pharse[0]);
//            radio.startListening();
//
//            delay(1000);
//
//            if (report){
//                Serial.println(F("Reply Successful. "));
//            } else{
//                Serial.println(F("Reply Failed. "));
//            }
//        }
//    } else {
//        // work as TX node.
//        bool report = radio.write(&Sign_in_test, sizeof(payload));
//        if (report) {
//            radio.startListening();
//            Serial.println(F("Transmission Successful. "));
//            unsigned long start_t = millis();
//            while (!radio.available()){
//                if (millis()-start_t >= 600){
//                    break ;
//                }
//            }
//            radio.stopListening();
//            uint8_t pipe;
//            if (radio.available(&pipe)){
//                payload received;
//                radio.read(&received, sizeof(payload));
//                Serial.println(F("Response Received from"));
//                Serial.print(pipe);
//                String test[3];
//                Read_package(received, test);
//                Serial.println(F(" Content: "));
//                Serial.print(test[0]);
//            } else{
//                Serial.println(F(" Response Failed. "));
//            }
//        } else {
//            Serial.println(F(" Trans Failed. "));
//        }
//    }
//    delay(1000);
//    Serial.print(F(" Another Round? "));
//    while (!Serial.available()){}
//    char input = Serial.read();
//    Serial.println(input);
}

void Read_package(payload packet, String* result){
    // Assume packet would be like :
    // Sign-in: ID |
    // Answer: ID | Ans |
    // Maybe More packet types.
    uint8_t length;
    int counts;

    String msg = String(packet.msg);

    length = msg.length();
    // Assume the length of ID is here.
    // Assume Hash into 5 bytes.
//    int ID_size = 4;

    for (int i = 0;i<length;i++){
        if (packet.msg[i]=='|'){
            counts ++;
        }
    }

    if (counts == 1){
        // Sign-in packet
        result[0] = msg.substring(0,5);
    } else if (counts == 2){
        // Answer packet.
        result[0] = msg.substring(0,5);
        result[1] = msg.substring(6,7);
    }
    return ;
}

// test version for unslotted trans.
uint8_t enhanced_transmit(void* payload1, size_t size, int8_t id = 0)
{
    // define DIFS value here, in # ms.
    uint8_t DIFS = 10;
    // test radio status
    if (radio.isFifo(true, false)){
        // transmission FIFO is full.
        // ? maybe we can resend them in this way.
//        Serial.println(F("Check FIFO test. "));
        radio.reUseTX();
        return 0;
    }
    // transmission detection.
    uint8_t count_down = 0;
    uint8_t BE = 0;
    uint8_t col_count = 0;
    uint8_t window_size = 0;

    const uint8_t max_retry = 10;
    const uint8_t max_win_size = 6;
    uint8_t window[7] = {1,7,15,31,63,127,255};

    bool CCAtest = false;
    bool loop_count = false;

    randomSeed(id);

    radio.flush_tx();
    radio.startListening();


    while (col_count <= max_retry){
        if (count_down > 0){
            // countdown according to the CCA rules.
            if (!radio.testRPD()){
                count_down --;
            }
//            else {
//                Serial.println(F("Collision Detected"));
//            }
        } else {
            // perform CCA to detect the channel.
            delay(DIFS);
            if (!radio.testRPD()){
                // CCA test passed.
                CCAtest = true;
            } else{
                // check the window type.
//                Serial.println(F("_______________________CCA Failed_____________________________"));
                if (loop_count){
                    loop_count = false;
//                    Serial.println(F("______________________SECOND COLLISION________________________"));
                    col_count ++;
                    if (col_count >  max_win_size){
                        window_size = max_win_size;
                    } else {
                        window_size = col_count;
                    }
                    // BE counts to zero. reassign values.
                    count_down = random(0,window[window_size] - BE);
                }
                else {
                    loop_count = true;
                    BE = floor(window[window_size] * random(5,9)/10);
                    // counts to BE.
                    count_down = random(0,BE);
                }
            }
        }

        if (CCAtest){
            // transmit the packages.
            radio.stopListening();
            delay(10);
            bool report = radio.write(payload1, size);
            if (report){
//                Serial.print(F("Retry Count: "));
//                Serial.println(col_count);
                return 1;
            }
            else{
                CCAtest = false;
                // transmission failed.
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

        delay(10);
    }
    Serial.println(F("Max Retry times reached. "));
    return 0;
}