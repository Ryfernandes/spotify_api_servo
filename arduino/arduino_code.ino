#include <Servo.h>

Servo servo1;

int servoPin = 13;
int rotation = 0;


void setup() {
  Serial.begin(115200);
  Serial.setTimeout(1);
  servo1.attach(servoPin);
}


void loop() {
  while (!Serial.available());
  rotation = Serial.readString().toInt();
  if(rotation == 0 || rotation == 90 || rotation == 180) {
    servo1.write(rotation);
  }
}
