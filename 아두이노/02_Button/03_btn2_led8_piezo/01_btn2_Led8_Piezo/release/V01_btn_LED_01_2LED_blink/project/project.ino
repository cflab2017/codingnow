#define LED_0 8
#define LED_1 4
/*GND -- LED -- 330ohm -- PIN*/

#define BUTTON_0 10
#define BUTTON_1 11
/*GND -- A1 -- btn, VDD(5V)*/

void setup() {
  Serial.begin(9600);
  //LED 초기화
  pinMode(LED_0, OUTPUT);
  pinMode(LED_1, OUTPUT);

  //button 초기화
  pinMode(BUTTON_0, INPUT_PULLUP);
  pinMode(BUTTON_1, INPUT_PULLUP);
}

void loop() {
  //button 상태
  int btn_0 = digitalRead(BUTTON_0);
  int btn_1 = digitalRead(BUTTON_1);

  if(btn_0==0){    
    Serial.println("press btn_0 : "+ String(btn_0));
    digitalWrite(LED_0, HIGH);
    delay(100);
    digitalWrite(LED_0, LOW);  
    delay(100);
  }else{
    digitalWrite(LED_0, LOW);  
  }

  if(btn_1==0){  
    Serial.println("press btn_1 : "+ String(btn_1));  
    digitalWrite(LED_1, HIGH);
    delay(100);
    digitalWrite(LED_1, LOW);  
    delay(100);
  }else{
    digitalWrite(LED_1, LOW);  
  }
}