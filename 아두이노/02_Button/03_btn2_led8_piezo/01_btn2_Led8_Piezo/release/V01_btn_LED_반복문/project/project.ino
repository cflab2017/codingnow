
#define BUTTON_0 10
#define BUTTON_1 11
/*GND -- 10Kohm -- A1 -- btn, VDD(5V)*/

#define MAX_LED 8
unsigned char arry_led[MAX_LED] = {
2,3,4,5,6,7,8,9
};
/*GND -- LED -- 250ohm -- PIN*/

#define DELAY_CYCLE 50

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
  pinMode(BUTTON_0, INPUT_PULLUP);
  pinMode(BUTTON_1, INPUT_PULLUP);

  for(i=0; i<MAX_LED; i++){
    pinMode(arry_led[i], OUTPUT);
  }
}

void loop() {
  //button 상태
  int btn_0 = digitalRead(BUTTON_0);
  int btn_1 = digitalRead(BUTTON_1);

  if(!btn_0 && !btn_1){
    Serial.println("press btn_0 & btn_1");
    led_all_blink();
  }else if(!btn_0){    
    Serial.println("press btn_0");
    led_right();
  }else if(!btn_1){    
    Serial.println("press btn_1");
    led_left();  
  }else{
    ;
  }
}
