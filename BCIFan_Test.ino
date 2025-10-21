int fanPin = 9;  // D9 connected to XY-MOS IN/PWM

void setup() {
  pinMode(fanPin, OUTPUT);
}

void loop() {
  // Ramp fan speed up
  for (int speed = 0; speed <= 255; speed += 5) {
    analogWrite(fanPin, speed); // 0 = off, 255 = full speed
    delay(50);
  }

  // Ramp fan speed down
  for (int speed = 255; speed >= 0; speed -= 5) {
    analogWrite(fanPin, speed);
    delay(50);
  }
}
