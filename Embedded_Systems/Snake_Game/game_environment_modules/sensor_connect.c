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
#include "driver/spi_master.h"
#include "led_strip.h"
#include "sdkconfig.h"
#include "esp_system.h"

// Include Headers
#include "include/nvs_storage_connect.h"
#include "include/matrix_control.h"
#include "include/menu_control.h"
#include "include/led_symbols.h"

// Z-Axis acceleration
#define Z_ACCEL_RECOGNIZE   2350

// LED Matrix Pin
#define BLINK_GPIO          8

// SPI Configurations
#define PIN_NUM_MISO        7       
#define PIN_NUM_MOSI        4       
#define PIN_NUM_CLK         10      
#define PIN_NUM_CS          1       

// ICM-42688-P Registers
#define REG_WHO_AM_I        0x75
#define REG_PWR_MGMT_1      0x06
#define REG_PWR_MGMT_2      0x07
#define REG_ACCEL_CONFIG0   0x50
#define REG_GYRO_CONFIG0    0x4E
#define REG_ACCEL_XOUT_H    0x1F
#define REG_ACCEL_XOUT_L    0x20
#define REG_ACCEL_YOUT_H    0x21
#define REG_ACCEL_YOUT_L    0x22
#define REG_ACCEL_ZOUT_H    0x23
#define REG_ACCEL_ZOUT_L    0x24
#define REG_GYRO_XOUT_H     0x25
#define REG_GYRO_XOUT_L     0x26
#define REG_GYRO_YOUT_H     0x27
#define REG_GYRO_YOUT_L     0x28
#define REG_GYRO_ZOUT_H     0x29
#define REG_GYRO_ZOUT_L     0x2A

// SPI handler for spi-communication
spi_device_handle_t spi;

// Function to initialize SPI
void spi_init() {
    esp_err_t ret;

    spi_bus_config_t buscfg = {
        .miso_io_num = PIN_NUM_MISO,
        .mosi_io_num = PIN_NUM_MOSI,
        .sclk_io_num = PIN_NUM_CLK,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1,
        .max_transfer_sz = 2 * 8,   // Max transfer size (2 bytes)
    };

    spi_device_interface_config_t devcfg = {
        .clock_speed_hz = 1*1000*1000,           // Clock out at 1 MHz
        .mode = 3,                               // SPI mode 3
        .spics_io_num = PIN_NUM_CS,              // CS pin
        .queue_size = 7,                         // We want to be able to queue 7 transactions at a time
    };

    // Initialize the SPI bus
    ret = spi_bus_initialize(SPI2_HOST, &buscfg, SPI_DMA_CH_AUTO);
    ESP_ERROR_CHECK(ret);

    // Attach the ICM-42688-P to the SPI bus
    ret = spi_bus_add_device(SPI2_HOST, &devcfg, &spi);
    ESP_ERROR_CHECK(ret);
}

// Function to write a register
void icm42688_write_register(uint8_t reg, uint8_t data) {
    spi_transaction_t t;
    memset(&t, 0, sizeof(t));       // Zero out the transaction
    uint8_t out_data[2] = {reg & 0x7F, data};  // Address byte (write) + data byte
    t.length = 8 * 2;               // Transaction length is in bits
    t.tx_buffer = out_data;         // The data
    spi_device_transmit(spi, &t);   // Transmit!
}

// Function to read a register
uint8_t icm42688_read_register(uint8_t reg) {
    spi_transaction_t t;
    memset(&t, 0, sizeof(t));       // Zero out the transaction
    uint8_t out_data[2] = {reg | 0x80, 0x00};  // Address byte (read) + dummy byte
    uint8_t in_data[2] = {0};
    t.length = 8 * 2;               // Transaction length is in bits
    t.tx_buffer = out_data;         // The data to send
    t.rx_buffer = in_data;          // The data to receive
    spi_device_transmit(spi, &t);   // Transmit!

    return in_data[1];              // The received data
}

