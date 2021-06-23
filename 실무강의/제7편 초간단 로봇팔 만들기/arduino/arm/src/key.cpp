#include "key.h"

#define KEY_MAX 2
unsigned char keyMap[KEY_MAX] = {A0, A1};

void key_Init(void)
{
    unsigned i;
    for(i=0; i<KEY_MAX; i++)
    {
        pinMode(keyMap[i], INPUT); //Analog
    }
}

unsigned char getKey(void)
{
    unsigned i, adc, count = 0;
    unsigned char keyResult = 0;

    for (i = 0; i < KEY_MAX; i++)
    {
        adc = analogRead(keyMap[i]);
        // // Debug.print(DBG_INFO, "adc %d:%d", i, adc);
        // Serial.print("adc ");
        // Serial.print(i);
        // Serial.print(" : ");
        // Serial.println(adc);
        if (adc > 700)
        {
            keyResult |= (0x01 << count); //left, up
        }
        else if (adc < 300)
        {
            keyResult |= (0x01 << (count+1));; //right, down
        }else{
            ;
        }
        count+=2;
    }
    // Serial.println(keyResult);
    return keyResult;
}