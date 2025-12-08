//****************************************************************************************//
//  Author:     Philip Biechl                                                             //
//  Project:    Embedded Systems - Snake Game                                             //
//  Place:      Game_Environment_Modules / Include                                        //
//****************************************************************************************//

#include <unistd.h>
#include "led_strip.h"

// Variables to fix LED-Matrix positions and colors
uint32_t colorMap_snake[5][3] = {
    {16,16,16}, {250,50,50}, {50,20,50}, {16,16,16}, {16,16,16}
};
uint8_t color_target[] = {150, 150, 16};
uint8_t color_snake_head[] = {100, 0, 100};
uint32_t colorMap_x[5][3] = {
    {16,16,16}, {250,50,50}, {50,20,50}, {16,16,16}, {16,16,16}
};

// LED-Matrix handle
led_strip_handle_t led_strip;

//LED-Matrix symbols
int8_t pixel_x[] = {0,4,6,8,12,16,18,20,24};
int8_t pixel_x_pos0[] = {1,2,3,7};
int8_t pixel_x_pos1[] = {1,2,3,7,9,13,14,19};
int8_t pixel_x_pos2[] = {1,2,3,7,9,13,14,19,17,21,22,23};
int8_t pixel_x_pos3[] = {1,2,3,7,9,13,14,19,17,21,22,23,5,10,11,15};
int8_t pixel_p[] = {1,2,3,6,8,11,12,13,16,21};
int8_t pixel_b[] = {1,6,11,12,13,16,18,21,22,23};
int8_t pixel_vq[] = {1,2,3,4,5,7,8,9,10,11,15,16,20,21};

// Menu symbols
int8_t pixel_menu_a[] = {1,6,7,11,13,16,17,21};                         // Game
int8_t pixel_menu_b[] = {1,6,7,8,13,17,18,19,23};                       // Settings (difficulty)
int8_t pixel_menu_c[] = {0,2,4,6,7,8,10,11,13,14,16,17,18,20,22,24};    // Settings (controls)
int8_t pixel_menu_d[] = {0,1,2,3,10,11,12,20,21,22};                    // Info (high-score)
int8_t pixel_menu_e[] = {5,8,11,14,15,18};                              // Info (console)