// Function to initialize the ICM-42688-P
void icm42688_init() {
    // Reset the device and wake it up
    icm42688_write_register(REG_PWR_MGMT_1, 0x01); // Clear sleep bit and set clock source to auto
    vTaskDelay(100 / portTICK_PERIOD_MS);

    // Enable accelerometer and gyroscope in low noise mode
    icm42688_write_register(REG_PWR_MGMT_2, 0x00); // Enable acceleration- and gyrosensor
    icm42688_write_register(REG_ACCEL_CONFIG0, 0x0E); // Set accelerometer to low noise mode, 1.125kHz, ±4g
    icm42688_write_register(REG_GYRO_CONFIG0, 0x0E); // Set gyroscope to low noise mode, 1.125kHz, ±2000dps
}

// Function to read sensor data and calculate motion and orientation
int8_t evaluate_motion_and_orientation() {
    // Read acceleration data
    uint8_t direction = 0;
    int8_t overlay_pitchroll = get_value_from_nvs("control_sensivity");

    if (!overlay_pitchroll) {overlay_pitchroll = -15;}

    uint8_t accel_x_h = icm42688_read_register(REG_ACCEL_XOUT_H);
    uint8_t accel_x_l = icm42688_read_register(REG_ACCEL_XOUT_L);
    uint8_t accel_y_h = icm42688_read_register(REG_ACCEL_YOUT_H);
    uint8_t accel_y_l = icm42688_read_register(REG_ACCEL_YOUT_L);
    uint8_t accel_z_h = icm42688_read_register(REG_ACCEL_ZOUT_H);
    uint8_t accel_z_l = icm42688_read_register(REG_ACCEL_ZOUT_L);

    int16_t accel_x = (accel_x_h << 8) | accel_x_l;
    int16_t accel_y = (accel_y_h << 8) | accel_y_l;
    int16_t accel_z = (accel_z_h << 8) | accel_z_l;

    // Read gyro data
    uint8_t gyro_x_h = icm42688_read_register(REG_GYRO_XOUT_H);
    uint8_t gyro_x_l = icm42688_read_register(REG_GYRO_XOUT_L);
    uint8_t gyro_y_h = icm42688_read_register(REG_GYRO_YOUT_H);
    uint8_t gyro_y_l = icm42688_read_register(REG_GYRO_YOUT_L);
    uint8_t gyro_z_h = icm42688_read_register(REG_GYRO_ZOUT_H);
    uint8_t gyro_z_l = icm42688_read_register(REG_GYRO_ZOUT_L);

    int16_t gyro_x = (gyro_x_h << 8) | gyro_x_l;
    int16_t gyro_y = (gyro_y_h << 8) | gyro_y_l;
    int16_t gyro_z = (gyro_z_h << 8) | gyro_z_l;

    // Convert raw acceleration data to g's
    float ax = accel_x / 4096.0; // Assuming ±4g range
    float ay = accel_y / 4096.0;
    float az = accel_z / 4096.0;

    // Calculate roll and pitch (in degrees)
    float roll = atan2(ay, az) * 180.0 / M_PI;
    float pitch = atan2(-ax, sqrt(ay * ay + az * az)) * 180.0 / M_PI;

    if (abs(roll) > abs(pitch)) {
        if (roll > abs(overlay_pitchroll)) {direction = 1; } 
        else if (roll < overlay_pitchroll) {direction = 3; } 
        else {direction = 0; }
    } else {
        if (pitch > abs(overlay_pitchroll)) {direction = 2; } 
        else if (pitch < overlay_pitchroll) {direction = 4; } 
        else {direction = 0; }
    }

    // Special function to leave snake-game on z-axis acceleration
    if (accel_z > Z_ACCEL_RECOGNIZE) {
        load_screen_matrix();
        device_menu_mode();
    }

    return direction;
}