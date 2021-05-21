#include "global.h"

//https://www.arduino.cc/reference/ko/language/variables/data-types/stringobject/

#define MAX_LED_CNT 4
unsigned char LEDS[MAX_LED_CNT] = {13,12,11,10};

void responseLedState(unsigned char state)
{
    unsigned char i,led;
    String hex;
    //digitalRead가 안되는 경우가 있어서 state를 가지고 처리함.
    led = state;
    // led = 0x00;
    // for(i=0; i<MAX_LED_CNT; i++)
    // {
    //     if(digitalRead(LEDS[i]))
    //     {
    //         led |= 0x01 << i;
    //     }
    // }
    Serial.print("Arduino LED : ");
    hex = String((led>>4)&0x0F, HEX);
    hex += String(led&0x0F, HEX);
    Serial.println(hex);
}

void setupMain() 
{
    unsigned char i;
    Serial.begin(9600);
    for(i=0; i<MAX_LED_CNT; i++){
        pinMode(LEDS[i], OUTPUT);
    }
}

void loopMain() 
{
    unsigned char state = 0, i;
    state = serialGet();

    if (state != 0xFF)
    {
        for(i=0; i<MAX_LED_CNT; i++)
        {
            if (state & (0x01 << i))
            {
                digitalWrite(LEDS[i], HIGH);
            }else{
                digitalWrite(LEDS[i], LOW);
            }
        }
        responseLedState(state);
    }
}