#include "bluetooth.h"

#include <SoftwareSerial.h>

SoftwareSerial bluetooth(A2, A3);
String str = "";

void bluetoothInit(void)
{
    bluetooth.begin(9600);
}

unsigned char bluetoothProcess(void)
{
    unsigned char key = 0x00;
    while (bluetooth.available())
    {
        str += (char)bluetooth.read();
        if (str.indexOf('\n') > -1)
        {
            str.replace("\n", ""); //enter 삭제
            str.replace(" ", "");  //space 삭제
            str.toUpperCase();     //대문자변환
            // Serial.print("str 1 : ");
            // Serial.println(str);
            if (str.indexOf("KEY=") > -1)
            {
                str.replace("KEY=", ""); //key= 삭제
                // Serial.print("str 2 : ");
                // Serial.println(str);
                if (str.length() == 2)
                {
                    char charBuf[3];
                    str.toCharArray(charBuf,3);
                    key = strtoul(charBuf, NULL, 16);
                    return key;
                }
            }
            str = "";
        }
    }
    return key;
}