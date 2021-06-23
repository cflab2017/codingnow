
#include <Stepper.h>
#include "moterStepper.h"

const int steps = 45; //2048;

Stepper myStepper(steps, 11, 9, 10, 8);

void stepperInit(void)
{
    myStepper.setSpeed(200); //RPM
}

void stepperRun(unsigned char key)
{
    if (key & dir_left){
        myStepper.step(45);
    }
    if (key & dir_right)
    {
        myStepper.step(-45);
    }
}