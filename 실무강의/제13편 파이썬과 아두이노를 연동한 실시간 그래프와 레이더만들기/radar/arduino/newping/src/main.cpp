#include "global.h"

typedef struct
{
    unsigned char degree;
    unsigned char direction;
} valType;

valType val;

unsigned char degreeValues[]={
    0, 45, 90, 135, 90, 45,
};

void setupMain() 
{
    unsigned char i;
    /*시리얼 초기화*/
    Serial.begin(9600);
    /*변수초기화*/
    memset(&val, 0x00, sizeof(val));
    /*장치 초기화*/
    newPingInit(); //거리측정센서
    servoInit();
}

void loopMain()
{
    #if 0
    servoMoving(0);
    #else
    servoMoving(degreeValues[val.degree]);
    val.direction = getDistance();

    int deg = map(degreeValues[val.degree],0,180,0,32);
    Debug.print(DBG_INFO, "value : %d,%d", deg, val.direction);
    // delay(20);
    val.degree = (val.degree + 1) % sizeof(degreeValues);
    #endif
}