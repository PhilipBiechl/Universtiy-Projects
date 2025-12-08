/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#ifndef DATACONTROL_H
#define DATACONTROL_H

#include <stdio.h>
#include <string.h>
#include "esp_wifi.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include "esp_log.h"
#include "esp_system.h"
#include "esp_netif.h"
#include "esp_http_server.h"
#include "esp_spiffs.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

#include "../include/server_data.h"
#include "../include/shtc3.h"
#include "../include/controller.h"

#ifndef SIM_PARAM

#define HEATING_POWER   200    // in Watt
#define TEMP_CAPACITY   2000   // in J/K
#define HEAT_LOSS       5      // in W/K

#endif

void data_read_task(void* arg);

#endif // data_control.h