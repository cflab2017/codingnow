#include "global.h"
#include <MsTimer2.h>
/*
Arduino Uno Board 메인 컨트롤러 : Atmega328 
Atmega328를 3개의 타이머가 있고 PWM 출력 및 시간 관련 함수들을 제공
Timer0 - 8Bit : PWM 5/6핀, 시간 관련 함수 (delay(), millis() 등)
Timer1 - 16Bit : PWM 9/10핀 (외부 라이브러리 Servo.h 와 함께 사용 불가)
Timer2 - 8Bit : PWM 3/11핀 (외부 라이브러리 MsTimer2.h 와 함께 사용 불가)
*/

#define _SLIDE_EN

unsigned char ledMap[2][COLUMN_MAX] = {
    /*ROW*/ {A5, 3, 13, A2, 6, 12, 7, 10},
    /*COL*/ {2, 8, 9, A4, 11, A3, 4, 5},
};

#ifdef _SLIDE_EN
typedef struct{
    unsigned char buffer[ROW_MAX][4]; //ready data buffer
    unsigned char idex;
    unsigned char dir;
} slideValType;
#endif
typedef struct{
    unsigned char dispBuffer[ROW_MAX]; //display data buffer
    unsigned char currRow;

    unsigned char rxBuffer[ROW_MAX];   //serial data buffer

#ifdef _SLIDE_EN
    slideValType slide;
#endif
    unsigned long timeCurr;
    unsigned long timeDealy;
}valType;

valType val;

unsigned char const heart[ROW_MAX] = {
    0b00000000,//0x00
    0b01100110,//0x66
    0b10011001,//0x99
    0b10000001,//0x81
    0b10000001,//0x81
    0b01000010,//0x42
    0b00100100,//0x24
    0b00011000,//0x18
};

void Timer2Interrupt()
{
    unsigned char i, col;
    digitalWrite(ledMap[ROW][val.currRow], LOW); //row port 초기화
    val.currRow = (val.currRow + 1) % ROW_MAX;
    col = val.dispBuffer[val.currRow]; //row의 column을 가져온다.

    for (i = 0; i < COLUMN_MAX; i++)
    {
        if (col & (0x01<<i))
            digitalWrite(ledMap[COL][i], LOW);//column on
        else
            digitalWrite(ledMap[COL][i], HIGH);//column off
    }
    digitalWrite(ledMap[ROW][val.currRow], HIGH); //row port enable
}

#ifdef _SLIDE_EN
void slideProcessInit(unsigned char *image)
{
    unsigned int i;
    memset(val.slide.buffer, 0x00, sizeof(val.slide.buffer));
    for (i = 0; i < ROW_MAX; i++)
    {
        val.slide.buffer[i][0] = image[i];
    }
    // memcpy(val.dispBuffer, image, sizeof(val.dispBuffer));
    memset(val.dispBuffer, 0x00, sizeof(val.dispBuffer));
    val.slide.idex= 0;
    val.slide.dir = 0;
    val.timeDealy = 1000;
}
void slideProcess(void)
{
    unsigned int i;
    unsigned char dispBufferTmp[ROW_MAX];
    unsigned long *p;

    for (i = 0; i < ROW_MAX; i++)
    {
        p = (unsigned long*)&val.slide.buffer[i];
        if (val.slide.dir == 0)
        {
            *p <<= 1;
        }else{
            *p >>= 1;
        }
        dispBufferTmp[i] = val.slide.buffer[i][1];
    }
    memcpy(val.dispBuffer, dispBufferTmp, sizeof(val.dispBuffer));
    val.slide.idex = (val.slide.idex + 1) % (COLUMN_MAX*2);

    if (val.slide.idex == 0)
    {
#if 1
        val.slide.dir = ~val.slide.dir;
        val.timeDealy = 500;
#else
        slideProcessInit(val.rxBuffer);
#endif
    }
}
#endif

void setupMain() 
{
    unsigned char i;
    /*시리얼 초기화*/
    Serial.begin(9600);
    /*변수초기화*/
    memset(&val, 0x00, sizeof(val));
    /*포트 초기화*/
    for (i = 0; i < COLUMN_MAX; i++)
    {
        pinMode(ledMap[ROW][i], OUTPUT); //row
        pinMode(ledMap[COL][i], OUTPUT); //column
    }
    /*led matrix 제어*/
    MsTimer2::set(1, Timer2Interrupt);//timer2 interrupt
    MsTimer2::start();

#ifdef _SLIDE_EN
    /*slide 초기화*/
    memcpy(val.rxBuffer,heart,sizeof(val.rxBuffer));
    slideProcessInit(val.rxBuffer);
#else
    memcpy(val.dispBuffer, heart, sizeof(val.dispBuffer));//heart image 넣기
#endif
    /*주기 설정 처음은 1sec*/
    val.timeCurr = millis();
    val.timeDealy = 1000;
}

void loopMain()
{
    /*serial data를 받아온다.*/
    if (serialGet(val.rxBuffer))
    {
#ifdef _SLIDE_EN
        slideProcessInit(val.rxBuffer);
#else
        memcpy(val.dispBuffer, val.rxBuffer, sizeof(val.dispBuffer));
#endif
    }

    /*100ms 주기로 slideProcess를 실행한다. */
    if ((millis() - val.timeCurr) > val.timeDealy)
    {
        val.timeCurr = millis();
        val.timeDealy = 100;
#ifdef _SLIDE_EN
        slideProcess();
#endif
    }
}