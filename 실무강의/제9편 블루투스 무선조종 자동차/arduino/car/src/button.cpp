#include "button.h"

#define buttonPin 10
unsigned char btnPre = 1;
unsigned char btnDebounce = 0;

void buttonInit(void)
{
    pinMode(buttonPin, INPUT_PULLUP);
    btnPre = 1;
    delay(100);
}

bool changeBtnState(void)
{
    unsigned char btn;
    btn = digitalRead(buttonPin);

    if(btn == 0)
    {
        btnDebounce++;
        Debug.print(DBG_INFO, "button : %d,%d", btn, btnDebounce);
        if (btnDebounce < 5)
            return false;
    }
    btnDebounce = 0;

    if (btn == 0 && btn != btnPre)
    {
        btnPre = btn;
        return true;
    }
    btnPre = btn;
    return false;
}