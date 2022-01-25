#include "global.h"

#include <WiFi.h>

const char *WIFI_SSID = "TEST";
const char *WIFI_PASS = "TEST1234";

void wifi_init(void)
{
    // WiFi.persistent(false);
    // WiFi.mode(WIFI_STA);
    WiFi.begin(WIFI_SSID, WIFI_PASS); // nos conectamos a la red wifi
    while (WiFi.status() != WL_CONNECTED)
    {
        delay(500);
    }

    Serial.print("http://");
    Serial.print(WiFi.localIP());
    Serial.println("/"); // para conectarnos IP res alta
}