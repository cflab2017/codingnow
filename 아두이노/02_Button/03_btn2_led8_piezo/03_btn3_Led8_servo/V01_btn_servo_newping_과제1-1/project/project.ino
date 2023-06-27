#include <Servo.h> 

/*초음파센서*/
#define PIN_TRIG A1
#define PIN_ECHO A2

/*서보모터*/
#define PIN_SERVO 12

Servo myservo;
int servo_angle = 0; //서보모터의 현재 각도를 저장하는 변수
int servo_step = 10;

void setup() {
  int i;
  Serial.begin(9600);
  
  pinMode (PIN_SERVO, OUTPUT);
  myservo.attach(PIN_SERVO);
  servo_angle = 120;
  myservo.write(servo_angle);
  delay(100);
  
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);

  Serial.println("start");
}

void loop() {
  float cycletime;
  float distance;
 
  for(servo_angle=0; servo_angle<180; servo_angle+=10)
  {      
    digitalWrite(PIN_TRIG, HIGH);
    delay(10);
    digitalWrite(PIN_TRIG, LOW);
    cycletime = pulseIn(PIN_ECHO, HIGH); //아두이노 핀으로 입력되는 펄스의 시간을 측정하는 함수
    distance = ((340 * cycletime) / 10000) / 2;  //거리 = 속력 X 시간
    
    if(distance < 10){
      myservo.write(servo_angle);
      Serial.println(" servo "+ String(servo_angle));
      delay(10);
    }      
  }
  delay(10);
}