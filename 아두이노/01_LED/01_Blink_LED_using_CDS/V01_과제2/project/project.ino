#define LED_RED 8
#define LED_YELLO 9
#define LED_GREEN 10

void setup() {
  pinMode(LED_RED, OUTPUT);
  pinMode(LED_YELLO, OUTPUT);
  pinMode(LED_GREEN, OUTPUT);
}

void loop() {
  digitalWrite(LED_RED, HIGH);
  delay(500);                   
  digitalWrite(LED_RED, LOW);   
  delay(500);      
  digitalWrite(LED_YELLO, HIGH);
  delay(500);       
  digitalWrite(LED_YELLO, LOW); 
  delay(500);     
  digitalWrite(LED_GREEN, HIGH);
  delay(500);      
  digitalWrite(LED_GREEN, LOW); 
  delay(500);                   
}