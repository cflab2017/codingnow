#define LED_RED 8
#define LED_YELLO 9
#define LED_GREEN 10

void setup() {
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_YELLO, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
}

// the loop function runs over and over again forever
void loop() {
  digitalWrite(LED_RED, HIGH);  // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED_YELLO, HIGH);  // turn the LED on (HIGH is the voltage level)
  digitalWrite(LED_GREEN, HIGH);  // turn the LED on (HIGH is the voltage level)
  delay(500);                      // wait for a second
  digitalWrite(LED_RED, LOW);   // turn the LED off by making the voltage LOW
  digitalWrite(LED_YELLO, LOW);   // turn the LED off by making the voltage LOW
  digitalWrite(LED_GREEN, LOW);   // turn the LED off by making the voltage LOW
  delay(500);                      // wait for a second
}