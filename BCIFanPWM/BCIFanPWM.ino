int fanPin = 9;
int speed = 0;

void setup() {
  pinMode(fanPin, OUTPUT);
  Serial.begin(9600);
  Serial.println("Enter PWM value (0–255):");
}

void loop() {
  if (Serial.available() > 0) {
    speed = Serial.parseInt();         // Read number from Serial
    speed = constrain(speed, 0, 255);  // Limit range
    analogWrite(fanPin, speed);        // Set PWM
    Serial.print("PWM set to: ");
    Serial.println(speed);
  }
}
