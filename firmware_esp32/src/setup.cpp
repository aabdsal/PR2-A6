/**
 * @file    setup.cpp
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Implementacion de la configuracion inicial de pines
 */

/* Includes ------------------------------------------------------------------*/
#include <ArduinoJson.h>
#include "setup.h"
#include "loop.h"
#include "config.h"
#include "funciones.h"
#include "comunicaciones.h"
#include "web.h"

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/
QueueHandle_t sensorQueue;
QueueHandle_t extraQueue;
TaskQueues_t taskQueues;

/* Private function prototypes -----------------------------------------------*/

/* Exported functions --------------------------------------------------------*/
void on_setup() 
{
    // initialize digital pin LED_BUILTIN as an output.
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    // Initialitzacio colas
    sensorQueue = xQueueCreate(5, sizeof(long));
    extraQueue = xQueueCreate(5, sizeof(uint8_t));

    taskQueues.qSensor = sensorQueue;
    taskQueues.qExtraBuffer = extraQueue;

    // Creacion de tareas pasando argumentos
    xTaskCreate(Task_Ultrasonidos, "Task_Ultra", 4096, (void*)&taskQueues, 2, NULL);

    initWebServer();
}

/* Private functions ---------------------------------------------------------*/

/* End of file ****************************************************************/

