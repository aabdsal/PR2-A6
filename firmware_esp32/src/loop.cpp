#include <Arduino.h>
#include "loop.h"
#include "funciones.h"
#include "config.h"
#include "comunicaciones.h"
#include "setup.h"

long now, lastMsg = 0;
long sensorsUpdateInterval = 5000; // tiempo de actualización de los sensores
bool emergencyLatched = false;
const uint8_t filterWindow = 5;

void on_loop() {

  //handleButtonState(bottonPressed());

  //bro descomentar cuando la mierda del mqtt vaya bien

  
  static long distanceSamples[filterWindow] = {0};
  static uint8_t sampleIndex = 0;
  static bool samplesFilled = false;

  long distancia = leerUltrasonidos();
  distanceSamples[sampleIndex] = distancia;
  sampleIndex = (sampleIndex + 1) % filterWindow;
  if (sampleIndex == 0) {
    samplesFilled = true;
  }

  uint8_t sampleCount = samplesFilled ? filterWindow : sampleIndex;
  long sum = 0;
  for (uint8_t i = 0; i < sampleCount; i++) {
    sum += distanceSamples[i];
  }
  long distanciaFiltrada = (sampleCount > 0) ? (sum / sampleCount) : distancia;

  if (distanciaFiltrada < DISTANCIA_EMERGENCIA) {
    if (!emergencyLatched) {
      //enviarMensajePorTopic(EMERGENCY_STOP_TOPIC, "STOP");
      Serial.println("EMERGENCY STOP!");
      emergencyLatched = true;
    }
  } else if (emergencyLatched) {
    //enviarMensajePorTopic(EMERGENCY_STOP_TOPIC, "GO");
    Serial.println("EMERGENCY CLEARED!");
    emergencyLatched = false;
  }

  /*
  now = millis();
  if (now - lastMsg > sensorsUpdateInterval) {
    lastMsg = now;
     // Heartbeat: publish a small JSON message indicating device is alive
     String hb = String("Esp32 is alive");
     enviarMensajePorTopic(HELLO_TOPIC, hb);
    


  }
  */
}


