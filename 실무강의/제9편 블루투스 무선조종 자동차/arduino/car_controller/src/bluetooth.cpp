#include "bluetooth.h"

unsigned char sendKey = 0x00;

void sendToBluetooth(unsigned char key)
{
    char buf[10];
    sprintf(buf,"key=%02X\n",key);
    Serial.print(buf);
}