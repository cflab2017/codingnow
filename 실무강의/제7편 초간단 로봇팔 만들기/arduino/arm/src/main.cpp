#include "global.h"

typedef struct{
    unsigned char keyResult;

    unsigned long timeCurr;
    unsigned long timeDealy;
}valType;

valType val;

void setupMain() 
{
    unsigned char i;
    /*시리얼 초기화*/
    Serial.begin(9600);
    /*변수초기화*/
    memset(&val, 0x00, sizeof(val));
    /*포트 초기화*/
    key_Init();
    stepperInit();
    servoInit();

    /*주기 설정 처음은 1sec*/
    val.timeCurr = millis();
    val.timeDealy = 50;
}

void loopMain()
{
    /*50ms 주기로 slideProcess를 실행한다. */
    if ((millis() - val.timeCurr) > val.timeDealy)
    {
        val.timeCurr = millis();
        val.timeDealy = 50;

        val.keyResult = getKey();
        if(val.keyResult & (dir_left|dir_right))
        {
            stepperRun(val.keyResult);
        }
        if (val.keyResult & (dir_up | dir_down))
        {
            servoRun(val.keyResult);
        }
    }
}