/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#ifndef STARTUP_H
#define STARTUP_H

#include <stdio.h>
#include "esp_log.h"
#include "controller/include/shtc3.h"
#include "controller/include/controller.h"
#include "controller/include/data_control.h"
#include "controller/include/adc_i2c.h"
#include "controller/include/server_init.h"
#include "controller/include/file_handler.h"
#include "controller/include/server_data.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"

void startup(void);

#endif // startup.h