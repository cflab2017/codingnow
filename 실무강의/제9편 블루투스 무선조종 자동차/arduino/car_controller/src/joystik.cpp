#include "joystik.h"

#define KEY_MAX 6
unsigned char keyMap[KEY_MAX] = {
    A0, A1, /*6,*/ 3, 5, 2, 4};

unsigned char keyResultPre = 0;

void joystickInit(void)
{
    unsigned char i;
    for (i = 0; i < KEY_MAX; i++) //포트 초기화
    {
        if (keyMap[i] >= A0)
            pinMode(keyMap[i], INPUT); //Analog
        else
            pinMode(keyMap[i], INPUT_PULLUP);
    }
}

unsigned char joystickGetkey(void)
{
    unsigned char i;
    unsigned char keyResult = 0;
    unsigned int adc;
#if 1
    adc = analogRead(keyMap[0]);
    if (adc > 530)        keyResult |= (0x01 << 0); //left
    if (adc < 500)        keyResult |= (0x01 << 1); //right

    adc = analogRead(keyMap[1]);
    if (adc > 530)        keyResult = (0x01 << 2); //up
    if (adc < 500)        keyResult = (0x01 << 3); //down

    keyResult |= ((~digitalRead(keyMap[2])) & 0x01) << 4;
    keyResult |= ((~digitalRead(keyMap[3])) & 0x01) << 5;
    keyResult |= ((~digitalRead(keyMap[4])) & 0x01) << 6;
    keyResult |= ((~digitalRead(keyMap[5])) & 0x01) << 7;
#else
    unsigned char count = 0;
    for (i = 0; i < KEY_MAX; i++)
    {
        if (keyMap[i] >= A0) //아날로그  pin read
        {
            adc = analogRead(keyMap[i]);
            if (adc > 530) keyResult |= (0x01 << count); //left, up
            count++;
            if (adc < 500) keyResult |= (0x01 << (count)); //right, down
        }else
        { //digital pin read
            keyResult |= ((~digitalRead(keyMap[i])) & 0x01) << count;
        }
        count++;
    }
#endif
#if 0//for debugging
    if (keyResult != keyResultPre)
    {
        Debug.print(DBG_INFO, "keyResult : %02X", keyResult);
        keyResultPre = keyResult;
    }
#endif
    return keyResult;
}