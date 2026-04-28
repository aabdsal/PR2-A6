#include <Arduino.h>
#include "loop.h"
#include "funciones.h"

long now, lastMsg = 0;
long sensorsUpdateInterval = 5000; // tiempo de actualización de los sensores

void on_loop() {

  handleButtonState(bottonPressed());

  now = millis();
  if (now - lastMsg > sensorsUpdateInterval ) {
    lastMsg = now;
    
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

