#include <SoftwareSerial.h>
#include <FPM.h>
#include <Servo.h>
SoftwareSerial softSer(2, 3);
FPM monitor(&softSer);
FPM_System_Params params;
#define IM_SIZE 36864UL
uint8_t imBuff[IM_SIZE];
Servo myservo;

void waitForFinger(){
    int16_t p = -1;
    Serial.println("finger ...");
    while (p != FPM_OK) {
        p = monitor.getImage();

    }
}


void sendIm(void) {
    if (!set_packet_len_128()) {
        return;
    }

    delay(100);

    waitForFinger();


    p = monitor.downImage();
    if (p != FPM_OK){
        Serial.println("stream error");
        return ;
    }


    bool rf;
    uint16_t len = IM_SIZE;
    uint16_t temp = 0;
    int16_t n = 0;

    while (true) {
        bool ret = monitor.readRaw(FPM_OUTPUT_TO_BUFFER, imBuff + temp, &rf, &len);
        if (ret) {
            n++;
            temp += len;
            len = IM_SIZE - temp;
            if (rf)
                break;
        }
        else {
            Serial.print("Error at");
            Serial.println(n);
            return;
        }
        yield();
    }

}

void rotate(){
    myservo.attach(7);
    if (myservo.read() != 0){
      myservo.write(0);
      delay(1000);
    }
    myservo.write(180);
    delay(1000);  // tell servo to go to position in variable 'pos'
    myservo.write(0);
    delay(1000);

    myservo.detach();
                    // waits 15ms for the servo to reach the position
}

void setup()
{
 myservo.attach(7);
  myservo.write(0);
  myservo.detach();
    Serial.begin(57600);

    softSer.begin(57600);

    if (monitor.begin()) {
        monitor.readParams(&params);
        Serial.println("sensor is found!");

    }
    else {
        Serial.println("error:(");
        while (1) yield();
    }
}

void loop() {
    sendIm();
    while (1) yield();
}



