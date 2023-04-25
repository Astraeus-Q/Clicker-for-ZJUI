#include <SPI.h> // delete LibSpi when compile.
#include <nRF24L01.h>
#include <RF24.h>
// not used in final compile.

typedef struct Payload_clicker{
    char msg[7];
    uint8_t counter;
}payload;

String* Read_package(payload packet);
int8_t unslotted_trans(void* payload ,int8_t id);

RF24 radio(7,8);

uint8_t RadioAddr = 0; // work as the central node.

uint8_t address[][6] = {"1Node","2Node"};

bool Rxmode = 1; // working as receiver.

void setup() {
    Serial.begin(9600);
    while(!Serial){}

    if (!radio.begin()){
        while(1){}
    }
    // radio settings
    radio.setPALevel(RF24_PA_MAX);
    radio.setPayloadSize(sizeof(payload));

    radio.openReadingPipe(1, address[RadioAddr]);
    radio.openWritingPipe(address[!RadioAddr]);

    radio.startListening();
}


void loop(){
    uint8_t pipe;
    payload Recv;
    // toy response
    uint8_t counter = 0;
    // Serial variables/buffers.
    uint8_t serial_in;
    String sin, first, second;
    char input[20];
    // loop control
    bool sign_in = false;   // default in idle mode.
    bool poll_in = false;

    if (Serial.available()){
        delay(100);     // wait for all frames.
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
             // Sign-in: |Poll:
             // Sign|1   |Poll|1
             // Sign|0   |poll|0
             sin = String(input);
             first = sin.substring(0,4);
             second = sin.substring(5,6);
             if (first == String("Sign")){
                 // sign_in option
                 if (second.toInt()){
                     // enable
                     sign_in = true;
                 }
                 else{
                     sign_in = false;
                 }
             }
             else if (first == String("Poll")){
                 // poll option
                 if (second.toInt()){
                     // enable
                     poll_in = true;
                 }
                 else{
                     poll_in = false;
                 }
             }
    }
    // enters main loop.
    if (sign_in){
        // enters the sign-in loop.
        radio.startListening();
        if (radio.available(&pipe)){
             // read the pipe number and the payload.
             uint8_t payload_size = radio.getPayloadSize();
             radio.read(&Recv, payload_size);
             String* content = Read_package(Recv);
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
             radio.read(&Recv, sizeof(payload));
             String* content = Read_package(Recv);
             Serial.println(Recv.msg);
        }
    }
    else {
        // enter sleep mode.
        radio.stopListening();
        radio.txStandBy();
    }

}


// read the given packet into string list.
String* Read_package(payload packet){
    // Assume packet would be like :
    // Sign-in: ID |
    // Answer: ID | Ans |
    // Maybe More packet types.
    uint8_t lengh;
    int counts;
    String msg = String(packet.msg);
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
        content[0] = msg.substring(0,4);
    } else if (counts == 2){
        // Answer packet.
        content[0] = msg.substring(0,4);
        content[1] = msg.substring(5,6);
    }
    return content;
}

int8_t unslotted_trans(void* payload ,int8_t id = -1){

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
        if (id != -1){
            srand(id);
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
