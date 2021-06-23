#ifndef global_en_
#define global_en_

// #include <Arduino_DebugUtils.h>

#include <inttypes.h>
#include <Arduino.h>

#include "main.h"
#include "moterStepper.h"
#include "key.h"
#include "moterServo.h"

enum
{
    dir_left = 0x01,
    dir_right = 0x02,
    dir_up = 0x04,
    dir_down = 0x08,
};


#endif