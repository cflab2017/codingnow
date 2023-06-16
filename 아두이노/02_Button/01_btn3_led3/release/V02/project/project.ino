
#define LED_RED 13
#define LED_GREEN 12
#define LED_YELLO 11
/*GND -- LED -- 250ohm -- PIN*/

#define BUTTON_0 A1
#define BUTTON_1 A2
#define BUTTON_2 A3
/*GND -- 10Kohm -- A1 -- btn, VDD(5V)*/

void setup() {
  Serial.begin(9600);
  //LED 초기화
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_YELLO, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);

  //button 초기화
  pinMode(BUTTON_0, INPUT);
  pinMode(BUTTON_1, INPUT);
  pinMode(BUTTON_2, INPUT);
}

void loop() {
  int i;
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
    delay(100);
    digitalWrite(LED_RED, LOW);  
    delay(100);
  }else{
    digitalWrite(LED_RED, LOW);  
  }

  if(btn_1){    
    digitalWrite(LED_GREEN, HIGH);
    delay(100);
    digitalWrite(LED_GREEN, LOW);  
    delay(100);
  }else{
    digitalWrite(LED_GREEN, LOW);  
  }

  if(btn_2){    
    digitalWrite(LED_YELLO, HIGH);
    delay(100);
    digitalWrite(LED_YELLO, LOW);  
    delay(100);
  }else{
    digitalWrite(LED_YELLO, LOW);  
  }
}
