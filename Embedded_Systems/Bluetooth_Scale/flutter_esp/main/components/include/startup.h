/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Projekt Embedded Systems                                                   **/
/*********************************************************************************************/

#ifndef STARTUP_H
#define STARTUP_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <inttypes.h>
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/event_groups.h"
#include "esp_system.h"
#include "esp_log.h"
#include "nvs_flash.h"
#include "esp_bt.h"
#include "esp_gatts_api.h"

#include "esp_gap_ble_api.h"
#include "esp_gatts_api.h"
#include "esp_bt_defs.h"
#include "esp_bt_main.h"
#include "esp_gatt_common_api.h"
#include "esp_timer.h"

#include "include/adc.h"
#include "include/gatts_manage.h"
#include "sdkconfig.h"

#define GATTS_TAG               "BLE_SERVER"

#define GATTS_SERVICE_UUID      0x00FF
#define GATTS_CHAR_UUID         0xFF01
#define GATTS_DESCR_UUID        0x3333
#define GATTS_NUM_HANDLE        4

#define TEST_DEVICE_NAME        "SCALE_BLE_DEVICE"

#define CHAR_VAL_LEN_MAX        0x40
#define PREPARE_BUF_MAX_SIZE    1024

void startup(void);

#endif //startup.h