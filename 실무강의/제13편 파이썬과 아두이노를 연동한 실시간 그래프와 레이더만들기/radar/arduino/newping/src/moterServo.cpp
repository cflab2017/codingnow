#include "moterServo.h"

#include <Servo.h>
//Servo Library https://github.com/arduino-libraries/Servo.git //

#define front_degree 120
#define left_degree (front_degree + 50)
#define right_degree (front_degree - 50)

int servoPin = 9;
int angle = 0;
Servo servo;

void servoInit(void)
{
    servo.attach(servoPin);
    delay(100);
    servo.write(0);
    delay(100);
    servo.write(angle);
}

void servoMoving(int target)
{
    char offset = 1;
    if (angle > target){
        offset = -1;
    }

    while(angle != target)
    {
        angle += offset;
        servo.write(angle);
        delay(10);
    }
}

void servoRun(unsigned char key)
{
    unsigned char i;

    if (key & dir_left)
    {
        servoMoving(left_degree);
    }

    if (key & dir_right)
    {
        servoMoving(right_degree);
    }

    if (key & dir_front)
    {
        servoMoving(front_degree);
    }
    delay(100);
}