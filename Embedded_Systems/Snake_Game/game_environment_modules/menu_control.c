//****************************************************************************************//
//  Author:     Philip Biechl                                                             //
//  Project:    Embedded Systems - Snake Game                                             //
//  Place:      Game_Environment_Modules / Include                                        //
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
#include "esp_random.h"
#include "esp_system.h"
#include "esp_log.h"

// Include Headers
#include "include/sensor_connect.h"
#include "include/nvs_storage_connect.h"
#include "include/matrix_control.h"
#include "include/game_control.h"
#include "include/led_symbols.h"

// TAG for ESP-LOGI commands
#define TAG "ICM42688"                      

#define MOTION_OUT                  20      // Time in which motion-functions will be deactivated after motion command
#define MOTION_IN                   0       // Time-Value for reactivaton motion functions
#define MOTION_TIMEOUT              15      // Time for no motion detection directly after loading menu
#define INITIAL_MENU_VALUE          0       // Standard menu position on load
#define MAX_TURN_ANGLE              -70     // Maximal angle to adjust minimum of recognised turning
#define MIN_TURN_ANGLE              -10     // Minimal angle to adjust minimum of recognised turning
#define ANGLE_SPACING               (abs(MAX_TURN_ANGLE - MIN_TURN_ANGLE) / 4) // Steps to change angle minimum
 
// Length of array function
#define ARRLEN(x)                   (&x)[1] - x 

// Decalration of main menu function
void device_menu_mode(void);

// Sets LED-Matrix symbol to current menu item
void device_menu_refresh(int8_t menu_state) {
    led_strip_clear(led_strip);

    switch ((int)menu_state)
    {
    case 0:
        led_strip_show(pixel_menu_a, ARRLEN(pixel_menu_a), colorMap_x[0]);   
        break;
    case 1:
        led_strip_show(pixel_menu_b, ARRLEN(pixel_menu_b), colorMap_x[0]);
        break;
    case 2:
        led_strip_show(pixel_menu_c, ARRLEN(pixel_menu_c), colorMap_x[0]);
        break;
    case 3:
        led_strip_show(pixel_menu_d, ARRLEN(pixel_menu_d), colorMap_x[0]);
        break;
    case 4:
        led_strip_show(pixel_menu_e, ARRLEN(pixel_menu_e), colorMap_x[0]);
        break;
    default:
        menu_state = 0;
        break;
    }

    led_strip_refresh(led_strip);
}

// Sets LED-Matrix symbol to display current value 
void settings_refresh(int8_t menu_state) {
    led_strip_clear(led_strip);
    led_strip_show(pixel_x, ARRLEN(pixel_x), colorMap_x[0]);

    switch ((int)menu_state)
    {
    case 0:
        break;
    case 1:
        led_strip_show(pixel_x_pos0, ARRLEN(pixel_x_pos0), colorMap_x[0]);
        break;
    case 2:
        led_strip_show(pixel_x_pos1, ARRLEN(pixel_x_pos1), colorMap_x[0]);
        break;
    case 3:
        led_strip_show(pixel_x_pos2, ARRLEN(pixel_x_pos2), colorMap_x[0]);
        break;
    case 4:
        led_strip_show(pixel_x_pos3, ARRLEN(pixel_x_pos3), colorMap_x[0]);
        break;
    default:
        menu_state = 0;
        break;
    }

    led_strip_refresh(led_strip);
}

// Function to load and set difficulty for the snake-game
void settings_difficulty() {
    // Motion active to recognise only one motion-command at a time
    int8_t motionActive = MOTION_TIMEOUT;
    int8_t difficulty = get_value_from_nvs("difficulty");
    settings_refresh(difficulty);

    // menu-point loop
    while (1) {
        if (motionActive < MOTION_IN) {
            /* Back or up orientation -> save and back to main menu
               right -> value +1 | left -> value -1 */
            if (evaluate_motion_and_orientation() && evaluate_motion_and_orientation() % 2 != 0) {
                save_value_to_nvs("difficulty", difficulty);
                ESP_LOGI(TAG, "Difficulty: %d", difficulty);
                device_menu_mode();
            } else if (evaluate_motion_and_orientation() == 2) {
                motionActive = MOTION_OUT;
                difficulty += 1;
                if (difficulty > 4) {difficulty = 0;}
                settings_refresh(difficulty);
            } else if (evaluate_motion_and_orientation() == 4) {
                motionActive = MOTION_OUT;
                difficulty -= 1;
                if (difficulty < 0) {difficulty = 4;}
                settings_refresh(difficulty);
            }
        } else {
            // Reset motion timeout
            motionActive--;
        }

        vTaskDelay(50 / portTICK_PERIOD_MS);
    }
}

