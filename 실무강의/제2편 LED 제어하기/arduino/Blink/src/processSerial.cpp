
#include "processSerial.h"
/* String Data Types
https://www.arduino.cc/reference/ko/language/variables/data-types/stringobject/
*/
String str = "";

unsigned char searchCMD(String str)
{
  if (str == "ON"){return 1;}
  if (str == "OFF"){return 2;}
  if (str == "BLINKING"){return 3;}
  return 0;
}

unsigned char serialGet(void) 
{
  unsigned char cmd = 0;
  while (Serial.available()) 
  {
    str += (char)Serial.read();
    if (str.indexOf('\n') > -1 )
    {
      // Serial.println(str);
      str.toUpperCase();//대문자변환
      str.replace("\n","");//enter 삭제
      cmd = searchCMD(str);
      str = "";
    }
  }
  return cmd;
}
