/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#ifndef SERVERINIT_H
#define SERVERINIT_H

#include <stdio.h>
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

#include "../include/file_handler.h"
#include "../include/shtc3.h"
#include "../include/controller.h"
#include "../include/server_data.h"

#define TAG "Server_Init"

#define PID_KI      0.3
#define PID_KP      2
#define PID_KD      0
#define MAX_PID     40
#define MIN_PID     -20
#define PID_T       0.3

static httpd_handle_t start_webserver(void);

void init_spiffs(void);
void wifi_init_softap(void);
void server_main(void);

#endif // server_init.h