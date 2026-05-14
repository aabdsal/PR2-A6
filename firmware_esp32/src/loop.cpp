/**
 * @file    loop.cpp
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Implementacion del bucle principal y logica de emergencia
 */

/* Includes ------------------------------------------------------------------*/
#include <Arduino.h>
#include "loop.h"
#include "funciones.h"
#include "config.h"
#include "comunicaciones.h"
#include "setup.h"
#include "buffer_circular.h"

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/

long now, lastMsg = 0;
long sensorsUpdateInterval = 5000; // tiempo de actualización de los sensores
bool emergencyLatched = false;

/* Private function prototypes -----------------------------------------------*/

/* Exported functions --------------------------------------------------------*/
bool PARAR = false;
void tareaUltrasonidos(void *parameter)
{
    Buffer_Circ* buff_prod = (Buffer_Circ*) parameter;
    const TickType_t xFrequency = pdMS_TO_TICKS(250);
    TickType_t xLastWakeTime = xTaskGetTickCount();
    while(!PARAR)
    {
        long lectura_ultrasonidos = leerUltrasonidos();
        if(lectura_ultrasonidos < DISTANCIA_EMERGENCIA)
        {
            if(!emergencyLatched)
            {
                push(buff_prod, PLANTA_STOP);
                emergencyLatched = true;
            }
        }
        else if(emergencyLatched)
        {
            push(buff_prod, PLANTA_GO);
            emergencyLatched = false;
        }
        vTaskDelayUntil(&xLastWakeTime, xFrequency);
    }
    vTaskDelete(NULL);
}


/* Private functions ---------------------------------------------------------*/

/* End of file ****************************************************************/
/*
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

*/