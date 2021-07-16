#include "global.h"

typedef struct
{
    unsigned char state;
    unsigned char direction;
} valType;

valType val;

enum{
    S_STOP_ = 0x00,
    S_READY_,
    S_RUN_,
    S_DIR_CHECK_    
};

void setupMain() 
{
    unsigned char i;
    /*시리얼 초기화*/
    Serial.begin(9600);
    /*변수초기화*/
    memset(&val, 0x00, sizeof(val));
    /*장치 초기화*/
    servoInit(); //서보모터
    newPingInit(); //거리측정센서
    buttonInit(); //시작 버튼
    val.state = S_STOP_;
}

void loopMain()
{
    //Button
    if (changeBtnState())
    {
        if (val.state == S_RUN_)
        {
            val.state = S_STOP_;
            // Serial.println("off!!");
        }else{
            val.state = S_RUN_;
            // Serial.println("on!!");
        }
    }

    switch(val.state)
    {
        case S_STOP_:
        {
            moveStop();
            val.state = S_READY_;
            // break;
        }
        case S_READY_:
        {
            // getDistance();
            break;
        }
        case S_RUN_:
        {
            if (getDistance() < 50)
            {
                val.state = S_DIR_CHECK_;
            }else
            {
                moveForward();
            }
            break;
        }
        case S_DIR_CHECK_:
        {
            int dLeft,dRight;
            moveStopAndBack();
            //left
            servoRun(dir_left);
            dLeft = getDistance();
            //right
            servoRun(dir_right);
            dRight = getDistance();
            //front
            servoRun(dir_front);
            //moving
            if (dLeft < 80 && dRight < 80)
            {
                turnRightBack();
            }
            else if (dLeft >= dRight)
            {
                turnLeft();
            }
            else
            {
                turnRight();
            }
            val.state = S_RUN_;
            break;
        }
    }    
}