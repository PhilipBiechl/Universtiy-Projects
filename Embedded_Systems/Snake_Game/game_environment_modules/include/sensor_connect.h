//****************************************************************************************//
//  Author:     Philip Biechl                                                             //
//  Project:    Embedded Systems - Snake Game                                             //
//  Place:      Game_Environment_Modules / Include                                        //
//****************************************************************************************//

void spi_init(void);
void icm42688_init(void);
void icm42688_write_register(uint8_t reg, uint8_t data);
uint8_t icm42688_read_register(uint8_t reg);
int8_t evaluate_motion_and_orientation(void);