#include <Arduino.h>
#include "loop.h"
#include "funciones.h"
#include "config.h"
#include "comunicaciones.h"
#include "setup.h"

long now, lastMsg = 0;
long sensorsUpdateInterval = 5000; // tiempo de actualización de los sensores
bool emergencyLatched = false;

void on_loop() 
{

  //handleButtonState(bottonPressed());

  //bro descomentar cuando la mierda del mqtt vaya bien

  
  long distancia = leerUltrasonidos();

  if (distancia > 0 && distancia != 797) 
  {
  Serial.print("Distancia: ");
  Serial.println(distancia);
  if (distancia < DISTANCIA_EMERGENCIA) 
  {
    if (!emergencyLatched) 
    {
      enviarMensajePorTopic(EMERGENCY_STOP_TOPIC, "STOP");
      Serial.println("EMERGENCY STOP!");
      emergencyLatched = true;
    }
  } else if (emergencyLatched) 
  {
    enviarMensajePorTopic(EMERGENCY_STOP_TOPIC, "GO");
    Serial.println("EMERGENCY CLEARED!");
    emergencyLatched = false;
  }
  }
  
  
  /*
  now = millis();
  if (now - lastMsg > sensorsUpdateInterval) 
  {
    lastMsg = now;
     // Heartbeat: publish a small JSON message indicating device is alive
     String hb = String("Esp32 is alive");
     enviarMensajePorTopic(HELLO_TOPIC, hb);
    


  }
  */
}


