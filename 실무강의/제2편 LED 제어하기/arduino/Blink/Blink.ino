#include "src/global.h"
#include <SimpleTimer.h>

unsigned char isToggle = 0;
unsigned char isBlinking = 0;

SimpleTimer timer;

void sTimerCallback()
{
  isToggle = ~isToggle;
  Serial.print("LED : ");
  Serial.println(digitalRead(LED_BUILTIN));
}

void setup() 
{
  Serial.begin(9600);
  pinMode(LED_BUILTIN, OUTPUT);
  // digitalWrite(LED_BUILTIN, LOW);
  timer.setInterval(1000, sTimerCallback);
}

void loop() 
{
  timer.run();
  switch (serialGet())
  {
    case 1: //ON
      digitalWrite(LED_BUILTIN, HIGH);
      Serial.println("LED ON");
      isBlinking = 0;
      break;
    case 2: //OFF
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("LED OFF");
      isBlinking = 0;
      break;
    case 3: //Blinking
      digitalWrite(LED_BUILTIN, LOW);
      Serial.println("LED Blinking");
      isBlinking = 1;
      break;
  }

  if (isBlinking)
  {
    if (isToggle){
      digitalWrite(LED_BUILTIN, HIGH);
    }else{
      digitalWrite(LED_BUILTIN, LOW);
    }
  }
}
