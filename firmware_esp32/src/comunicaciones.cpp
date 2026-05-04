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
      
    }

    if (strcmp(topic, ESTADO_PROCESO_TOPIC) == 0 ) {
      infoln("Mensaje recibido en topic ESTADO_PROCESO_TOPIC:");
      infoln(incomingMessage);

      if (incomingMessage == "proc1") {
        infoln("Ejecutando proceso 1...");
        setLedProceso(1);
      }
      else if (incomingMessage == "proc2") {
        infoln("Ejecutando proceso 2...");
        setLedProceso(2);
      }
      else if (incomingMessage == "proc3") {
        infoln("Ejecutando proceso 3...");
        setLedProceso(3);
      }
     
    }

      


}

void enviarMensajePorTopic(const char* topic, String outgoingMessage) {

  mqtt_publish(topic, outgoingMessage.c_str());

}





