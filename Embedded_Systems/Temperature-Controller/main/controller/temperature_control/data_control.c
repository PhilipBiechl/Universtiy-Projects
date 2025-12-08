/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#include "../include/data_control.h"

/* calculate temperature for simulated rooms */
void calculate_sim_temp() {
    gSimTemp = gSimTemp + (((gFinal - gSimTemp) * HEATING_POWER / HEAT_LOSS - gSimTemp) / (TEMP_CAPACITY / HEAT_LOSS)); // Difference in wanted and heating temperature - with room specifications
}

/* update data for current situation */
void data_read_task(void* arg) {
    while (1) {
        if (gServer) {
            /* get real temperature, humidity */
            shtc3_read(&gTemp, &gHum);
            if (!gSimMode) {
                /* load as real temperature */
                gSimTemp = gTemp;
            } else {
                /* load from simulated temperature */
                calculate_sim_temp();
                gTemp = gSimTemp;
            }
            if (!gRegulationMode) {
                /* input is heating parameter */
                gFinal = gSoll;
            } else {
                /* controller sets heating parameter to get desired temperature from input */
                pid.realvalue = gTemp;
                pid.setpoint = gSoll;
                gFinal = PID_Compute(&pid);
            }
        }
        vTaskDelay(pdMS_TO_TICKS(1000));
    }
}