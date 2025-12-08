/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#include "../include/server_data.h"
/* data to be accessed in all files */

httpd_handle_t gServer = NULL;

char* device_name = "ESP32C3";
char* gSSID = "Temp_Ctrl";
char* gPW = "12345678";

float gSimTemp = 0.0f;

int8_t gRegulationMode = 0;
int8_t gSimMode = 0;

float gTemp = 0.0f;
float gHum = 0.0f;
float gSoll = 0.0f;
float gFinal = 0.0f;