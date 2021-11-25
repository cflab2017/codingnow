#include "global.h"

#define level_danger 1.7
#define level_warning 1.6

void setupMain() 
{
    /*시리얼 초기화*/
    Serial.begin(9600);
    /*장치 초기화*/
    init_buzzer();
    init_led();
}

void loopMain()
{
    float value = get_ppm();//일산화 탄소 값을 가져온다.

    led_blinking();
    if (value > level_danger)      //위험 값?
    {
        play_buzzer();
    }
    else if (value > level_warning)//주의 값?
    {
        ;
    }
    else                           //이상없음.
    {
        delay(400);
    }
    delay(100);

    // play_buzzer();
    // delay(1000);
}