#include <SoftwareSerial.h> 
SoftwareSerial BTSerial(A2, A3); //bluetooth module Tx:A2 Rx:A3 
void setup() { 
  Serial.begin(9600); 
  BTSerial.begin(9600); 
} 
void loop() {
  if (BTSerial.available()){
    Serial.write(BTSerial.read());
  }
  if (Serial.available()){ 
    BTSerial.write(Serial.read()); 
  }
}
