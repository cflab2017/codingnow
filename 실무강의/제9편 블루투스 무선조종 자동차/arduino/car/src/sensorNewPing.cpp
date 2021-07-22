#include "sensorNewPing.h"

#include <NewPing.h>
//NewPing Library https://github.com/livetronic/Arduino-NewPing//

#define TRIG_PIN A0
#define ECHO_PIN A1
#define MAX_DISTANCE 200

NewPing sonar(TRIG_PIN, ECHO_PIN, MAX_DISTANCE);

int distance = 100;

int readPing()
{
    delay(70);
    int cm = sonar.ping_cm();
    if (cm == 0)
    {
        cm = 250;
    }
    return cm;
}

void newPingInit(void)
{
    distance = readPing();
    delay(100);
    distance = readPing();
    delay(100);
    distance = readPing();
    delay(100);
    distance = readPing();
    delay(100);
    // Debug.print(DBG_INFO, "distance : %d", distance);
}

int getDistance(void)
{
    distance = readPing();
    // Debug.print(DBG_INFO, "distance : %d", distance);
    return distance;
}
