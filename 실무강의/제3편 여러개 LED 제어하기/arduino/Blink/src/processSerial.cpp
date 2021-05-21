
#include "processSerial.h"
/* String Data Types
https://www.arduino.cc/reference/ko/language/variables/data-types/stringobject/
*/
String str = "";

unsigned char AsciiToHex(unsigned char val)
{
  if(val >= '0' && val <= '9')
  {
    return val-'0';
  }
  if(val >= 'A' && val <= 'F')
  {
    return (val-'A')+10;
  }
  return 0;
}
unsigned char strToHex(String val)
{
  unsigned char ret = 0;
  ret = AsciiToHex(val[0]) << 4;
  ret += AsciiToHex(val[1]);
  return ret;
}

unsigned char serialGet(void) 
{
  unsigned char cmd = 0xFF;
  while (Serial.available()) 
  {
    str += (char)Serial.read();
    if (str.indexOf('\n') > -1 )
    {
      str.replace("\n","");//enter 삭제
      str.replace(" ","");//space 삭제
      str.toUpperCase();//대문자변환
      if(str.indexOf("LED")>-1)
      {
        str.replace("LED","");//LED 삭제
        if(str.length()==2)
        {
          cmd = strToHex(str);
          // Serial.print(cmd);
        }
      }
      str = "";
    }
  }
  return cmd;
}
