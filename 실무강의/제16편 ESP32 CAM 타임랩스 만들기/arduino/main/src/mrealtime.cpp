
#include "global.h"

#include "time.h"
#include "lwip/err.h"
#include "lwip/apps/sntp.h"

struct tm timeinfo;
time_t now;
char strftime_buf[64];

void init_time(void)
{
    sntp_setoperatingmode(SNTP_OPMODE_POLL);
    sntp_setservername(0, "pool.ntp.org");
    // sntp_setservername(1, "europe.pool.ntp.org");
    // sntp_setservername(2, "uk.pool.ntp.org ");
    // sntp_setservername(3, "us.pool.ntp.org");
    sntp_setservername(4, "time1.google.com");
    sntp_init();
    // wait for time to be set
    now = 0;
    timeinfo = {0};
    int retry = 0;
    const int retry_count = 10;
    while (timeinfo.tm_year < (2016 - 1900) && ++retry < retry_count)
    {
        Serial.printf("Waiting for system time to be set... (%d/%d)\n", retry, retry_count);
        delay(2000);
        time(&now);
        localtime_r(&now, &timeinfo);
    }

    time(&now);
    // setenv("TZ", "GMT0BST,M3.5.0/01,M10.5.0/02", 1);
    // Set timezone to Seoul Standard Time
    setenv("TZ", "CST-9", 1);
    tzset();

    Serial.printf("%s\n", getStrCurrentTime());
}

char* getStrCurrentTime(void)
{
    time(&now);
    localtime_r(&now, &timeinfo);
    strftime(strftime_buf, sizeof(strftime_buf), "%F_%H_%M_%S", &timeinfo);
    return strftime_buf;
}