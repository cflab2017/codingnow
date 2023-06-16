
#define LED_RED 13
#define LED_GREEN 12
#define LED_YELLO 11
/*GND -- LED -- 250ohm -- PIN*/

#define BUTTON_0 A1
#define BUTTON_1 A2
#define BUTTON_2 A3
/*GND -- 10Kohm -- A1 -- btn, VDD(5V)*/

#define MAX_LED 8
unsigned char arry_led[MAX_LED] = {
2,3,4,5,6,7,8,9
};

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
  //LED 초기화
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_YELLO, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);

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

  if(btn_0){    
    digitalWrite(LED_RED, HIGH); 
    led_right();
  }else{
    digitalWrite(LED_RED, LOW);  
  }

  if(btn_1){    
    digitalWrite(LED_GREEN, HIGH); 
    led_all_blink();
  }else{
    digitalWrite(LED_GREEN, LOW);  
  }

  if(btn_2){  
    digitalWrite(LED_YELLO, HIGH); 
    led_left();  
  }else{
    digitalWrite(LED_YELLO, LOW);  
  }
}
