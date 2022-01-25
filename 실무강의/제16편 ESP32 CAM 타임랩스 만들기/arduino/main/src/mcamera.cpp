#include "global.h"

//#include "soc/soc.h"
//#include "soc/rtc_cntl_reg.h"

camera_fb_t *fb;

//   카메라핀 설정
#define PWDN_GPIO_NUM 32
#define RESET_GPIO_NUM -1
#define XCLK_GPIO_NUM 0
#define SIOD_GPIO_NUM 26
#define SIOC_GPIO_NUM 27

#define Y9_GPIO_NUM 35
#define Y8_GPIO_NUM 34
#define Y7_GPIO_NUM 39
#define Y6_GPIO_NUM 36
#define Y5_GPIO_NUM 21
#define Y4_GPIO_NUM 19
#define Y3_GPIO_NUM 18
#define Y2_GPIO_NUM 5
#define VSYNC_GPIO_NUM 25
#define HREF_GPIO_NUM 23
#define PCLK_GPIO_NUM 22

bool camera_init(void)
{
    //test 할때만
    //WRITE_PERI_REG(RTC_CNTL_BROWN_OUT_REG, 0); // BROWN OUT DESABLE

    camera_config_t config;
    config.ledc_channel = LEDC_CHANNEL_0;
    config.ledc_timer = LEDC_TIMER_0;
    config.pin_d0 = Y2_GPIO_NUM;
    config.pin_d1 = Y3_GPIO_NUM;
    config.pin_d2 = Y4_GPIO_NUM;
    config.pin_d3 = Y5_GPIO_NUM;
    config.pin_d4 = Y6_GPIO_NUM;
    config.pin_d5 = Y7_GPIO_NUM;
    config.pin_d6 = Y8_GPIO_NUM;
    config.pin_d7 = Y9_GPIO_NUM;
    config.pin_xclk = XCLK_GPIO_NUM;
    config.pin_pclk = PCLK_GPIO_NUM;
    config.pin_vsync = VSYNC_GPIO_NUM;
    config.pin_href = HREF_GPIO_NUM;
    config.pin_sscb_sda = SIOD_GPIO_NUM;
    config.pin_sscb_scl = SIOC_GPIO_NUM;
    config.pin_pwdn = PWDN_GPIO_NUM;
    config.pin_reset = RESET_GPIO_NUM;
    config.xclk_freq_hz = 20000000;
    config.pixel_format = PIXFORMAT_JPEG;
    // init with high specs to pre-allocate larger buffers
#if 0
    if (psramFound())
    {
        config.frame_size = FRAMESIZE_UXGA;
        config.jpeg_quality = 10;
        config.fb_count = 2;
    }
    else
#endif
    {
        config.frame_size = FRAMESIZE_SVGA;
        config.jpeg_quality = 12;
        config.fb_count = 1;
    }
    // camera init
    esp_err_t err = esp_camera_init(&config);
    if (err != ESP_OK)
    {
        Serial.printf("Camera init failed with error 0x%x", err);
        return ESP_FAIL;
    }

    sensor_t *s = esp_camera_sensor_get();
    s->set_framesize(s, FRAMESIZE_VGA);
    return ESP_OK;
}

float cam_fb_capture(void)
{
    fb = esp_camera_fb_get();
    if (!fb)
    {
        Serial.println("CAPTURE FAIL");
        return 0;
    }
    float size = (float)fb->len / 1024;
    Serial.printf("CAPTURE OK %dx%d %fkbyte\n",
                  fb->width, fb->height,
                  size);
    return size;
}

void cam_fb_release(void)
{
    if (fb != NULL)
    {
        esp_camera_fb_return(fb);
        fb = NULL;
        Serial.println("capture release!!");
    }
}

void save_photo(char *filename, capture_val_type *img, char *msg)
{
    float size;
    // capture using the camera.
    size = cam_fb_capture();
    if (size == 0)
    {
        return;
    }

    // copy to web display buffer
    if (img->buf != NULL)
    {
        free(img->buf);
    }
    img->buf = (uint8_t *)malloc(fb->len);
    memcpy(img->buf, fb->buf, fb->len);
    img->len = fb->len;

    // save it as a jpg file
    FILE *file = fopen(filename, "w");
    if (file != NULL)
    {
        size_t err = fwrite(fb->buf, 1, fb->len, file);
        if (err != 1)
        {
            Serial.printf("File saved: %s\n", filename);
            img->fileCount++;
            sprintf(msg, "#%d\n%s\nsize : %.2fKbyte", img->fileCount, filename, size);
        }else{
            Serial.printf("Fail file save %d\n", err);
            sprintf(msg, "Fail file save");
        }
        fclose(file);
        // Find out the size of the ssd
        getSDfreeSize(&img->ssd_used_Mbytes, &img->ssd_used_per);
    }else{
        Serial.println("Could not open file");
    }
    // release camera
    cam_fb_release();
}

