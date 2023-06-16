/*GND -- LED -- 220ohm -- PIN*/
#define MAX_LED 8
unsigned char arry_led[MAX_LED] = {
2,3,4,5,6,7,8,9
};

#define CNT_BLICK 3
#define DELAY_CYCLE 100
#define DELAY_BLINK 500

void setup() {
  int i;
  for(i=0; i<MAX_LED; i++){
    pinMode(arry_led[i], OUTPUT);
  }
}

void loop() {
  int i,k;
//정방향
  for(i=0; i<MAX_LED; i++){
    digitalWrite(arry_led[i], HIGH);
    delay(DELAY_CYCLE);
  }

  for(i=0; i<MAX_LED; i++){
    digitalWrite(arry_led[i], LOW);
    delay(DELAY_CYCLE);
  }
  delay(500);

//깜박이기
  for(k=0; k<CNT_BLICK; k++){
    for(i=0; i<MAX_LED; i++){
      digitalWrite(arry_led[i], HIGH);
    }
    delay(DELAY_BLINK);
    for(i=0; i<MAX_LED; i++){
      digitalWrite(arry_led[i], LOW);
    }
    delay(DELAY_BLINK);
  }
}
