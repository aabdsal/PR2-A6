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
  //mqtt_subscribe(ESTADO_PROCESO_TOPIC);

}

void alRecibirMensajePorTopic(char* topic, String incomingMessage) {

  
  // If a message is received on the topic ...
    if (strcmp(topic, HELLO_TOPIC) == 0 ) {
      if(incomingMessage == "on") {
        infoln("Encender el led interno (remote)");
        setInternalLedFromRemote(1);
        delay(1000);
        setInternalLedFromRemote(0);
      }
    }
      


}

void enviarMensajePorTopic(const char* topic, String outgoingMessage) {

  mqtt_publish(topic, outgoingMessage.c_str());

}





