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
  delay(100);
  digitalWrite(LED_02, HIGH);
  delay(100);
  digitalWrite(LED_03, HIGH);
  delay(100);
  digitalWrite(LED_04, HIGH);
  delay(100);
  digitalWrite(LED_05, HIGH);
  delay(100);
  digitalWrite(LED_06, HIGH);
  delay(100);
  digitalWrite(LED_07, HIGH);
  delay(100);
  digitalWrite(LED_08, HIGH);
  delay(100);

  digitalWrite(LED_01, LOW);
  delay(100);
  digitalWrite(LED_02, LOW);
  delay(100);
  digitalWrite(LED_03, LOW);
  delay(100);
  digitalWrite(LED_04, LOW);
  delay(100);
  digitalWrite(LED_05, LOW);
  delay(100);
  digitalWrite(LED_06, LOW);
  delay(100);
  digitalWrite(LED_07, LOW);
  delay(100);
  digitalWrite(LED_08, LOW);
  delay(100);
}
