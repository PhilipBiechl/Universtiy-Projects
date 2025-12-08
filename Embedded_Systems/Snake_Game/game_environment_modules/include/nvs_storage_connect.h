//****************************************************************************************//
//  Author:     Philip Biechl                                                             //
//  Project:    Embedded Systems - Snake Game                                             //
//  Place:      Game_Environment_Modules / Include                                        //
//****************************************************************************************//

void nvs_init(void);
void save_value_to_nvs(const char* key, int32_t value);
int32_t get_value_from_nvs(const char* key);