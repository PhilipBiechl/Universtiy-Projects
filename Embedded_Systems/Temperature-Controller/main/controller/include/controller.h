/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#ifndef CONTROLLER_H
#define CONTROLLER_H

#include "stdint.h"

#include "../include/server_data.h"

typedef struct {
    double Kp;
    double Ki;
    double Kd;

    double setpoint;
    double realvalue;
    double prev_error;
    double integral;

    double delta_time; // seconds
    double output_min; // °C
    double output_max; // °C
} PID_Controller;

extern PID_Controller pid;

void PID_Init(PID_Controller *pid, double Kp, double Ki, double Kd, double setpoint, double realVal, double deltaTime, double output_min, double output_max);
double PID_Compute(PID_Controller *pid);

#endif // controller.h