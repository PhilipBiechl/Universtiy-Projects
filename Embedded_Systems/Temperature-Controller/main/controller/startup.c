/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#include "include/startup.h"

/* starts all functions needed for the webserver */
void startup() {
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);

    ESP_ERROR_CHECK(esp_netif_init());
    ESP_ERROR_CHECK(esp_event_loop_create_default());

    wifi_init_softap();
    vTaskDelay(pdMS_TO_TICKS(2000));

    init_adc();
    init_spiffs();
    initI2C(I2C_INTERFACE);
    shtc3_init();

    /* these tasks continue to update the temperature, etc. data */
    xTaskCreate(adc_read_task, "ADC Read Task", 2048, NULL, 5, NULL);
    xTaskCreate(data_read_task, "Data Read Task", 2048, NULL, 5, NULL);
}