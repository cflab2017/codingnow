
#define MAX_LED 8
unsigned char arry_led[MAX_LED] = {
2,3,4,5,6,7,8,9
};

void setup() {
  int i;
  Serial.begin(9600);

  for(i=0; i<MAX_LED; i++){
    pinMode(arry_led[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available()) {
    String inString = Serial.readStringUntil('\n');
    Serial.println(inString);
    if (inString== "on0") {
      digitalWrite(arry_led[0], HIGH);
    }
    if (inString== "off0") {
      digitalWrite(arry_led[0], LOW);
    }
  }
}
