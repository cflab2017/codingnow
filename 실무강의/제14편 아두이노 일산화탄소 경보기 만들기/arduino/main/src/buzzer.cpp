#include "global.h"
#include "buzzer.h"

#define pin_buzzer 2

#define NOTE_C5 523 //도 
#define NOTE_D5 587 //레 
#define NOTE_E5 659 //미 
#define NOTE_F5 698 //파 
#define NOTE_G5 784 //솔 
#define NOTE_A5 880 //라 
#define NOTE_B5 988 //시 
#define NOTE_C6 1047 //도

#if 1
int melody[] = { NOTE_C5,NOTE_C5,NOTE_C5,NOTE_C5,NOTE_C5, NOTE_E5,NOTE_G5,NOTE_G5,NOTE_E5,NOTE_C5, NOTE_G5,NOTE_G5,NOTE_E5,NOTE_G5,NOTE_G5,NOTE_E5, NOTE_C5,NOTE_C5,NOTE_C5, NOTE_G5,NOTE_G5,NOTE_E5,NOTE_C5, NOTE_G5,NOTE_G5,NOTE_G5, NOTE_G5,NOTE_G5,NOTE_E5,NOTE_C5, NOTE_G5,NOTE_G5,NOTE_G5, NOTE_G5,NOTE_G5,NOTE_E5,NOTE_C5, NOTE_G5,NOTE_G5,NOTE_G5,NOTE_A5,NOTE_G5, NOTE_C6,NOTE_G5,NOTE_C6,NOTE_G5, NOTE_E5,NOTE_D5,NOTE_C5 };

int noteDurations[]={ 4,8,8,4,4, 4,8,8,4,4, 8,8,4,8,8,4, 4,4,2, 4,4,4,4, 4,4,2, 4,4,4,4, 4,4,2, 4,4,4,4, 8,8,8,8,2, 4,4,4,4, 4,4,2 };

void play_buzzer_test_02(void)
{
    for (int i = 0; i < 49; i++)
    {
        int Durations = 1000 / noteDurations[i]; // 음계의 음길이 계산
        tone(pin_buzzer, melody[i], Durations);
        int pauseBetweenNotes = Durations * 1.3;
        delay(pauseBetweenNotes);
        noTone(pin_buzzer);
    }
}

unsigned int code[] = {
    NOTE_C5, NOTE_D5, NOTE_E5, NOTE_F5, NOTE_G5, NOTE_A5, NOTE_B5, NOTE_C6};

void play_buzzer_test_01(void)
{
    for (int i = 0; i < sizeof(code) / sizeof(unsigned int); i++)
    {
        tone(pin_buzzer, code[i], 1000);
        delay(250);
    }
    noTone(pin_buzzer);
}
#endif

void play_buzzer_danger(void)
{
    tone(pin_buzzer, NOTE_C6, 1000);
    delay(250);
    noTone(pin_buzzer);
}

void init_buzzer(void)
{
    pinMode(pin_buzzer,OUTPUT);
}

void play_buzzer(void)
{
    play_buzzer_danger();
    //play_buzzer_test_01();
    // play_buzzer_test_02();
}