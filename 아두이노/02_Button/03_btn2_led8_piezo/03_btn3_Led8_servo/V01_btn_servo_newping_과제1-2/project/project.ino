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

  digitalWrite(PIN_TRIG, HIGH);
  delay(10);
  digitalWrite(PIN_TRIG, LOW);
  cycletime = pulseIn(PIN_ECHO, HIGH); //아두이노 핀으로 입력되는 펄스의 시간을 측정하는 함수
  distance = ((340 * cycletime) / 10000) / 2;  //거리 = 속력 X 시간

  // Serial.print("Distance:");
  // Serial.print(distance);
  // Serial.println("cm");

  if(distance < 10){  
      Serial.println(" servo "+ String(servo_angle));
      servo_angle += servo_step;

      if(servo_step > 0){
        if(servo_angle > 180){
          servo_angle = 180;
          servo_step = -10;
        }
      }else{
        if(servo_angle < 0){
          servo_angle = 0;
          servo_step = 10;
        }
      }
      myservo.write(servo_angle);
  }
  delay(10);
}