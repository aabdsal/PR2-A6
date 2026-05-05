#include "comunicaciones.h"
#include "config.h"
#include "c_logger.h"
#include "mqtt.h"
#include "funciones.h"

void suscribirseATopics() 
{
  // TODO: añadir suscripciones a los topics MQTT ...
  mqtt_subscribe(HELLO_TOPIC);
  //mqtt_subscribe(BUTTON_TOPIC);
  mqtt_subscribe(EMERGENCY_STOP_TOPIC);
  //mqtt_subscribe(ESTADO_PROCESO_TOPIC);
}


void alRecibirMensajePorTopic(char* topic, String incomingMessage) {

  StaticJsonDocument<128> doc;
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
    }
    else if (strcmp(estadoLed, "off") == 0) 
    {
      infoln("Apagar el led interno (remote)");
      setInternalLedFromRemote(0);
    }
    else 
    {
      warnln("estado_led desconocido");
    }
  }

  if (strcmp(topic, ESTADO_PROCESO_TOPIC) == 0 ) 
  {
    const char* proc = doc["proc"];
    if (!proc) {
      warnln("Falta el campo proc en ESTADO_PROCESO_TOPIC");
      return;
    }

    if (strcmp(proc, "proc1") == 0) 
    {
      infoln("Ejecutando proceso 1...");
      setLedProceso(1);
    }
    else if (strcmp(proc, "proc2") == 0) 
    {
      infoln("Ejecutando proceso 2...");
      setLedProceso(2);
    }
    else if (strcmp(proc, "proc3") == 0) 
    {
      infoln("Ejecutando proceso 3...");
      setLedProceso(3);
    }
    else 
    {
      warnln("proc desconocido");
    }
  }

}

void enviarMensajePorTopic(const char* topic, String outgoingMessage) 
{
  mqtt_publish(topic, outgoingMessage.c_str());
}





