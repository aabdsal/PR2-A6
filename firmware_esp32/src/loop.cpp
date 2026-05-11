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
#include "web.h"

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/

long now, lastMsg = 0;
long sensorsUpdateInterval = 5000; // tiempo de actualización de los sensores
bool emergencyLatched = false;

/* Private function prototypes -----------------------------------------------*/

/* Exported functions --------------------------------------------------------*/
void on_loop()
{
    handleWebServer();

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
}

/* Private functions ---------------------------------------------------------*/

/* End of file ****************************************************************/



