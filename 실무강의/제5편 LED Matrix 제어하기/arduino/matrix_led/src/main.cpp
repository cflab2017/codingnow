#include "global.h"
#include <MsTimer2.h>
/*
Arduino Uno Board 메인 컨트롤러 : Atmega328 
Atmega328를 3개의 타이머가 있고 PWM 출력 및 시간 관련 함수들을 제공
Timer0 - 8Bit : PWM 5/6핀, 시간 관련 함수 (delay(), millis() 등)
Timer1 - 16Bit : PWM 9/10핀 (외부 라이브러리 Servo.h 와 함께 사용 불가)
Timer2 - 8Bit : PWM 3/11핀 (외부 라이브러리 MsTimer2.h 와 함께 사용 불가)
*/

#define _CONTROL_PYTHON_EN
// #define _TEST_0_EN
// #define _DEMO_EN

unsigned char ledMap[2][COLUMN_MAX] = {
    /*ROW*/ {A5, 3, 13, A2, 6, 12, 7, 10},
    /*COL*/ {2, 8, 9, A4, 11, A3, 4, 5},
};

typedef struct{
unsigned char dispBuffer[ROW_MAX];//display data buffer
unsigned char rxBuffer[ROW_MAX];//serial data buffer
unsigned char currRow;

#if defined(_DEMO_EN) || defined(_TEST_0_EN)
unsigned long timeCurr;
unsigned long timeDealy;
#ifdef _TEST_0_EN
unsigned char idexRow;
unsigned char idexCol;
#endif
#ifdef _DEMO_EN
unsigned char imageIdex;
#endif
#endif
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

#ifdef _DEMO_EN
#define IMAGE_MAX 4
unsigned char const images[IMAGE_MAX][ROW_MAX] = {
    {0x00, 0x42, 0xA5, 0x00, 0x00, 0x00, 0x42, 0x3C},
    {0x00, 0x42, 0xA5, 0x42, 0x00, 0x00, 0x42, 0x3C},
    {0x00, 0x42, 0xA5, 0x00, 0x00, 0x00, 0x3C, 0x42},
    {0x00, 0x66, 0x99, 0x81, 0x81, 0x42, 0x24, 0x18},
};
#endif

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

void setupMain() 
{
    unsigned char i;
    Serial.begin(9600);//시리얼 초기화
    memset(&val, 0x00, sizeof(val));//변수초기화
    for (i = 0; i < COLUMN_MAX; i++) //포트 초기화
    {
        pinMode(ledMap[ROW][i], OUTPUT); //row
        pinMode(ledMap[COL][i], OUTPUT); //col
    }
    memcpy(val.dispBuffer, heart, sizeof(val.dispBuffer));//heart image 넣기
    // val.dispBuffer[1] = 0x01;
    // memset(val.dispBuffer,0xff, sizeof(val.dispBuffer));
    MsTimer2::set(1, Timer2Interrupt);//timer2 interrupt
    MsTimer2::start();

#if defined(_DEMO_EN) || defined(_TEST_0_EN)
    val.timeCurr = millis();
    val.timeDealy = 1000;
#endif
}

void loopMain()
{
#ifdef _CONTROL_PYTHON_EN
    if (serialGet(val.rxBuffer))
    {
        memcpy(val.dispBuffer, val.rxBuffer, sizeof(val.dispBuffer));
    }
#endif

#if defined(_DEMO_EN) || defined(_TEST_0_EN)
    if ((millis() - val.timeCurr) > val.timeDealy)
    {
        val.timeCurr = millis();
#ifdef _DEMO_EN
        val.timeDealy = 500;
        memcpy(val.dispBuffer, &images[val.imageIdex], sizeof(val.dispBuffer));
        val.imageIdex = (val.imageIdex + 1) % IMAGE_MAX;
#endif
#ifdef _TEST_0_EN
        val.timeDealy = 100;
        memset(val.dispBuffer, 0x00, sizeof(val.dispBuffer));
        val.dispBuffer[val.idexRow] = 0x01 << val.idexCol;

        val.idexCol = (val.idexCol + 1) % COLUMN_MAX;
        if (val.idexCol == 0)
        {
            val.idexRow = (val.idexRow + 1) % ROW_MAX;
        }
#endif
    }
#endif
}