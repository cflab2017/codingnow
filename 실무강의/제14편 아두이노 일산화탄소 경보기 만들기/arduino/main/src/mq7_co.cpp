#include "global.h"
#include "MQ7.h"
//https://github.com/swatish17/MQ7-Library

MQ7 mq7(A5, 5.0); //MQ7 아날로그 포트 A5 지정

#define AVR_MAX 10 //average filter

float get_ppm(void)
{
    float value = 0;

    for(int i=0; i<AVR_MAX; i++){
        value += mq7.getPPM();
        delayMicroseconds(100);
    }

    value = value/AVR_MAX;

    Serial.print("CO: ");
    Serial.print(value); 
    Serial.println(" ppm");
    return value;
}