#include <Arduino.h>
#include "comunicaciones.h"
#include "funciones.h"
#include "config.h"
#include "c_logger.h"

uint8_t ledStatus = 0;
// When true, button presses won't change the LED; remote commands control it
static bool ledRemoteLocked = false;


void setInternalLedFromRemote(uint8_t status) 
{
  // lock control to remote commands
  ledRemoteLocked = true;
  if (ledStatus == status) return;

  ledStatus = status;
  
  if (status) 
  {
    infoln("Led: on");
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    infoln("Led: off");
    digitalWrite(LED_BUILTIN, LOW);
  }
}



long leerUltrasonidos() 
{
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);
  
  long duration = pulseIn(ECHO_PIN, HIGH);
  
  // Calculating the distance
  // Speed of sound wave divided by 2 (go and back)
  return duration * 0.034 / 2;
}



