#include "comunicaciones.h"
#include "config.h"
#include "c_logger.h"
#include "mqtt.h"
#include "funciones.h"
#include <ArduinoJson.h>

void suscribirseATopics() 
{
  // TODO: añadir suscripciones a los topics MQTT ...
  mqtt_subscribe(HELLO_TOPIC);
  //mqtt_subscribe(BUTTON_TOPIC);
  mqtt_subscribe(EMERGENCY_STOP_TOPIC);
  //mqtt_subscribe(ESTADO_PROCESO_TOPIC);
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

  // If a message is received on the topic ...
  if (strcmp(topic, HELLO_TOPIC) == 0 ) {
    const char* estadoLed = doc["estado_led"];
    if (!estadoLed) 
    {
      warnln("Falta el campo estado_led en HELLO_TOPIC");
      return;
    }

    if (strcmp(estadoLed, "on") == 0) 
    {
      infoln("Encender el led interno (remote)");
      setInternalLedFromRemote(1);
      delay(1000);
      setInternalLedFromRemote(0);
    }
    
  }
}

void enviarMensajePorTopic(const char* topic, String outgoingMessage) 
{
  mqtt_publish(topic, outgoingMessage.c_str());
}





