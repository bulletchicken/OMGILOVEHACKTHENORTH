#include <Servo.h>

Servo head;
Servo rightArm;
Servo leftArm;

int sound_sensor2 = A2; //assign to pin A2
int sound_sensor = A1; //assign to pin A2

int PulseSensor = 7;
int Signal;
int Threshold = 550;

int timer = 0;

void setup() 
{
  Serial.begin(9600); //begin Serial Communication
  head.attach(2);
  rightArm.attach(3);
  leftArm.attach(4);

  head.write(90);
  rightArm.write(70);
  leftArm.write(90);
}
 
void loop()
{
  timer++;
  delay(10);
  if(timer>1000){
    idle();
    idle();
    idle();
    timer = 0;
  }


  if (Serial.available() > 0) {
    String input = Serial.readStringUntil('\n');
    input.trim();
    if(input=="wave"){
      wave();
    }
    else if(input=="readPulse"){
      readPulse();
    }
    else if(input=="leftRight"){
      leftRight();
    }

    else if(input=="dance"){
      dance();
    }
  }

}

void wave(){
  for(int i = 0; i < 5; i++){
    rightArm.write(0);
    delay(100);
    rightArm.write(70);
    delay(100);
  }
}

void readPulse(){
  leftArm.write(180);
  delay(5000);
  Signal = analogRead(PulseSensor);
  Serial.println(Signal);
  delay(100);
  leftArm.write(90);
}

void leftRight(){
    
  int soundValue = 0; //create variable to store many different readings
  soundValue = analogRead(sound_sensor); //read the sound sensor
  soundValue >>= 5; //bitshift operation 

  int soundValue2 = 0;
  soundValue2 = analogRead(sound_sensor2);
  soundValue2 >>= 5;


  if(soundValue2>soundValue){
    //turn head left
    head.write(180);
    delay(3000);
  }else{
    head.write(0);
    delay(3000);
  }
  head.write(90);
}

void idle(){
  leftArm.write(0);
  rightArm.write(100);
  delay(500);
  leftArm.write(40);
  rightArm.write(70);
  delay(500);
}

void dance(){
  leftArm.write(180);
  rightArm.write(0);
  delay(500);
  leftArm.write(0);
  rightArm.write(180);
  delay(500);
}