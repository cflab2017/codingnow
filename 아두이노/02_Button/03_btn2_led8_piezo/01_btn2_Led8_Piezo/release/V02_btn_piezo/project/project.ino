// https://diyver.tistory.com/32

#define BUTTON_0 10
#define BUTTON_1 11

#define PIN_PIEZO 13
/*261 도, 294 레,330 미,349 파, 392 솔, 440 라, 494 시, 523 도 */

void setup() {
  int i;
  Serial.begin(9600);
  //button 초기화
  pinMode(BUTTON_0, INPUT_PULLUP);
  pinMode(BUTTON_1, INPUT_PULLUP);
  pinMode(PIN_PIEZO, OUTPUT);
}

void loop() {
  int i;
  //button 상태
  int btn_0 = digitalRead(BUTTON_0);
  int btn_1 = digitalRead(BUTTON_1);

  if(!btn_0){
    Serial.println("press btn_0");
    tone(PIN_PIEZO,261);
    delay(200);
    noTone(PIN_PIEZO); 
  }
  if(!btn_1){
    Serial.println("press btn_1");
    tone(PIN_PIEZO,392);
    delay(200);
    noTone(PIN_PIEZO); 
  }
}
