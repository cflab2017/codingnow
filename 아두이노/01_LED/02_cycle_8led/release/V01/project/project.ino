#define LED_01 2
#define LED_02 3
#define LED_03 4
#define LED_04 5
#define LED_05 6
#define LED_06 7
#define LED_07 8
#define LED_08 9
/*GND -- LED -- 220ohm -- PIN*/

void setup() {
  pinMode(LED_01, OUTPUT);
  pinMode(LED_02, OUTPUT);
  pinMode(LED_03, OUTPUT);
  pinMode(LED_04, OUTPUT);
  pinMode(LED_05, OUTPUT);
  pinMode(LED_06, OUTPUT);
  pinMode(LED_07, OUTPUT);
  pinMode(LED_08, OUTPUT);
}

void loop() {
  digitalWrite(LED_01, HIGH);
  digitalWrite(LED_02, HIGH);
  digitalWrite(LED_03, HIGH);
  digitalWrite(LED_04, HIGH);
  digitalWrite(LED_05, HIGH);
  digitalWrite(LED_06, HIGH);
  digitalWrite(LED_07, HIGH);
  digitalWrite(LED_08, HIGH);
  delay(500);

  digitalWrite(LED_01, LOW);
  digitalWrite(LED_02, LOW);
  digitalWrite(LED_03, LOW);
  digitalWrite(LED_04, LOW);
  digitalWrite(LED_05, LOW);
  digitalWrite(LED_06, LOW);
  digitalWrite(LED_07, LOW);
  digitalWrite(LED_08, LOW);
  delay(500);
}
