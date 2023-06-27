#include <Servo.h> 

/*초음파센서*/
#define PIN_TRIG A1
#define PIN_ECHO A2

/*서보모터*/
#define PIN_SERVO 12

/*LED*/
// #define MAX_LED 8
// unsigned char arry_led[MAX_LED] = {
// 2,3,4,5,6,7,8,9
// };

Servo myservo;
int servo_angle = 0; //서보모터의 현재 각도를 저장하는 변수

void setup() {
  int i;
  Serial.begin(9600);
  
  pinMode (PIN_SERVO, OUTPUT);
  myservo.attach(PIN_SERVO);
  servo_angle = 0;
  myservo.write(servo_angle);
  delay(100);
  
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);

  // for(i=0; i<MAX_LED; i++)
  // {
  //   pinMode(arry_led[i], OUTPUT);
  // }

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
    if (servo_angle != 170)
    {    
      Serial.println(" servo 170 "+ String(distance));
      servo_angle = 170;
      myservo.write(servo_angle);
      delay(100);
    }
  }else{
    if (servo_angle != 90)
    {    
      Serial.println(" servo 90 "+ String(distance));
      servo_angle = 90;
      myservo.write(servo_angle);
      delay(100);
    }
  }
  delay(100);
}