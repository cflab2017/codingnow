#include "global.h"

typedef struct
{
    unsigned char direction;
} valType;

valType val;

void setupMain() 
{
    unsigned char i;
    /*시리얼 초기화*/
    Serial.begin(9600);
    /*변수초기화*/
    memset(&val, 0x00, sizeof(val));
    /*장치 초기화*/
    newPingInit(); //거리측정센서
}

void loopMain()
{
    val.direction = getDistance();
    Debug.print(DBG_INFO, "value : %d", val.direction);
    delay(20);
}