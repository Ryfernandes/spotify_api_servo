#include <Servo.h>

Servo servo1;

int servoPin = 13;
int rotation = 0;

//starts serial connection for communication with api program and attaches pin for servo
void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  servo1.attach(servoPin);
}

//waits for serial communication and then moves servo to speicified point; used arduino documentation as reference
void loop() {
  while (!Serial.available());
  rotation = Serial.readString().toInt();
  if(rotation == 0 || rotation == 90 || rotation == 180) {
    servo1.write(rotation);
  }
}
