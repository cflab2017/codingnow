#include "global.h"

#define KEY_MAX 6
unsigned char keyMap[KEY_MAX] = {
A0, A1, /*6,*/ 3, 5, 2, 4
};

typedef struct{
  unsigned char key;
  unsigned char keyPre;
  unsigned char keyResult[KEY_MAX + 2];
}KeyValtype;
KeyValtype val;

void getKey()
{
    // int adc1, adc2, key1,key2, key3, key4;
    // adc1 = analogRead(keyMap[0]);
    // adc2 = analogRead(keyMap[1]);
    // Serial.print(adc1);
    // Serial.print(",");
    // Serial.print(adc2);

    // key1 = digitalRead(keyMap[2]);
    // key2 = digitalRead(keyMap[3]);
    // key3 = digitalRead(keyMap[4]);
    // key4 = digitalRead(keyMap[5]);
    // Serial.print(key1);
    // Serial.print(",");
    // Serial.print(key2);
    // Serial.print(",");
    // Serial.print(key3);
    // Serial.print(",");
    // Serial.println(key4);

    unsigned char i, count = 0;
    unsigned int adc;
    memset(val.keyResult, 0x00, sizeof(val.keyResult));
    for (i = 0; i < KEY_MAX; i++)
    {
        if (keyMap[i] >= A0)//아날로그  pin read
        {
            adc = analogRead(keyMap[i]);
            if (adc > 530)
            {
                val.keyResult[count] = 1; //left, up
            }else if(adc < 500)
            {
                val.keyResult[count + 1] = 1; //right, down
            }
            count++;
        }else{//digital pin read
            val.keyResult[count] = (~digitalRead(keyMap[i])) & 0x01;
        }
        count++;
    }
}

void keyProcess(void)
{
    unsigned char i,key = 0x00;
    for (i = 0; i < sizeof(val.keyResult); i++)
    {
        key |= (val.keyResult[i] << i);
    }
    val.key = key;
}

void sendMsg()
{
    char buf[64];
    // unsigned char i,cnt=0;
    // for(i=0; i<sizeof(val.keyResult);i++)
    // {
    //     sprintf(&buf[cnt], "%02X,", val.keyResult[i]);
    //     cnt += 3;
    // }
    // sprintf(buf, "%02X,%02X,%02X,%02X,%02X,%02X,%02X"
    //             , val.keyResult[0], val.keyResult[1]
    //             , val.keyResult[2], val.keyResult[3]
    //             , val.keyResult[4], val.keyResult[5], 
    //             val.keyResult[6]);

    if (val.key == val.keyPre)
        return;
    val.keyPre = val.key;
    sprintf(buf, "key=%02X", val.key);
    Serial.println(buf);
}

void setupMain() 
{
    unsigned char i;
    Serial.begin(9600);//시리얼 초기화
    memset(&val, 0x00, sizeof(val));//변수 초기화
    for (i = 0; i < KEY_MAX; i++) //포트 초기화
    {
        if(keyMap[i] >= A0)
        {
            pinMode(keyMap[i], INPUT);//Analog
        }else{
            pinMode(keyMap[i], INPUT_PULLUP);
        }
    }
}

void loopMain() 
{
    getKey();//key값을 read 한다.
    keyProcess();//key값을 원하는 형태로 변환한다.
    sendMsg();//시리얼 데이타를 전송한다.
}