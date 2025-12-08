//****************************************************************************************//
//  Author:     Philip Biechl                                                             //
//  Project:    Embedded Systems - Snake Game                                             //
//  Place:      Main                                                                      //
//****************************************************************************************//

#include <unistd.h>

// Include Headers
#include "../game_environment_modules/include/game_control.h"
#include "../game_environment_modules/include/matrix_control.h"
#include "../game_environment_modules/include/menu_control.h"
#include "../game_environment_modules/include/nvs_storage_connect.h"
#include "../game_environment_modules/include/sensor_connect.h"

void app_main(void) {
    // Initalise the peripheral modules
    configure_led();
    spi_init();
    icm42688_init();
    nvs_init();

    // Start the game environment with startup animation
    startup();
}