/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#include "../include/adc_i2c.h"

/* previous value */
int32_t storedValue = 0;

/* initialises the interface */
void initI2C(i2c_port_t i2c_num) {
	ESP_LOGI(TAG, "init I2C");
	i2c_config_t conf = {
		.mode = I2C_MODE_MASTER,
		.sda_io_num = GPIO_NUM_5,
		.scl_io_num = GPIO_NUM_6,
		.sda_pullup_en = GPIO_PULLUP_ENABLE,
		.scl_pullup_en = GPIO_PULLUP_ENABLE,
		.master.clk_speed = 400000
	};
	i2c_param_config(i2c_num, &conf);
	esp_err_t res = i2c_driver_install(i2c_num, conf.mode, 0, 0, 0);
	if (res != ESP_OK) {
		ESP_LOGW(TAG, "i2c_driver_install() FAILED: %d!", res);
		return;
	} else {
		ESP_LOGI(TAG, "i2c_driver_install() OK");
	}
}

/* initialises the connection to poti */
void init_adc() {
    adc1_config_width(ADC_WIDTH);
    adc1_config_channel_atten(ADC_CHANNEL, ADC_ATTEN);
}

/* task to read data from poti & if there is a significant change - upload the new value */
void adc_read_task(void* arg) {
    while (1) {
        int adc_value = adc1_get_raw(ADC_CHANNEL);
		if (((float)abs(storedValue - adc_value) / (adc_value + 1)) > 0.05) {
			storedValue = adc_value;
			gSoll = ((MAX_TEMP - MIN_TEMP) / MAX_POTI) * (float)adc_value + MIN_TEMP;
		}
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}