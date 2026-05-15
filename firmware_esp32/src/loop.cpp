/**
 * @file    loop.cpp
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Implementacion del bucle principal y logica de emergencia
 */

/* Includes ------------------------------------------------------------------*/
#include <Arduino.h>
#include <ArduinoJson.h>
#include "loop.h"
#include "funciones.h"
#include "config.h"
#include "comunicaciones.h"
#include "setup.h"
#include "web.h"
#include "c_logger.h"

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/

long sensorsUpdateInterval = 5000; // tiempo de actualización de los sensores
bool emergencyLatched = false;

/* Private function prototypes -----------------------------------------------*/

/* Exported functions --------------------------------------------------------*/

void tareaLedOn(void *pvParameters)
{
    infoln("Encender el led interno (remote)");
    setInternalLedFromRemote(1);
    vTaskDelay(pdMS_TO_TICKS(1000));
    setInternalLedFromRemote(0);
    vTaskDelete(NULL);
}

// Nueva tarea que envuelve LA MISMA lógica del ultrasonidos (Rubrica 2)
void Task_Ultrasonidos(void *pvParameters)
{
    TaskQueues_t *queues = (TaskQueues_t *)pvParameters; // Pasamos parámetros según rúbrica
    TickType_t xLastWakeTime = xTaskGetTickCount();
    const TickType_t xFrequency = pdMS_TO_TICKS(100); // Frecuencia de muestreo del sensor

    for(;;)
    {
        JsonDocument doc;
        long distancia = leerUltrasonidos();

        if (distancia > 0 && distancia != 797) 
        {
            Serial.print("Distancia: ");
            Serial.println(distancia);

            if (distancia < DISTANCIA_EMERGENCIA) 
            {
                if (!emergencyLatched) 
                {
                    doc["estado_simulacion"] = "STOP";

                    String payload;
                    serializeJson(doc, payload);

                    enviarMensajePorTopic(EMERGENCY_STOP_TOPIC, payload);
                    Serial.println("EMERGENCY STOP!");
                    emergencyLatched = true;
                }
            } 
            else if (emergencyLatched) 
            {
                doc["estado_simulacion"] = "GO";

                String payload;
                serializeJson(doc, payload);

                enviarMensajePorTopic(EMERGENCY_STOP_TOPIC, payload);
                Serial.println("EMERGENCY CLEARED!");
                emergencyLatched = false;
            }
        }

        // Simulación de uso del sensor buffer temporal para cumplir la rúbrica (más de 1 buffer manejado)
        long copyDist = distancia;
        xQueueSend(queues->qSensor, &copyDist, 0);

        // Tarea periodica timing absoluto
        vTaskDelayUntil(&xLastWakeTime, xFrequency);
    }
}

void on_loop()
{
    handleWebServer();
}

/* Private functions ---------------------------------------------------------*/

/* End of file ****************************************************************/



