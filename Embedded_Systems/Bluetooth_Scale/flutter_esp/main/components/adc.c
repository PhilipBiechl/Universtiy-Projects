/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Projekt Embedded Systems                                                   **/
/*********************************************************************************************/

#include "include/adc.h"

uint8_t scaleMeasure[15] = {0};
uint8_t highest = 0, high = 0, mid = 0, low = 0;

void splitter(uint32_t input, uint8_t *highest_bytes, uint8_t *higher_bytes, uint8_t *mid_bytes, 
uint8_t *lower_bytes) {
    *highest_bytes = (input >> 24) & 0xFF;
    *higher_bytes = (input >> 16) & 0xFF;
    *mid_bytes = (input >> 8) & 0xFF;
    *lower_bytes = input & 0xFF;
}

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

void init_adc() {
    adc1_config_width(ADC_WIDTH);
    adc1_config_channel_atten(ADC_CHANNEL, ADC_ATTEN);
}

void adc_read_task(void* arg) {
    
    while (1) {
        int adc_value = adc1_get_raw(ADC_CHANNEL);
        splitter(
            (((MAX_SCALE - MIN_SCALE) / MAX_POTI) * adc_value + MIN_SCALE) * 1000, 
            &highest, &high, &mid, &low);

        printf("%d", adc_value);

        scaleMeasure[1] = highest;
        scaleMeasure[2] = high;
        scaleMeasure[3] = mid;
        scaleMeasure[4] = low;
        vTaskDelay(pdMS_TO_TICKS(500));
    }
}