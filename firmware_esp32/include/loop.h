/**
 * @file    loop.h
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Declaracion del bucle principal
 */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef LOOP_H
#define LOOP_H

/* Includes ------------------------------------------------------------------*/
#include <Arduino.h>
#include "freertos/FreeRTOS.h"
#include "freertos/queue.h"
#include "freertos/task.h"

/* Exported types ------------------------------------------------------------*/
// Estructura de colas para pasar a la tarea de control
typedef struct {
    QueueHandle_t qSensor;
    QueueHandle_t qExtraBuffer; // Mantinc això per complir "Alguna tasca gestiona més d'un buffer"
} TaskQueues_t;

// Extern queues and task handles
extern QueueHandle_t sensorQueue;
extern QueueHandle_t extraQueue;
extern TaskQueues_t taskQueues;

/* Exported constants --------------------------------------------------------*/

/* Exported macro ------------------------------------------------------------*/

/* Exported functions --------------------------------------------------------*/

void Task_Ultrasonidos(void *pvParameters);
void Task_Control(void *pvParameters);
void Task_Logger(void *pvParameters);

/******************************************************************************/
/**
 * @brief  Ejecuta tareas ciclicas del dispositivo
 * @retval None
 */
void on_loop();

#endif // LOOP_H

/* End of file ****************************************************************/
