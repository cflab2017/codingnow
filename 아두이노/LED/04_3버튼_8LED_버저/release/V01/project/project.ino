
#define BUTTON_0 10
#define BUTTON_1 11
#define BUTTON_2 12
/*GND -- 10Kohm -- A1 -- btn, VDD(5V)*/

#define MAX_LED 8
unsigned char arry_led[MAX_LED] = {
2,3,4,5,6,7,8,9
};
/*GND -- LED -- 250ohm -- PIN*/

#define DELAY_CYCLE 100

void led_right(void){
  int i;
  for(i=0; i<MAX_LED; i++){
    digitalWrite(arry_led[i], HIGH);
    delay(DELAY_CYCLE);
  }

  for(i=0; i<MAX_LED; i++){
    digitalWrite(arry_led[i], LOW);
    delay(DELAY_CYCLE);
  }
}

void led_left(void){
  int i;
  for(i=MAX_LED-1; i>=0; i--){
    digitalWrite(arry_led[i], HIGH);
    delay(DELAY_CYCLE);
  }

  for(i=MAX_LED-1; i>=0; i--){
    digitalWrite(arry_led[i], LOW);
    delay(DELAY_CYCLE);
  }
}

void led_all_blink(void){
  int i;
  for(i=0; i<MAX_LED; i++){
    if(i%2 == 0)
    {
      digitalWrite(arry_led[i], HIGH);
    }
  }
  delay(DELAY_CYCLE);
  for(i=0; i<MAX_LED; i++)
  {
    if (i % 2 == 0)
    {
      digitalWrite(arry_led[i], LOW);
    }
  }
  delay(DELAY_CYCLE);
}

void setup() {
  int i;
  Serial.begin(9600);

  //button 초기화
  pinMode(BUTTON_0, INPUT);
  pinMode(BUTTON_1, INPUT);
  pinMode(BUTTON_2, INPUT);

  for(i=0; i<MAX_LED; i++){
    pinMode(arry_led[i], OUTPUT);
  }
}

void loop() {
  //button 상태
  int btn_0 = digitalRead(BUTTON_0);
  int btn_1 = digitalRead(BUTTON_1);
  int btn_2 = digitalRead(BUTTON_2);

  Serial.print("btn_0 : "+String(btn_0)+",");
  Serial.print("btn_1 : "+String(btn_1)+",");
  Serial.print("btn_2 : "+String(btn_2)+",");
  Serial.println();

  // if(btn_0){    
  //   led_right();
  // }

  // if(btn_1){    
  //   led_all_blink();
  // }

  // if(btn_2){  
  //   led_left();  
  // }
}
