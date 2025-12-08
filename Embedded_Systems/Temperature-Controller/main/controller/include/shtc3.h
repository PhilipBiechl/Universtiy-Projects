/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#ifndef SHTC3_H
#define SHTC3_H

#include <stdint.h>
#include "esp_err.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2c.h"
#include "esp_log.h"
#include <stdio.h>
#include <string.h>
#include "esp_wifi.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include "esp_system.h"
#include "esp_netif.h"
#include "esp_http_server.h"
#include "esp_spiffs.h"

#define TAG                 "SHTC3"
#define I2C_INTERFACE		I2C_NUM_0

#define SHTC3_ADDRESS       0x70
#define SHTC3_CMD_READ_ID   0xEFC8
#define SHTC3_ID            0x807
#define SHTC3_ID_MASK       0x83F
#define SHTC3_CMD_READ      0x7CA2

struct SHTC3Event {
    float temperature;
    float humidity;
};

esp_err_t shtc3_init(void);
esp_err_t shtc3_read(float* pTemperature, float* pHumidity);

#endif // shtc3.h