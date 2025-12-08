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
#include "esp_random.h"
#include "esp_system.h"
#include "esp_log.h"

// Include Headers
#include "include/sensor_connect.h"
#include "include/nvs_storage_connect.h"
#include "include/matrix_control.h"
#include "include/menu_control.h"
#include "include/led_symbols.h"

// TAG for ESP-LOGI commands
#define TAG "ICM42688"      

// Length of array function
#define ARRLEN(x)                   (&x)[1] - x 

// target position, snake head and game level at game initialisation
#define TARGET_PRIMARY              0 
#define INIT_GAME_LEVEL             0
#define SNAKE_INIT_POS              12

// Registers to genereate random numbers
#define RNG_BASE                    0x60026000
#define RNG_DATA_REG_OFFS           0xB0

// Game environment variables
int8_t game_level = 0;              // counts, how many targets have been collected, affects snake length and speed
int8_t target_pos = TARGET_PRIMARY; // poisition for the target, generated with RNG
int8_t snake_pos[24] = {0};         // array to store snake positions
int8_t direction = 3;               // direction for the next move of the snake

// Register for RNG (random numbers) as volatile to secure different numbers at multiple read commands
volatile uint32_t* rng_reg = (volatile uint32_t*)(RNG_BASE | RNG_DATA_REG_OFFS);

// Get the target for snake-game if needed
int8_t get_snake_target() {
    int8_t target_clear = 0;

    /* if the snake head is on the target position a new random target 
       (that does not match any of the snakes positions) will be generated */
    if (target_pos == snake_pos[0]) {
        do {
            target_pos = (*rng_reg % 25);
            target_clear = 1;
            for (int i = 0; i < ARRLEN(snake_pos); i++) {
                if(target_pos == snake_pos[i]) {
                    target_clear = 0; 
                }
            }
        } while (target_clear != 1);

        game_level += 1;
    }

	return target_pos;
}

// Reaction to snake head touching the snake body - checked after every move
void snake_move_analysis() {
    // load difficulty data to load previous high score
    int8_t difficulty = get_value_from_nvs("difficulty");
    char score_difficulty[20] = "highscore";
    char diff_string[5];
    sprintf(diff_string, "%d", difficulty); // convert integer to string
    strcat(score_difficulty, diff_string);
    int8_t highscore = get_value_from_nvs(score_difficulty);
    
    // End the game if condition is true and save new high score if there is one
    for (int8_t i = 1; i < ARRLEN(snake_pos); i++) {
        if ((snake_pos[0] == snake_pos[i]) && (snake_pos[i] != -1)) {
            if (game_level > highscore) {save_value_to_nvs(score_difficulty, game_level);}
            load_screen_matrix(); // lost anim
            device_menu_mode();
        }
    }
}

// Function to keep the snake running while game is on
void led_snake() {
    int8_t head_before = snake_pos[0];
    
    // Move head position down to body - body positions back, as long as snake is (depends on game level)
    for (int i = game_level; i >= 0; i--) {
        snake_pos[i+1] = snake_pos[i];
    }

    // If direction is given and is not equal with the direction the snake is coming from - change to new value
    if(evaluate_motion_and_orientation() && abs(evaluate_motion_and_orientation() - direction) != 2) {
        direction = evaluate_motion_and_orientation();
    }

    /* Changes snake head positon on given direction - on leaving the game-field 
       position will be reseted to oposite side of field
       Directions: 1 down | 2 right | 3 up | 4 left */
    switch (direction) 
    {
    case 1:
        if(head_before > 19) {
            snake_pos[0] = head_before - 20;
        } else {
            snake_pos[0] = head_before + 5;
        }
        break;
    case 2:
        if((head_before + 1) % 5 == 0) {
            snake_pos[0] = head_before - 4;
        } else {
            snake_pos[0] = head_before + 1;
        }
        break;
    case 3:
        if(head_before < 5) { 
            snake_pos[0] = head_before + 20;
        } else {
            snake_pos[0] = head_before - 5;
        }
        break;
    case 4:
        if((head_before + 5) % 5 == 0) { 
            snake_pos[0] = head_before + 4;
        } else {
            snake_pos[0] = head_before - 1;
        }
        break;
    default: 
        ESP_LOGI(TAG, "Error - direction value \'%d\' cannot be processed", direction);
        break;
    }

    // Check losing conditions
    snake_move_analysis();

    // Set new pixels - target, snake and snake-head
    led_strip_clear(led_strip);
    led_strip_show(snake_pos, ARRLEN(snake_pos), colorMap_snake[0]);
    led_strip_set_pixel(led_strip, snake_pos[0], color_snake_head[0], color_snake_head[1], color_snake_head[2]);
    led_strip_set_pixel(led_strip, get_snake_target(), color_target[0], color_target[1], color_target[2]);
    led_strip_refresh(led_strip);
}

// Initialises game and calls led_snake function
void init_snake_game() {
    game_level = INIT_GAME_LEVEL;
    int8_t difficulty = get_value_from_nvs("difficulty");

    // Not active snake_pos values on '-1' to differ from actual positions like '0'
    for (int i = 0; i < ARRLEN(snake_pos); i++) {
        snake_pos[i] = -1;
    }
    // Starting position for snake head
    snake_pos[0] = SNAKE_INIT_POS;

    // Show initial game positions on LED-Matrix
    led_strip_clear(led_strip);
    led_strip_show(snake_pos, ARRLEN(snake_pos), colorMap_snake[0]);
    led_strip_set_pixel(led_strip, get_snake_target(), color_target[0], color_target[1], color_target[2]);
    led_strip_refresh(led_strip);

    // Main game loop
    while (1) {
        vTaskDelay(1000 / (portTICK_PERIOD_MS + game_level * difficulty * 0.5));
        led_snake();
    }
}