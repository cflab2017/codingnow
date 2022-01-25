#include "global.h"
// #include <WebServer.h>
#include <ESPAsyncWebServer.h>
//#include <esp32cam.h>
//#include "esp_camera.h"
#include "mwebserverhtml.h"

/* AsyncWebServer 참고 사이트
https://randomnerdtutorials.com/display-images-esp32-esp8266-web-server/
[LIB]
https://github.com/me-no-dev/ESPAsyncWebServer
https://github.com/me-no-dev/AsyncTCP
*/

#define CAPTURE_INTERVAL_TIME (1000 * 60)
// #define CAPTURE_INTERVAL_TIME (1000 * 5)

static webserver_val_type web;

AsyncWebServer server(80);

static void handleRoot(AsyncWebServerRequest *request)
{
    if (request->hasArg("CONTROL"))
    {
        String value = request->arg("CONTROL");
        Serial.print("CONTROL = ");
        Serial.println(value);

        if (value == "Start" && web.isCaptureRun == false)
        {
            web.isCaptureRun = true;
            web.img.fileCount = 0;
            sprintf(web.msg, "ESP32 CAM Capture Start!!");
            Serial.printf("%s\n", web.msg);
            web.time_last_capture += CAPTURE_INTERVAL_TIME;
        }
        if (value == "Stop")
        {
            web.isCaptureRun = false;
            if (web.img.buf != NULL)
            {
                free(web.img.buf);
            }
            web.img.buf = NULL;
            sprintf(web.msg, "ESP32 CAM Capture Stop!!");
            Serial.printf("%s\n", web.msg);
        }
    }
    String s = (const __FlashStringHelper *)index_html;
    String strUsed_Mbytes = (String)web.img.ssd_used_Mbytes;
    String strUsed_per = (String)web.img.ssd_used_per;

    s.replace("@@USED_MBYTE@@", strUsed_Mbytes);
    s.replace("@@USED_PER@@", strUsed_per);
    s.replace("@@MESSAGE@@", web.msg);
    if (web.isCaptureRun == false)
    {
        s.replace("<meta http-equiv='refresh' content='5'>","");
        s.replace("<img src=\"cam\">", "");
    }else{
        if (web.img.buf == NULL)
        {
            s.replace("<img src=\"cam\">", "");
        }
    }
    request->send(200, "text/html", s);
    s.clear();
    strUsed_Mbytes.clear();
    strUsed_per.clear();
}

static bool capture_handler(AsyncWebServerRequest *request)
{
    if (web.img.buf == NULL) return true;

    AsyncWebServerResponse *response =
        request->beginResponse_P(200,
                                 "image/jpg",
                                 web.img.buf,
                                 web.img.len);
    request->send(response);
    return true;
}

void webserver_init(void)
{
//변수 초기화
    memset(&web,0x00,sizeof(web));
    web.img.buf = NULL;
//서버 초기화
    server.on("/", HTTP_ANY, handleRoot);
    server.on("/cam", HTTP_GET, capture_handler);
    server.begin();
    Serial.println("web sever ready!!");
    sprintf(web.msg, "web sever ready!!");
}

void webserver_handler(void){
    if (millis() - web.time_last_capture > CAPTURE_INTERVAL_TIME)
    {
        web.time_last_capture = millis();
        if (web.isCaptureRun)
        {
            sprintf(web.filename, "/sdcard/%s.jpg", getStrCurrentTime());
            save_photo(web.filename, &web.img, web.msg);
        }
    }
}