#include "global.h"

typedef struct
{
    unsigned char keyCur;
    unsigned char keyPre;
} valType;

valType val;

void setupMain() 
{
    /*시리얼 초기화*/
    Serial.begin(9600);
    /*변수초기화*/
    memset(&val, 0x00, sizeof(val));
    /*장치 초기화*/
    joystickInit();
}

void loopMain()
{
    val.keyCur = joystickGetkey();
    if (val.keyCur != val.keyPre)
    {
        sendToBluetooth(val.keyCur);
        val.keyPre = val.keyCur;
    }
}