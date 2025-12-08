//****************************************************************************************//
//  Author:     Philip Biechl                                                             //
//  Project:    Embedded Systems - Snake Game                                             //
//  Place:      Game_Environment_Modules                                                  //
//****************************************************************************************//

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <unistd.h>
#include "driver/gpio.h"
#include "sdkconfig.h"
#include "nvs_flash.h"
#include "nvs.h"
#include "esp_system.h"
#include "esp_log.h"

// Default value to get, if not loadable
#define DEFAULT_LOADED_VALUE        0

// Function to initalise NVS-storage connection
void nvs_init() {
    esp_err_t ret = nvs_flash_init();
    if (ret == ESP_ERR_NVS_NO_FREE_PAGES || ret == ESP_ERR_NVS_NEW_VERSION_FOUND) {
        ESP_ERROR_CHECK(nvs_flash_erase());
        ret = nvs_flash_init();
    }
    ESP_ERROR_CHECK(ret);
}

// Funcion to save values to NVS-storage and return error msg if a step is malfunctioning
void save_value_to_nvs(const char* key, int32_t value) {
    nvs_handle_t my_handle;


    esp_err_t err = nvs_open("storage", NVS_READWRITE, &my_handle);
    if (err != ESP_OK) {
        ESP_LOGE("NVS", "Error (%s) opening NVS handle!", esp_err_to_name(err));
        return;
    }

    err = nvs_set_i32(my_handle, key, value);
    if (err != ESP_OK) {
        ESP_LOGE("NVS", "Error (%s) setting value!", esp_err_to_name(err));
    }

    err = nvs_commit(my_handle);
    if (err != ESP_OK) {
        ESP_LOGE("NVS", "Error (%s) committing value!", esp_err_to_name(err));
    }

    nvs_close(my_handle);
}

// Function to get values from NVS-storage and return error msg if necessary
int32_t get_value_from_nvs(const char* key) {
    nvs_handle_t my_handle;
    int32_t value = DEFAULT_LOADED_VALUE;

    esp_err_t err = nvs_open("storage", NVS_READONLY, &my_handle);
    if (err != ESP_OK) {
        ESP_LOGE("NVS", "Error (%s) opening NVS handle!", esp_err_to_name(err));
        return value;
    }

    err = nvs_get_i32(my_handle, key, &value);

    nvs_close(my_handle);
    switch (err) {
        case ESP_OK:
            return value;
            break;
        case ESP_ERR_NVS_NOT_FOUND:
            return DEFAULT_LOADED_VALUE;
            break;
        default :
            nvs_close(my_handle);
            return DEFAULT_LOADED_VALUE;
    }
    return value;
}