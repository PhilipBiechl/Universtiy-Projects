//****************************************************************************************//
//  Author:     Philip Biechl                                                             //
//  Project:    Embedded Systems - Snake Game                                             //
//  Place:      Game_Environment_Modules                                                  //
//****************************************************************************************//

#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <unistd.h>
#include "driver/gpio.h"
#include "driver/spi_master.h"
#include "led_strip.h"
#include "esp_system.h"

// Include Headers
#include "include/sensor_connect.h"
#include "include/game_control.h"
#include "include/menu_control.h"
#include "include/led_symbols.h"

// TAG for ESP-LOGI commands
#define TAG "ICM42688"

// LED Matrix Pin
#define BLINK_GPIO                  8

// Length of array function
#define ARRLEN(x)                   (&x)[1] - x 

// Function to initialise LED
void configure_led() {
    led_strip_config_t strip_config = {
        .strip_gpio_num = BLINK_GPIO,
        .max_leds = 25,
    };
#if CONFIG_BLINK_LED_STRIP_BACKEND_RMT
    led_strip_rmt_config_t rmt_config = {
        .resolution_hz = 10 * 1000 * 1000, // 10MHz
        .flags.with_dma = false,
    };
    ESP_ERROR_CHECK(led_strip_new_rmt_device(&strip_config, &rmt_config, &led_strip));
#elif CONFIG_BLINK_LED_STRIP_BACKEND_SPI
    led_strip_spi_config_t spi_config = {
        .spi_bus = SPI2_HOST,
        .flags.with_dma = true,
    };
    ESP_ERROR_CHECK(led_strip_new_spi_device(&strip_config, &spi_config, &led_strip));
#endif
    led_strip_clear(led_strip);
}

// Function directly displays all pixels in a array on LED-Matrix 
void led_strip_show(int8_t pixelMap[], uint8_t len, uint32_t colorMap[]) {
    int32_t color_arr = 1;
    color_arr *= 3;
    for (uint8_t i = 0; i < len; i++) {
        if (pixelMap[i] >= 0 && pixelMap[i] < 25) {
            led_strip_set_pixel(led_strip, pixelMap[i], colorMap[0], colorMap[1], colorMap[2]);
        }
    }
}

// LED-Matrix startup animation
void startup_matrix() {
    int8_t startup_pos[3] = {12, 7, 2};

    led_strip_clear(led_strip);
    led_strip_show(startup_pos, ARRLEN(startup_pos), colorMap_x[0]);
    led_strip_refresh(led_strip);

    // Change pixel position for rotation animation
    for (int8_t i = 0; i < 24; i++)
    {
        switch (i)
        {
        case 0:
            startup_pos[2] += 1;
            break;
        case 1:
            startup_pos[1] += 1;
            break;
        case 2:
            startup_pos[2] += 1;
            break;
        case 3:
            startup_pos[2] += 5;
            break;
        case 4:
            startup_pos[1] += 5;
            break;
        case 5:
            startup_pos[2] += 5;
            break;
        case 6:
            startup_pos[2] += 5;
            break;
        case 7:
            startup_pos[1] += 5;
            break;
        case 8:
            startup_pos[2] += 5;
            break;
        case 9:
            startup_pos[2] -= 1;
            break;
        case 10:
            startup_pos[1] -= 1;
            break;
        case 11:
            startup_pos[2] -= 1;
            break;
        case 12:
            startup_pos[2] -= 1;
            break;
        case 13:
            startup_pos[1] -= 1;
            break;
        case 14:
            startup_pos[2] -= 1;
            break;
        case 15:
            startup_pos[2] -= 5;
            break;
        case 16:
            startup_pos[1] -= 5;
            break;
        case 17:
            startup_pos[2] -= 5;
            break;
        case 18:
            startup_pos[2] -= 5;
            break;
        case 19:
            startup_pos[1] -= 5;
            break;
        case 20:
            startup_pos[2] -= 5;
            break;
        case 21:
            startup_pos[2] += 1;
            break;
        case 22:
            startup_pos[1] += 1;
            break;
        case 23:
            startup_pos[2] += 1;
            break;
        default:
            break;
        }

        vTaskDelay(150 / (i+1));
        
        led_strip_clear(led_strip);
        led_strip_show(startup_pos, ARRLEN(startup_pos), colorMap_x[0]);
        led_strip_refresh(led_strip);
    }
}

// Loading screen animation
void load_screen_matrix() {
    int8_t loading_pos[] = {0,1,2,3,4};

    led_strip_clear(led_strip);
    led_strip_show(loading_pos, ARRLEN(loading_pos), colorMap_x[0]);
    led_strip_refresh(led_strip);

    vTaskDelay(100 / 1);
    
    // Change pixel positions vertically down
    for (int8_t i = 0; i < 5; i++)
    {
        led_strip_clear(led_strip);
        led_strip_show(loading_pos, ARRLEN(loading_pos), colorMap_x[0]);

        for (int8_t j = 0; j < 5; j++)
        {
            loading_pos[j] += 5;
            if (loading_pos[j] > 24) {break;}
        }
        
        led_strip_show(loading_pos, ARRLEN(loading_pos), colorMap_x[0]);
        led_strip_refresh(led_strip);

        vTaskDelay(500 / (portTICK_PERIOD_MS + 10* i));
    }
}

// Full on-initialisation animation and primary call of menu-function
void startup() {
    // Startup animation
    startup_matrix();
    vTaskDelay(250 / portTICK_PERIOD_MS);

    // First initial 'p'
    led_strip_clear(led_strip);
    led_strip_show(pixel_p, ARRLEN(pixel_p), colorMap_x);
    led_strip_refresh(led_strip);
    vTaskDelay(500 / portTICK_PERIOD_MS);

    // Second initial 'b'
    led_strip_clear(led_strip);
    led_strip_show(pixel_b, ARRLEN(pixel_b), colorMap_x);
    led_strip_refresh(led_strip);
    vTaskDelay(500 / portTICK_PERIOD_MS);

    // Logo display
    led_strip_clear(led_strip);
    led_strip_show(pixel_vq, ARRLEN(pixel_vq), colorMap_x);
    led_strip_refresh(led_strip);
    vTaskDelay(500 / portTICK_PERIOD_MS);

    // Start the menu and full environment
    device_menu_mode();
}