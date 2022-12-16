#include "global.h"

#define key_left_right A0
#define key_up_down A1
#define key_enter 3

typedef struct{
  unsigned char key;
  unsigned char keyPre;
}KeyValtype;
KeyValtype val;

void setupMain()
{
  unsigned char i;
  Serial.begin(9600);              // 시리얼 초기화
  memset(&val, 0x00, sizeof(val)); // 변수 초기화
  pinMode(key_left_right, INPUT);  // Analog
  pinMode(key_up_down, INPUT);     // Analog
  pinMode(key_enter, INPUT_PULLUP);
}

unsigned char get_direction(unsigned char port)
{
    unsigned int adc;
    adc = analogRead(port);
    //Serial.println(adc);
    if (adc > 1000){return 1;} // left, up
    if (adc < 10){return 2;} // right, down
    return 0;
}

unsigned char get_switch(unsigned char port)
{
    unsigned char val;
    val = (~digitalRead(port)) & 0x01;  // on, off
    return val;
}

void keyProcess(void)
{
    unsigned char key = 0x00;
    key |= (get_direction(key_left_right)<<0);
    key |= (get_direction(key_up_down)<<2);

    if ((val.keyPre & 0x0F) && (key&0x0F))//이전 값이 없을때만
    {
        key = (val.keyPre & 0x0F);
    }

    key |= (get_switch(key_enter)<<4);
    val.key = key;
}

void sendMsg()
{
    char buf[64];
    if (val.key == val.keyPre)
        return;
    val.keyPre = val.key;
    sprintf(buf, "key=%02X", val.key);
    Serial.println(buf);
}

void loopMain() 
{
    keyProcess();//key값을 처리한다.
    sendMsg();//시리얼 데이타를 전송한다.
}