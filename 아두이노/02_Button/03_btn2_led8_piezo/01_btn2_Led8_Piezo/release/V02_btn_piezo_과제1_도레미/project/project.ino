// https://diyver.tistory.com/32

#define BUTTON_0 10
#define BUTTON_1 11
/*GND -- 10Kohm -- A1 -- btn, VDD(5V)*/

#define PIN_PIEZO 13
#define TONES_MAX 8
int Tones[TONES_MAX] = {261, 294, 330, 349, 392, 440, 494, 523}; // 도, 레, 미, 파, 솔, 라, 시, 도

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
    for(i = 0; i<TONES_MAX; i++)
    {
      tone(PIN_PIEZO,Tones[i]);
      delay(200);
    }
    noTone(PIN_PIEZO); 
  }else if(!btn_1){
    Serial.println("press btn_1");
    for(i = TONES_MAX-1; i >= 0; i--)
    {
      tone(PIN_PIEZO,Tones[i]);
      delay(200);
    }
    noTone(PIN_PIEZO); 
  }else{
    ;
  }
}
