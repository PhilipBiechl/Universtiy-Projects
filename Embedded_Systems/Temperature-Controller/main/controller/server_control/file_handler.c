/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#include "../include/file_handler.h"

/* ctrl value for connection-state */
int8_t ctrl_cnt = 0;

/* load index.html */
esp_err_t index_get_handler(httpd_req_t *req)
{
    FILE* file = fopen("/spiffs/index.html", "r");
    if (!file) {
        httpd_resp_send_404(req);
        return ESP_FAIL;
    }

    char buffer[1024];
    size_t bytesRead = 0;
    while ((bytesRead = fread(buffer, 1, sizeof(buffer), file)) > 0) {
        httpd_resp_send_chunk(req, buffer, bytesRead);
    }
    fclose(file);
    
    httpd_resp_send_chunk(req, NULL, 0);
    return ESP_OK;
}

/* load style.css */
esp_err_t style_css_get_handler(httpd_req_t *req)
{
    FILE* file = fopen("/spiffs/style.css", "r");
    if (!file) {
        httpd_resp_send_404(req);
        return ESP_FAIL;
    }

    char buffer[1024];
    size_t bytesRead = 0;
    while ((bytesRead = fread(buffer, 1, sizeof(buffer), file)) > 0) {
        httpd_resp_send_chunk(req, buffer, bytesRead);
    }
    fclose(file);
    
    httpd_resp_send_chunk(req, NULL, 0);
    return ESP_OK;
}

/* load script.js */
esp_err_t script_js_get_handler(httpd_req_t *req)
{
    FILE* file = fopen("/spiffs/script.js", "r");
    if (!file) {
        httpd_resp_send_404(req);
        printf("This is where we fail");
        return ESP_FAIL;
    }

    char buffer[1024];
    size_t bytesRead = 0;
    while ((bytesRead = fread(buffer, 1, sizeof(buffer), file)) > 0) {
        httpd_resp_send_chunk(req, buffer, bytesRead);
    }
    fclose(file);
    
    httpd_resp_send_chunk(req, NULL, 0);
    return ESP_OK;
}

/* load chart.js - open-source code */
esp_err_t chart_js_get_handler(httpd_req_t *req)
{
    FILE* file = fopen("/spiffs/chart.js", "r");
    if (!file) {
        httpd_resp_send_404(req);
        printf("This is where we fail");
        return ESP_FAIL;
    }

    char buffer[1024];
    size_t bytesRead = 0;
    while ((bytesRead = fread(buffer, 1, sizeof(buffer), file)) > 0) {
        httpd_resp_send_chunk(req, buffer, bytesRead);
    }
    fclose(file);
    
    httpd_resp_send_chunk(req, NULL, 0);
    return ESP_OK;
}

/* sends data updates to webpage */
esp_err_t data_rcv_handler(httpd_req_t *req) {
    ctrl_cnt = ctrl_cnt > 100 ? 0 : ctrl_cnt + 1;
    
    httpd_resp_set_type(req, "text/plain");
    char responsebody[100] = "string";
    sprintf(responsebody, "%lf, %lf, %lf, %lf, %d, %d, %s, %s, %d, %lf, %lf", gTemp, gSoll, gFinal, gHum, gSimMode, gRegulationMode, gSSID, device_name, ctrl_cnt, pid.Ki, pid.Kp);
    httpd_resp_sendstr(req, responsebody);
    return ESP_OK;
}

/* request simulation-mode function */
esp_err_t get_gSimMode_status(httpd_req_t *req) {
    httpd_resp_set_type(req, "text/plain");
    char responsebody[100] = "string";
    sprintf(responsebody, "%d", gSimMode);
    httpd_resp_sendstr(req, responsebody);
    return ESP_OK;
}

/* toggle the status of the regulation */
esp_err_t toggle_regulation_mode_handler() {
    gRegulationMode = (gRegulationMode == 1 ? 0 : 1);
    return ESP_OK;
}

/* toggle the status of the simulation */
esp_err_t toggle_simulation_mode_handler() {
    gSimMode = (gSimMode == 1 ? 0 : 1);
    return ESP_OK;
}

/* variables to get data from website input */
char field1_value[32] = {0};
char field2_value[32] = {0};

/* load data from website input */
esp_err_t submit_post_handler(httpd_req_t *req) {
    char buffer[256];
    /* recieve data */
    int received = httpd_req_recv(req, buffer, sizeof(buffer) - 1);
    if (received <= 0) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Failed to receive data");
        return ESP_FAIL;
    }

    buffer[received] = '\0'; 

    /* load JSON from recieved data */
    cJSON *json = cJSON_Parse(buffer);
    if (!json) {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "Invalid JSON");
        return ESP_FAIL;
    }

    /* load values from JSON */
    cJSON *field1 = cJSON_GetObjectItem(json, "field1");
    cJSON *field2 = cJSON_GetObjectItem(json, "field2");
    if (field1 && field2) {
        strncpy(field1_value, field1->valuestring, sizeof(field1_value) - 1);
        strncpy(field2_value, field2->valuestring, sizeof(field2_value) - 1);

        sscanf(field1_value, "%lf", &pid.Ki);
        sscanf(field2_value, "%lf", &pid.Kp);

        httpd_resp_sendstr(req, "1"); // success
    } else {
        httpd_resp_send_err(req, HTTPD_400_BAD_REQUEST, "0"); // error
    }

    cJSON_Delete(json);
    return ESP_OK;
}