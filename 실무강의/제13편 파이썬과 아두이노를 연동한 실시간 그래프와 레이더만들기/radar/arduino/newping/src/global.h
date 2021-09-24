#ifndef global_en_
#define global_en_

#include <Arduino_DebugUtils.h>

#include <inttypes.h>
#include <Arduino.h>

#include "main.h"
#include "sensorNewPing.h"
#include "moterServo.h"
enum
{
    dir_left = 0x01,
    dir_right = 0x02,
    dir_front = 0x04,
    dir_back = 0x08,
};

#endif