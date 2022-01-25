#include "global.h"

#include "driver/sdmmc_host.h"
#include "driver/sdmmc_defs.h"
#include "sdmmc_cmd.h"
#include "esp_vfs_fat.h"

esp_err_t init_sdcard(void)
{
    esp_err_t ret = ESP_FAIL;
    sdmmc_host_t host = SDMMC_HOST_DEFAULT();
    sdmmc_slot_config_t slot_config = SDMMC_SLOT_CONFIG_DEFAULT();
    esp_vfs_fat_sdmmc_mount_config_t mount_config = {
        .format_if_mount_failed = true,
        .max_files = 5,
    };
    sdmmc_card_t *card;

    Serial.println("Mounting SD card...");
    ret = esp_vfs_fat_sdmmc_mount("/sdcard", &host, &slot_config, &mount_config, &card);

    switch (ret)
    {
        case ESP_OK:
            Serial.printf("CID name %s!\n", card->cid.name);
            break;
        case ESP_ERR_INVALID_STATE:
            Serial.printf("File system already mounted\n");
            break;
        case ESP_FAIL:
            Serial.printf("Failed to mount filesystem. If you want the card to be formatted, set format_if_mount_failed = true.\n");
            break;
        default:
            Serial.printf("Failed to initialize the card (%d). Make sure SD card lines have pull-up resistors in place.\n", ret);
            break;
    }
    return ret;
}

void getSDfreeSize(float *ssd_used_Mbytes, float *ssd_used_per)
{
    FATFS *fs;
    DWORD fre_clust, fre_sect, tot_sect;

    /* Get volume information and free clusters of sdcard */
    auto res = f_getfree("/sdcard/", &fre_clust, &fs);
    if (res)
    {
        return;
    }

    /* Get total sectors and free sectors */
    tot_sect = (fs->n_fatent - 2) * fs->csize;
    fre_sect = fre_clust * fs->csize;

    uint64_t tmp_total_bytes = (uint64_t)tot_sect * FF_SS_SDCARD;
    uint64_t tmp_free_bytes = (uint64_t)fre_sect * FF_SS_SDCARD;
    uint64_t tmp_useed_bytes = tmp_total_bytes - tmp_free_bytes;

    *ssd_used_Mbytes = ((float)tmp_useed_bytes / 1024) / 1024;
    *ssd_used_per = (float)tmp_useed_bytes / (float)tmp_total_bytes * 100;

    /* Print the free space in bytes */
    Serial.printf("%llu total Mbytes. %f used Mbytes. %f%s\n", 
            (tmp_total_bytes / 1024) / 1024, 
            *ssd_used_Mbytes, 
            *ssd_used_per, 
            "%");
}