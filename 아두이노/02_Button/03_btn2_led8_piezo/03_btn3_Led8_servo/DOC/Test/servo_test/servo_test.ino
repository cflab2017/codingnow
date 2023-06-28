#include <Servo.h> 
#define PIN_SERVO 12
Servo myservo;
int ServoMove = 0;

void setup() {
  Serial.begin(9600);
  
  pinMode (PIN_SERVO, OUTPUT);
  myservo.attach(PIN_SERVO);
  ServoMove = 0;
  myservo.write(ServoMove);
  delay(100);
  Serial.println("start");
}

void loop() {
  {    
    Serial.println(" servo 170 ");
    ServoMove = 170;
    myservo.write(ServoMove);
    delay(500);
  }  
  {    
    Serial.println(" servo 90 ");
    ServoMove = 90;
    myservo.write(ServoMove);
    delay(500);
  }
}