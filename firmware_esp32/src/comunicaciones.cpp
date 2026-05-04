#include "comunicaciones.h"
#include "config.h"
#include "c_logger.h"
#include "mqtt.h"
#include "funciones.h"

void suscribirseATopics() {
  
  // TODO: añadir suscripciones a los topics MQTT ...
  mqtt_subscribe(HELLO_TOPIC);
  //mqtt_subscribe(BUTTON_TOPIC);
  mqtt_subscribe(EMERGENCY_STOP_TOPIC);

}

void alRecibirMensajePorTopic(char* topic, String incomingMessage) {

  // TODO: Controlador que gestiona la recepción de datos

  // A partir de aquí debemos gestionar los mensajes
  //  recibidos por los diferentes topics (canales)
  //
  
  // If a message is received on the topic ...
    if (strcmp(topic, HELLO_TOPIC) == 0 ) {
      if(incomingMessage == "on") {
        infoln("Encender el led interno (remote)");
        setInternalLedFromRemote(1);
      }
      else if (incomingMessage == "off") {
        infoln("Apagar el led interno (remote)");
        setInternalLedFromRemote(0);
      }
      else {
        warnln("**>> Solicitud no reconocida!");
      }
    }




}

void enviarMensajePorTopic(const char* topic, String outgoingMessage) {

  mqtt_publish(topic, outgoingMessage.c_str());

}





