#include "global.h"

typedef struct
{
    unsigned char direction;
    unsigned char key;
    unsigned char keyCurr;
    int distance;
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
    // servoInit(); //서보모터
    newPingInit(); //거리측정센서
    buttonInit();  //시작 버튼
    bluetoothInit();
}

void loopMain()
{
    val.keyCurr = bluetoothProcess();
    if (val.keyCurr)
    {
        val.key = val.keyCurr;
        Serial.print("direction : ");
        Serial.println(String(val.key, 16));

        if (val.key & dir_left)     turnLeft();
        if (val.key & dir_right)    turnRight();
        if (val.key & dir_front)    moveForward();
        if (val.key & dir_back)     moveBackward();
        if (val.key & dir_stop)     moveStop();
    }

    if (val.key & dir_front)
    {
        val.distance = getDistance();
        Debug.print(DBG_INFO, "distance : %d", val.distance);
    }else{
        val.distance = 250;
    }

    if ((val.distance < 50) || changeBtnState())
    {
        val.key  = dir_stop;
        moveStop();
    }
}