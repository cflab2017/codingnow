#include "moterServo.h"

#include <Servo.h>

int servoPin = 7;
int angle = 90;
Servo servo;

void servoInit(void)
{
    servo.attach(servoPin);
    delay(100);
    servo.write(0);
    delay(100);
    servo.write(angle);
}

void servoRun(unsigned char key)
{
    if (key & dir_up)
    {
        if (angle < 180)
        {
            angle += 10;
        }else{
            angle = 180;
        }
        servo.write(angle);
    }

    if (key & dir_down)
    {
        if (angle > 0)
        {
            angle -= 10;
        }
        else
        {
            angle = 0;
        }
        servo.write(angle);
    }
}