/**
 * @file    comunicaciones.cpp
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Implementacion de comunicaciones MQTT y manejo de mensajes
 */

/* Includes ------------------------------------------------------------------*/
#include "buffer_circular.h"
#include "comunicaciones.h"
#include "config.h"
#include "c_logger.h"
#include "mqtt.h"
#include "funciones.h"
#include <ArduinoJson.h>

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Exported variables --------------------------------------------------------*/
extern bool PARAR;
extern Buffer_Circ buzon_led;
/* Private function prototypes -----------------------------------------------*/
/* Exported functions --------------------------------------------------------*/
void suscribirseATopics() 
{
    // TODO: añadir suscripciones a los topics MQTT ...
    mqtt_subscribe(HELLO_TOPIC);
    mqtt_subscribe(LED_TOPIC);
    mqtt_subscribe(EMERGENCY_STOP_TOPIC);
}


void alRecibirMensajePorTopic(char* topic, String incomingMessage) {

    JsonDocument doc;
    DeserializationError err = deserializeJson(doc, incomingMessage);
    if (err) 
    {
        warnln("Error al parsear JSON en mensaje MQTT");
        warnln(err.c_str());
        return;
    }

    if (strcmp(topic, LED_TOPIC) == 0 ) 
    {
        const char* estadoLed = doc["estado_led"];
        if (!estadoLed) 
        {
          warnln("Falta el campo estado_led en LED_TOPIC");
          return;
        }

        if (strcmp(estadoLed, "on") == 0) 
        {
          infoln("Orden recibida: Encender LED. Enviando al buzon...");
          push(&buzon_led, LED_ENCENDIDO);
        }

    }
}

void enviarMensajePorTopic(const char* topic, String outgoingMessage) 
{
    mqtt_publish(topic, outgoingMessage.c_str());
}

void tareaGestorMQTT(void *parameter)
{
    Buffer_Circ* buff_cons = (Buffer_Circ*) parameter;
    const TickType_t xFrequency = pdMS_TO_TICKS(100);
    TickType_t xLastWakeTime = xTaskGetTickCount();
    int estado_recibido;
    while(!PARAR)
    {
        if(pop(buff_cons, &estado_recibido) == 0)
        {
            JsonDocument doc;
            if(estado_recibido == PLANTA_GO)
            {
                doc["estado_simulacion"] = "GO";
                String payload;
                serializeJson(doc, payload);

                enviarMensajePorTopic(EMERGENCY_STOP_TOPIC, payload);
                Serial.println("EMERGENCY CLEARED!");
            }
            else
            {
                doc["estado_simulacion"] = "STOP";

                String payload;
                serializeJson(doc, payload);

                enviarMensajePorTopic(EMERGENCY_STOP_TOPIC, payload);
                Serial.println("EMERGENCY STOP!");
            }
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




