#include <Arduino.h>
#include "loop.h"
#include "funciones.h"
#include "config.h"
#include "comunicaciones.h"
#include "setup.h"

long now, lastMsg = 0;
long sensorsUpdateInterval = 5000; // tiempo de actualización de los sensores

void on_loop() {

  handleButtonState(bottonPressed());

  //bro descomentar cuando la mierda del mqtt vaya bien

  /*
  long distancia = leerUltrasonidos();
  if (distancia < DISTANCIA_EMERGENCIA) {
    enviarMensajePorTopic(EMERGENCY_STOP_TOPIC, "{\"status\":\"paro_emergencia\"}");
    // Opcional: afegir un petit retard per no saturar de missatges
    delay(100); 
  }

  */
  now = millis();
  if (now - lastMsg > sensorsUpdateInterval ) {
    lastMsg = now;
     // Heartbeat: publish a small JSON message indicating device is alive
     String hb = String("Esp32 is alive");
     enviarMensajePorTopic(HELLO_TOPIC, hb);
    
    //
    // Read and process sensors
    //
/*
    char tempString[8];
    dtostrf(temperature, 1, 2, tempString);
    Serial.print("Temperature: ");
    Serial.println(tempString);
    enviarMensajePorTopic("esp32/temperature", tempString);
*/

  }

}

