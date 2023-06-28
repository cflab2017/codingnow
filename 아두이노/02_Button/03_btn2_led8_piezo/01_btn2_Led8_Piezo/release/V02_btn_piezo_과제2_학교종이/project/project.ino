// https://diyver.tistory.com/32

#define BUTTON_0 10
#define BUTTON_1 11
/*GND -- 10Kohm -- A1 -- btn, VDD(5V)*/

#define PIN_PIEZO 13
#define TONES_MAX 8
int Tones[TONES_MAX] = {261, 294, 330, 349, 392, 440, 494, 523}; // 도, 레, 미, 파, 솔, 라, 시, 도

int t_do1 = 261;
int t_re1 = 294;
int t_mi1 = 330;
int t_pa1 = 349;
int t_so1 = 392;
int t_ra1 = 440;
int t_si1 = 494;
int t_do2 = 523;
int t_dum = -1;

int play_00[] = {
  t_so1,t_so1,t_ra1,t_ra1,t_so1,t_so1,t_mi1,t_dum,
  t_so1,t_so1,t_mi1,t_mi1,t_re1,t_dum,
  t_so1,t_so1,t_ra1,t_ra1,t_so1,t_so1,t_mi1,t_dum,
  t_so1,t_mi1,t_re1,t_mi1,t_do1,t_dum,
};

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
  }
  if(!btn_1){

    for(i = 0; i < sizeof(play_00)/sizeof(int); i++)
    {
      tone(PIN_PIEZO,play_00[i]);
      delay(200);
      if(play_00[i+1] == t_dum){        
        delay(200);
        i++;
      }
      noTone(PIN_PIEZO); 
      delay(200);
    }
    noTone(PIN_PIEZO); 
  }
}
