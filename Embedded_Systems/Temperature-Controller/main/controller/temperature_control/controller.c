/*********************************************************************************************/
/**  Author:     Philip Biechl                                                              **/
/**  Project:    Embedded Systems - Building Blocks                                         **/
/*********************************************************************************************/

#include "../include/controller.h"

/* PID Controller - D is set to '0' because of use case */
PID_Controller pid;

/* initialises the controller */
void PID_Init(PID_Controller *pid, double Kp, double Ki, double Kd, double setpoint, double realVal, double deltaTime, double output_min, double output_max) {
    pid->Kp = Kp;
    pid->Ki = Ki;
    pid->Kd = Kd;
    pid->setpoint = setpoint;
    pid->realvalue = realVal;
    pid->prev_error = 0.0;
    pid->integral = 0.0;
    pid->delta_time = deltaTime;
    pid->output_min = output_min;
    pid->output_max = output_max;
}

/* calculate controller response */
double PID_Compute(PID_Controller *pid) {
    double error = (pid->setpoint) - (pid->realvalue);

    pid->integral += error * pid->delta_time * pid->Ki;

    double derivative = (error - pid->prev_error) / pid->delta_time;

    double output = (pid->Kp * error) + (pid->integral) + (pid->Kd * derivative);

    pid->prev_error = error;

    if (output > pid->output_max) output = pid->output_max;
    if (output < pid->output_min) output = pid->output_min;

    printf("%lf %lf %lf\n\n", output, pid->output_max, error);

    return output;
}