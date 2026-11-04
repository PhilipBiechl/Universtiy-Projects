/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Projekt Embedded Systems                                                   **/
/*********************************************************************************************/

#ifndef GATTS_MANAGE_H
#define GATTS_MANAGE_H

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
#include "sdkconfig.h"

#define GATTS_TAG "BLE_SERVER"

static void gatts_event_handler(esp_gatts_cb_event_t event, esp_gatt_if_t gatts_if, esp_ble_gatts_cb_param_t *param);

#define GATTS_SERVICE_UUID      0x00FF
#define GATTS_CHAR_UUID         0xFF01
#define GATTS_DESCR_UUID        0x3333
#define GATTS_NUM_HANDLE        4

#define TEST_DEVICE_NAME        "SCALE_BLE_DEVICE"

#define CHAR_VAL_LEN_MAX        0x40
#define PREPARE_BUF_MAX_SIZE    1024

#define PROFILE_NUM             2
#define APP_ID                  0
#define PROFILE_B_APP_ID        1

#define adv_config_flag         (1 << 0)
#define scan_rsp_config_flag    (1 << 1)

void send_value_task(void *arg);

typedef struct {
    uint8_t                 *prepare_buf;
    int                     prepare_len;
} prepare_type_env_t;

static prepare_type_env_t a_prepare_write_env;

void write_event_env(esp_gatt_if_t gatts_if, prepare_type_env_t *prepare_write_env, esp_ble_gatts_cb_param_t *param);
void exec_write_event_env(prepare_type_env_t *prepare_write_env, esp_ble_gatts_cb_param_t *param);
void gap_event_handler(esp_gap_ble_cb_event_t event, esp_ble_gap_cb_param_t *param);
void init_gev(void);

#endif //gatts_manage.h