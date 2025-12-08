/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#ifndef SERVER_DATA_H
#define SERVER_DATA_H

#include "esp_http_server.h"

extern char* device_name;
extern char* gSSID;
extern char* gPW;

extern httpd_handle_t gServer;

extern int8_t gRegulationMode;
extern int8_t gSimMode;

extern float gSimTemp;
extern float gTemp;
extern float gHum;
extern float gSoll;
extern float gFinal;

#endif // server_data.h