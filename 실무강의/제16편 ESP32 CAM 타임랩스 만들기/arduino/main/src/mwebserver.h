#ifndef mwebserver_h_en
#define mwebserver_h_en


typedef struct
{
    char msg[21 + 32 + 32 + 32];
    char filename[21 + 32];
    bool isCaptureRun;
    long time_last_capture;
    capture_val_type img;
} webserver_val_type;

void webserver_init(void);
void webserver_handler(void);
#endif