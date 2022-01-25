#ifndef camera_h_en
#define camera_h_en

//#include <esp32cam.h>
#include "esp_camera.h"

typedef struct
{
    uint8_t *buf;
    size_t len;
    int fileCount;
    float ssd_used_Mbytes;
    float ssd_used_per;
} capture_val_type;

bool camera_init(void);
float cam_fb_capture(void);
void cam_fb_release(void);
void save_photo(char *mfile, capture_val_type *img, char *msg);
#endif