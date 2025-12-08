/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#include "../include/server_init.h"

/* initalise webserver with uri handlers from file handler */
static httpd_handle_t start_webserver(void) {
    httpd_config_t config = HTTPD_DEFAULT_CONFIG();

    httpd_handle_t server = NULL;
    if (httpd_start(&server, &config) == ESP_OK) {
        httpd_uri_t index_uri = {
            .uri = "/",
            .method = HTTP_GET,
            .handler = index_get_handler,
            .user_ctx = NULL
        };
        httpd_register_uri_handler(server, &index_uri);

        httpd_uri_t data_uri = {
            .uri = "/data",
            .method = HTTP_GET,
            .handler = data_rcv_handler,
            .user_ctx = NULL
        };
        httpd_register_uri_handler(server, &data_uri);

        httpd_uri_t get_gSimMode = {
            .uri = "/gSimMode",
            .method = HTTP_GET,
            .handler = get_gSimMode_status,
            .user_ctx = NULL
        };
        httpd_register_uri_handler(server, &get_gSimMode);

        httpd_uri_t toggle_reg = {
            .uri = "/reg",
            .method = HTTP_GET,
            .handler = toggle_regulation_mode_handler,
            .user_ctx = NULL
        };
        httpd_register_uri_handler(server, &toggle_reg);

        httpd_uri_t toggle_sim = {
            .uri = "/sim",
            .method = HTTP_GET,
            .handler = toggle_simulation_mode_handler,
            .user_ctx = NULL
        };
        httpd_register_uri_handler(server, &toggle_sim);

        httpd_uri_t style_css = {
            .uri       = "/style.css",
            .method    = HTTP_GET,
            .handler   = style_css_get_handler,
            .user_ctx  = NULL
        };
        httpd_register_uri_handler(server, &style_css);

        httpd_uri_t script_js = {
            .uri       = "/script.js",
            .method    = HTTP_GET,
            .handler   = script_js_get_handler,
            .user_ctx  = NULL
        };
        httpd_register_uri_handler(server, &script_js);

        httpd_uri_t chart_js = {
            .uri       = "/chart.js",
            .method    = HTTP_GET,
            .handler   = chart_js_get_handler,
            .user_ctx  = NULL
        };
        httpd_register_uri_handler(server, &chart_js);

        httpd_uri_t submit_post_uri = {
            .uri = "/submit",
            .method = HTTP_POST,
            .handler = submit_post_handler,
            .user_ctx = NULL,
        };
        httpd_register_uri_handler(server, &submit_post_uri);

        return server;
    }

    ESP_LOGE(TAG, "Server could not be started");
    return NULL;
}

/* initialise file system */
void init_spiffs(void) {
    esp_vfs_spiffs_conf_t conf = {
        .base_path = "/spiffs",       
        .partition_label = NULL,      
        .max_files = 5,               
        .format_if_mount_failed = true 
    };

    esp_err_t ret = esp_vfs_spiffs_register(&conf);

    if (ret != ESP_OK) {
        if (ret == ESP_FAIL) {
            ESP_LOGE("SPIFFS", "Failed to mount or format filesystem");
        } else if (ret == ESP_ERR_NOT_FOUND) {
            ESP_LOGE("SPIFFS", "Failed to find SPIFFS partition");
        } else if (ret == ESP_ERR_INVALID_ARG) {
            ESP_LOGE("SPIFFS", "Invalid argument (check configuration)");
        } else {
            ESP_LOGE("SPIFFS", "Failed to initialize SPIFFS (%s)", esp_err_to_name(ret));
        }
        return;
    }

    size_t total = 0, used = 0;
    ret = esp_spiffs_info(NULL, &total, &used);
    if (ret == ESP_OK) {
        ESP_LOGI("SPIFFS", "Partition size: total: %d, used: %d", total, used);
    } else {
        ESP_LOGE("SPIFFS", "Failed to get SPIFFS partition information (%s)", esp_err_to_name(ret));
    }
}

/* start wifi broadcast */
void wifi_init_softap(void) {
    esp_netif_init(); 
    esp_event_loop_create_default(); 
    esp_netif_create_default_wifi_ap(); 

    wifi_init_config_t cfg = WIFI_INIT_CONFIG_DEFAULT();
    ESP_ERROR_CHECK(esp_wifi_init(&cfg));

    wifi_config_t wifi_config = {
        .ap = {
            .ssid = "Temp_Ctrl",
            .ssid_len = strlen("Temp_Ctrl"),
            .password = "12345678",
            .max_connection = 4,
            .authmode = WIFI_AUTH_WPA_WPA2_PSK,
        },
    };
    if (strlen("12345678") == 0) {
        wifi_config.ap.authmode = WIFI_AUTH_OPEN;
    }

    ESP_ERROR_CHECK(esp_wifi_set_mode(WIFI_MODE_AP)); 
    ESP_ERROR_CHECK(esp_wifi_set_config(ESP_IF_WIFI_AP, &wifi_config)); 
    ESP_ERROR_CHECK(esp_wifi_start()); 
}

/* start the server from here */
void server_main() {
    gServer = NULL; // Safety-function
    
    double desired_value = 0.0;
    double current_value = 0.0;

    PID_Init(&pid, PID_KP, PID_KI, PID_KD, desired_value, current_value, PID_T, MIN_PID, MAX_PID);
    
    gServer = start_webserver();
}