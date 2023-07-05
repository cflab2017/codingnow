
#define PIN_TRIG A1
#define PIN_ECHO A2

#define MAX_LED 8
unsigned char arry_led[MAX_LED] = {
2,3,4,5,6,7,8,9
};

void setup() {
  int i;
  Serial.begin(9600);
  
  pinMode(PIN_TRIG, OUTPUT);
  pinMode(PIN_ECHO, INPUT);

  for(i=0; i<MAX_LED; i++)
  {
    pinMode(arry_led[i], OUTPUT);
  }
}

void loop() {
  int i;
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

  for(i=0; i<MAX_LED; i++){
    if((distance > (i*5)) && (distance <= (i*5)+5))
    {
      digitalWrite(arry_led[i], HIGH);
    }else{
      digitalWrite(arry_led[i], LOW);
    }
  }
  delay(100);
}
