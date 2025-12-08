/*********************************************************************************************/
/**  Author:     Philip Biechl (reference from lessons)                                     **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#include "../include/shtc3.h"

/* reads data from SHTC3 to communicate  */
esp_err_t readSHTC3ID(uint16_t* pID) {
	uint8_t writeBuf[2] = { SHTC3_CMD_READ_ID >> 8, SHTC3_CMD_READ_ID & 0xFF }; // Read ID register
	uint8_t readBuf[2];
	esp_err_t res = i2c_master_write_read_device(I2C_INTERFACE, SHTC3_ADDRESS, writeBuf, 2, readBuf, 2, pdMS_TO_TICKS(100));
	if (res != ESP_OK) {
		*pID = 0;
	} else {
        *pID = readBuf[0] << 8 | readBuf[1];
    }
    return res;
}

/* initialises connection with temperature sensor */
esp_err_t shtc3_init() {
    ESP_LOGI(TAG, "init SHTC3");
    uint16_t id;
    esp_err_t res = readSHTC3ID(&id);
    if ((res == ESP_OK) && ((id & SHTC3_ID_MASK) == SHTC3_ID)) {
        ESP_LOGI(TAG, "SHTC3 found, ID: 0x%04X", id);
    } else {
        ESP_LOGE(TAG, "SHTC3 NOT FOUND! (ID: 0x%04X)", id);
    }
    return res;
}

/* reads actual temperature / humidity data and uploads it to referenced values */
esp_err_t shtc3_read(float* pTemperature, float* pHumidity) {
	uint8_t writeBuf[2] = { SHTC3_CMD_READ >> 8, SHTC3_CMD_READ & 0xFF }; 
	uint8_t readBuf[6];
	esp_err_t res = i2c_master_write_read_device(I2C_INTERFACE, SHTC3_ADDRESS, writeBuf, 2, readBuf, 6, pdMS_TO_TICKS(100));
	if (res != ESP_OK) {
		*pTemperature = 0.0f;
		*pHumidity = 0.0f;
	} else {
	    *pTemperature = 175.0f * (float)(readBuf[0] << 8 | readBuf[1]) / 65536.0f - 51.5f; 
	    *pHumidity = 100.0f * (float)(readBuf[3] << 8 | readBuf[4]) / 65536.0f;
    }
    return res;
}