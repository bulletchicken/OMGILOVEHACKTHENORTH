#include <Servo.h>
Servo move;  // 0 to stop, 105 max speed
Servo turn;  // 90 default

void setup() {
  Serial.begin(4800);
  Serial.print("hello3");
  move.attach(2);  // signal line of Servo is with DPin-2
  move.write(0);   // initial position of Servo at 90 degrees (stop)
  turn.attach(3);
  turn.write(180);
}

void loop() {
  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    char firstChar = input.charAt(0);
        Serial.print("Input: ");
    Serial.println(input);
    Serial.print("First char is 'f': ");
    Serial.println(firstChar == 'f' ? "true" : "false");
    if (firstChar == 't') {
      input = input.substring(1);
      int angle = input.toInt();
      turn.write(angle);
      Serial.println("move: " + String(angle));
    } else if (firstChar == 'm') {
      input = input.substring(1);
      int angle = input.toInt();
      move.write(angle);
      Serial.println("turn: " + String(angle));
    } else {
      Serial.println("Unknown command");
    }
  }
  delay(1000);
}