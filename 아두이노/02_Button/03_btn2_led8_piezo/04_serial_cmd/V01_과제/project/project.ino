
#define MAX_LED 8
unsigned char arry_led[MAX_LED] = {
  2, 3, 4, 5, 6, 7, 8, 9
};

void setup() {
  int i;
  Serial.begin(9600);

  for (i = 0; i < MAX_LED; i++) {
    pinMode(arry_led[i], OUTPUT);
  }
}

void loop() {
  if (Serial.available()) {
    String inString = Serial.readStringUntil('\n');
    
    if (inString.indexOf("on") > -1) {
      inString.replace("on", "");
      Serial.println(inString);

      int i;
      for (i = 0; i < inString.length(); i++) {
        if (inString.charAt(i) == '1') {
          digitalWrite(arry_led[i], HIGH);
        }
        if (inString.charAt(i) == '0') {
          digitalWrite(arry_led[i], LOW);
        }
      }
    }
  }
}
