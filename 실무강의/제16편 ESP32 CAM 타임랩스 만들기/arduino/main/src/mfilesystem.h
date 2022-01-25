#ifndef mfilesystem_h_en
#define mfilesystem_h_en

esp_err_t init_sdcard(void);
void getSDfreeSize(float *ssd_used_Mbytes, float *ssd_used_per);
#endif