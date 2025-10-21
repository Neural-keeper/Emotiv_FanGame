// Arduino code to receive mental commands from Node.js bridge
String command = "";
float strength = 0.0;
int fanPin = 9;  // D9 connected to XY-MOS IN/PWM

void setup() {
  pinMode(fanPin, OUTPUT);
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  Serial.println("Arduino ready for mental commands");
}

void loop() {
  if (Serial.available()) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    
    // Parse command,strength format
    int commaIndex = data.indexOf(',');
    if (commaIndex > 0) {
      command = data.substring(0, commaIndex);
      strength = data.substring(commaIndex + 1).toFloat();
      
      Serial.print("Received: ");
      Serial.print(command);
      Serial.print(" (");
      Serial.print(strength);
      Serial.println(")");
      
      // Handle different commands
      // handleCommand(command, strength);
      fan(strength);
    }
  }
}

void handleCommand(String cmd, float str) {
  if (str > 0.3) { // Only act on strong commands
    
    if (cmd == "lift") {
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("LED ON - LIFT command");
    }
    else if (cmd == "push") {
      // Blink LED fast
      for (int i = 0; i < 5; i++) {
        digitalWrite(LED_BUILTIN, HIGH);
        delay(100);
        digitalWrite(LED_BUILTIN, LOW);
        delay(100);
      }
      Serial.println("LED BLINK - PUSH command");
    }
    else if (cmd == "left") {
      // Pulse LED
      for (int i = 0; i < 255; i += 5) {
        analogWrite(LED_BUILTIN, i);
        delay(10);
      }
      analogWrite(LED_BUILTIN, 0);
      Serial.println("LED PULSE - LEFT command");
    }
    else if (cmd == "right") {
      // Quick flash
      digitalWrite(LED_BUILTIN, HIGH);
      delay(500);
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("LED FLASH - RIGHT command");
    }
    
  } else {
    // Weak command or neutral
    digitalWrite(LED_BUILTIN, LOW);
  }
}

void fan(float str){
  float str_speed= (str*255);
  analogWrite(fanPin,str_speed);
    if(str == 0.35)
      analogWrite(fanPin, 0);
}