// Function to load and set control sensitivity
void settings_controls() {
    // Motion active to recognise only one motion-command at a time
    int8_t motionActive = MOTION_TIMEOUT;
    int8_t control_sensitivity = get_value_from_nvs("control_sensitivity");
    settings_refresh((abs(control_sensitivity) - 10) / 15);

    while (1) {
        if (motionActive < MOTION_IN) {
            /* Back or up orientation -> save and back to main menu
               right -> value +15 | left -> value -15 (values are negative) */
            if (evaluate_motion_and_orientation() && evaluate_motion_and_orientation() % 2 != 0) {
                save_value_to_nvs("control_sensitivity", control_sensitivity);
                ESP_LOGI(TAG, "sensitivity: %d", control_sensitivity);
                device_menu_mode();
            } else if (evaluate_motion_and_orientation() == 2) {
                motionActive = MOTION_OUT;
                control_sensitivity -= ANGLE_SPACING;
                if (control_sensitivity < MAX_TURN_ANGLE) {control_sensitivity = MIN_TURN_ANGLE;}
                settings_refresh((abs(control_sensitivity) - 10) / 15);
            } else if (evaluate_motion_and_orientation() == 4) {
                motionActive = MOTION_OUT;
                control_sensitivity += ANGLE_SPACING;
                if (control_sensitivity > MIN_TURN_ANGLE) {control_sensitivity = MAX_TURN_ANGLE;}
                settings_refresh((abs(control_sensitivity) - 10) / 15);
            }
        } else {
            // Reset motion timeout
            motionActive--;
        }

        vTaskDelay(50 / portTICK_PERIOD_MS);
    }
}

// Function to load high score and print as LED-Stripe
void info_highscore() {
    // Loading difficulty to get current high score
    int8_t difficulty = get_value_from_nvs("difficulty");
    char score_difficulty[] = "highscore";
    char diff_string[5];
    sprintf(diff_string, "%d", difficulty); // Convert integer to string
    strcat(score_difficulty, diff_string);
    int8_t highscore = get_value_from_nvs(score_difficulty);

    // Display high score value with animation
    led_strip_clear(led_strip);
    for (int8_t i = 0; i < highscore; i++) {
        led_strip_set_pixel(led_strip, i, colorMap_x[0], colorMap_x[1], colorMap_x[2]);
        led_strip_refresh(led_strip);
        vTaskDelay(500 / portTICK_PERIOD_MS + i);
    }
    
    vTaskDelay(1000 / portTICK_PERIOD_MS);

    // Back to main menu
    if (evaluate_motion_and_orientation()) {
        device_menu_mode();
    }
}

// Function to print all high score and settings data
void info_all() {
    printf("\nSpieldaten:\n--------------------------------------------------\n\n");
    printf("High Score (Level 0):\t\t\t%d\n", (int)get_value_from_nvs("highscore0"));
    printf("High Score (Level 1):\t\t\t%d\n", (int)get_value_from_nvs("highscore1"));
    printf("High Score (Level 2):\t\t\t%d\n", (int)get_value_from_nvs("highscore2"));
    printf("High Score (Level 3):\t\t\t%d\n", (int)get_value_from_nvs("highscore3"));
    printf("High Score (Level 4):\t\t\t%d\n", (int)get_value_from_nvs("highscore4"));
    printf("\n--------------------------------------------------\n\n");
    printf("Current difficulty (0-4):\t\t%d\n", (int)get_value_from_nvs("difficulty"));
    printf("Current control sensitivity (0-4):\t%d\n\n", (int)get_value_from_nvs("control_sensitivity"));

}

// Function to call specific functions based on current menu position
void menu_selection(int8_t menu_selection) {
    load_screen_matrix();
    switch ((int)menu_selection)
    {
    case 0: 
        init_snake_game();
        break;
    case 1:
        settings_difficulty();
        break;
    case 2:
        settings_controls();
        break;
    case 3:
        info_highscore();
        break;
    case 4:
        info_all();
        break;
    default:
        menu_selection = 0;
        break;
    }
}

// Main menu for the game environment
void device_menu_mode() {
    // Motion active to recognise only one motion-command at a time
    int8_t menu_state = INITIAL_MENU_VALUE;
    int8_t motionActive = MOTION_TIMEOUT;
    device_menu_refresh(menu_state);

    // Main loop for the main menu
    while (1) {
        if (motionActive < MOTION_IN) {
            /* Back or up orientation -> select and run current menu point
               right -> next option | left -> last option */
            if (evaluate_motion_and_orientation() && evaluate_motion_and_orientation() % 2 != 0) {
                motionActive = MOTION_OUT;
                menu_selection(menu_state);
            } else if (evaluate_motion_and_orientation() == 2) {
                motionActive = MOTION_OUT;
                menu_state += 1;
                if (menu_state > 4) {menu_state = 0;}
                device_menu_refresh(menu_state);
            } else if (evaluate_motion_and_orientation() == 4) {
                motionActive = MOTION_OUT;
                menu_state -= 1;
                if (menu_state < 0) {menu_state = 4;}
                device_menu_refresh(menu_state);
            }
        } else {
            // Reset motion timeout
            motionActive--;
        }

        vTaskDelay(50 / portTICK_PERIOD_MS);
    }    
}