/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#ifndef ADCI2C_H
#define ADCI2C_H

#include <stdio.h>
#include <string.h>
#include "esp_log.h"
#include "esp_system.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/i2c.h"
#include "driver/adc.h"
#include "esp_adc_cal.h"

#include "../include/adc_i2c.h"
#include "../include/server_data.h"

#define TAG                 "adc_i2c"

#define ADC_CHANNEL         ADC_CHANNEL_2
#define ADC_ATTEN           ADC_ATTEN_DB_11
#define ADC_WIDTH           ADC_BITWIDTH_12

#define MAX_POTI            3700.0f
#define MAX_TEMP            40.0f // °C
#define MIN_TEMP            10.0f // °C

#define LED_PIN             2
#define I2C_INTERFACE		I2C_NUM_0

void initI2C(i2c_port_t i2c_num);
void init_adc();
void adc_read_task(void *arg);

#endif // adc_i2c.h