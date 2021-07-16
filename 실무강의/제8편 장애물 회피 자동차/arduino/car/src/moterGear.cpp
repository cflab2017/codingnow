#include "moterGear.h"
#include <AFMotor.h>
//AFMotor Library https://learn.adafruit.com/adafruit-motor-shield/library-install //

AF_DCMotor motor1(1, MOTOR12_1KHZ);
AF_DCMotor motor2(2, MOTOR12_1KHZ);
AF_DCMotor motor3(3, MOTOR34_1KHZ);
AF_DCMotor motor4(4, MOTOR34_1KHZ);

#define MAX_SPEED 80//190 // sets speed of DC  motors
bool goesForward = 0;

void setSpeed(void)
{
    int speed;
    for (speed = 0; speed < MAX_SPEED; speed += 2)
    {
        motor1.setSpeed(speed);
        motor2.setSpeed(speed);
        motor3.setSpeed(speed);
        motor4.setSpeed(speed);
        delay(10);
    }
}

void moveForward(void)
{

    if (!goesForward)
    {
        goesForward = true;
        motor1.run(FORWARD);
        motor2.run(FORWARD);
        motor3.run(FORWARD);
        motor4.run(FORWARD);
        setSpeed();
    }
}

void moveBackward(void)
{
    goesForward = false;
    motor1.run(BACKWARD);
    motor2.run(BACKWARD);
    motor3.run(BACKWARD);
    motor4.run(BACKWARD);
    setSpeed();
    delay(300);
    moveStop();
}

void turnRight(void)
{
    motor1.run(FORWARD);
    motor2.run(FORWARD);
    motor3.run(BACKWARD);
    motor4.run(BACKWARD);
    setSpeed();
    delay(800);
    moveStop();
}
void turnLeft(void)
{
    motor1.run(BACKWARD);
    motor2.run(BACKWARD);
    motor3.run(FORWARD);
    motor4.run(FORWARD);
    setSpeed();
    delay(800);
    moveStop();
}

void turnRightBack(void)
{
    motor1.run(FORWARD);
    motor2.run(FORWARD);
    motor3.run(BACKWARD);
    motor4.run(BACKWARD);
    setSpeed();
    delay(1000);
    moveStop();
}

void moveStop(void)
{
    motor1.run(RELEASE);
    motor2.run(RELEASE);
    motor3.run(RELEASE);
    motor4.run(RELEASE);
    goesForward = false;
}

void moveStopAndBack(void)
{
    moveStop();
    moveBackward();
}
