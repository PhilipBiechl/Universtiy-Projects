/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#ifndef FILEHANDLER_H
#define FILEHANDLER_H

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
#include <cJSON.h>

#include "../include/server_data.h"
#include "../include/controller.h"

esp_err_t index_get_handler(httpd_req_t *req);
esp_err_t style_css_get_handler(httpd_req_t *req);
esp_err_t script_js_get_handler(httpd_req_t *req);
esp_err_t chart_js_get_handler(httpd_req_t *req);
esp_err_t data_rcv_handler(httpd_req_t *req);
esp_err_t toggle_regulation_mode_handler(void);
esp_err_t toggle_simulation_mode_handler(void);
esp_err_t get_gSimMode_status(httpd_req_t *req);
esp_err_t submit_post_handler(httpd_req_t *req);

#endif // file_handler.h