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

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/

long sensorsUpdateInterval = 5000; // tiempo de actualización de los sensores
//bool emergencyLatched = false; AQUÍ ES GLOBAL, LA HE METIDO EN TASK CONTROL PARA QUE SEA VARIABLE LOCAL

/* Private function prototypes -----------------------------------------------*/

/* Exported functions --------------------------------------------------------*/

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
            xQueueSend(queues->qSensor, &distancia, 0);

            // ESTO DE AQUÍ ABAJO VA A IR EN OTRA TAREA

            /*Serial.print("Distancia: ");
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
        xQueueSend(queues->qSensor, &copyDist, 0);*/
        }

        // Tarea periodica timing absoluto
        vTaskDelayUntil(&xLastWakeTime, xFrequency);
    }
}

/* --- Tarea 2: Lógica y MQTT --- */
void Task_Control(void *pvParameters)
{
    TaskQueues_t *queues = (TaskQueues_t *)pvParameters;
    long distRecibida;
    bool localEmergencyLatched = false; // Estado local, eliminamos la variable global 

    for(;;)
    {
        // Esperamos a que llegue un dato de la cola (Bloqueante hasta que haya datos)
        if (xQueueReceive(queues->qSensor, &distRecibida, portMAX_DELAY) == pdPASS)
        {
            JsonDocument doc;
            
            if (distRecibida < DISTANCIA_EMERGENCIA) // 
            {
                if (!localEmergencyLatched) 
                {
                    doc["estado_simulacion"] = "STOP";
                    String payload;
                    serializeJson(doc, payload);
                    enviarMensajePorTopic(EMERGENCY_STOP_TOPIC, payload); // 
                    
                    localEmergencyLatched = true;

                    //  Así manejamos más de un buffer: Enviamos código de evento (1=STOP)
                    uint8_t eventCode = 1;
                    xQueueSend(queues->qExtraBuffer, &eventCode, 0); 
                }
            } 
            else if (localEmergencyLatched) 
            {
                doc["estado_simulacion"] = "GO";
                String payload;
                serializeJson(doc, payload);
                enviarMensajePorTopic(EMERGENCY_STOP_TOPIC, payload); // 
                
                localEmergencyLatched = false;

                // Enviamos código de evento al segundo buffer (0=CLEAR)
                uint8_t eventCode = 0;
                xQueueSend(queues->qExtraBuffer, &eventCode, 0);
            }
        }
    }
}

void on_loop()
{
    handleWebServer();
}

/* Private functions ---------------------------------------------------------*/

/* End of file ****************************************************************/



