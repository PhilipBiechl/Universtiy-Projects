//****************************************************************************************//
//  Author:     Philip Biechl                                                             //
//  Project:    Embedded Systems - Snake Game                                             //
//  Place:      Game_Environment_Modules / Include                                        //
//****************************************************************************************//

#include <unistd.h>
#include "led_strip.h"

// Variables to fix LED-Matrix positions and colors
extern uint32_t colorMap_snake[5][3];
extern uint8_t color_target[3];
extern uint8_t color_snake_head[3];
extern uint32_t colorMap_x[5][3];

// LED-Matrix handle
extern led_strip_handle_t led_strip;

//LED-Matrix symbols
extern int8_t pixel_x[9];
extern int8_t pixel_x_pos0[4];
extern int8_t pixel_x_pos1[8];
extern int8_t pixel_x_pos2[12];
extern int8_t pixel_x_pos3[16];
extern int8_t pixel_p[10];
extern int8_t pixel_b[10];
extern int8_t pixel_vq[14];

// Menu symbols
extern int8_t pixel_menu_a[8];                         
extern int8_t pixel_menu_b[9];                      
extern int8_t pixel_menu_c[16];    
extern int8_t pixel_menu_d[10];               
extern int8_t pixel_menu_e[6];                      