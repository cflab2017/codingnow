#define MAX_LED 8
unsigned char arry_led[MAX_LED] = {
2,3,4,5,6,7,8,9
};

void setup() {
  int i;
  for(i=0; i<MAX_LED; i++){
    pinMode(arry_led[i], OUTPUT);
  }
}

void loop() {
  int i;

  for(i=0; i<MAX_LED; i++){
    if(i%2==0){
      digitalWrite(arry_led[i], HIGH);
    }
  }
  delay(100);

  for(i=0; i<MAX_LED; i++){
    digitalWrite(arry_led[i], LOW);
  }
  delay(100);
}
