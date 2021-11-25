#include "global.h"
#include "led.h"

#define pin_led 3
unsigned char led_toggle = 0;

void init_led(void)
{
    pinMode(pin_led,OUTPUT);
    digitalWrite(pin_led, LOW);
}

void led_blinking(void)
{
    if(led_toggle){
        led_toggle = 0;
        digitalWrite(pin_led,LOW);
    }else{
        led_toggle = 1;
        digitalWrite(pin_led, HIGH);
    }
}