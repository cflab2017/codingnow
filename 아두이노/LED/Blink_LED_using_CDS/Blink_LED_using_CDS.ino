
#define LED_RED 8
#define LED_YELLO 9
#define LED_GREEN 10
/*GND -- LED -- 250ohm -- PIN*/

#define PIN_CDS A0 
/*GND -- 10Kohm -- A0 -- CDS -- VDD(5V)*/

// the setup function runs once when you press reset or power the board
void setup() {
  Serial.begin(9600);
  // initialize digital pin LED_BUILTIN as an output.
  pinMode(LED_BUILTIN, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_YELLO, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
  pinMode(PIN_CDS, INPUT);
}

// the loop function runs over and over again forever
void loop() {
  int cds = analogRead(A0); // A0로 받은 아날로그 값을 cds변수로 넘겨줍니다.
  Serial.println(cds); // Serial 모니터에 cds 값을 찍어주고 한줄 내려줍니다.

  digitalWrite(LED_BUILTIN, HIGH);  // turn the LED on (HIGH is the voltage level)
  if(cds < 500){
    digitalWrite(LED_RED, HIGH);  // turn the LED on (HIGH is the voltage level)
    digitalWrite(LED_YELLO, HIGH);  // turn the LED on (HIGH is the voltage level)
    digitalWrite(LED_GREEN, HIGH);  // turn the LED on (HIGH is the voltage level)
    delay(500);                      // wait for a second
    digitalWrite(LED_RED, LOW);   // turn the LED off by making the voltage LOW
    digitalWrite(LED_YELLO, LOW);   // turn the LED off by making the voltage LOW
    digitalWrite(LED_GREEN, LOW);   // turn the LED off by making the voltage LOW
  }else{
    delay(500);                      // wait for a second
  }
  digitalWrite(LED_BUILTIN, LOW);   // turn the LED off by making the voltage LOW
  delay(500);                      // wait for a second
}
