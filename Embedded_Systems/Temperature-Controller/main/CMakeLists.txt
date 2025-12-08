set(requires "")
idf_build_get_property(target IDF_TARGET)

if(${target} STREQUAL "linux")
    list(APPEND requires esp_stubs esp-tls esp_http_server protocol_examples_common nvs_flash)
endif()
idf_component_register(SRCS "main.c" "controller/startup.c" "controller/temperature_control/data_control.c" "controller/temperature_control/controller.c" "controller/server_control/file_handler.c" "controller/server_control/server_data.c" "controller/server_control/server_init.c" "controller/peripheral_drivers/shtc3.c" "controller/peripheral_drivers/adc_i2c.c" "controller/include/startup.h" "controller/include/data_control.h" "controller/include/controller.h" "controller/include/file_handler.h" "controller/include/server_data.h" "controller/include/server_init.h" "controller/include/shtc3.h" "controller/include/adc_i2c.h"
                    INCLUDE_DIRS "." "../spiffs" "controller" "controller/include" "controller/peripheral_drivers" "controller/server_control" "controller/temperature_control"
                    EMBED_TXTFILES "../spiffs/index.html" "../spiffs/style.css" "../spiffs/script.js" "../spiffs/chart.js"
                    REQUIRES ${requires})