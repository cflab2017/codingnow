#include "global.h"

void setupMain() 
{
    /*시리얼 초기화*/
    Serial.begin(115200);
    Serial.println();
    /*장치 초기화*/
    if (camera_init() != ESP_OK)
    {
        ESP.restart();
        return;
    }
    if (init_sdcard() != ESP_OK)
    {
        ESP.restart();
        return;
    }
    wifi_init();
    init_time();
    webserver_init();
}

void loopMain()
{
    webserver_handler();
}