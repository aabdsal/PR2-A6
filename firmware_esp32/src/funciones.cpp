#include <Arduino.h>
#include "comunicaciones.h"
#include "funciones.h"
#include "config.h"
#include "c_logger.h"

uint8_t ledStatus = 0;
// When true, button presses won't change the LED; remote commands control it
static bool ledRemoteLocked = false;

void setInternalLed(uint8_t status) {
  if ( ledStatus == status ) // Nothing to do
    return;
    
  ledStatus = status;
  if ( status ) {
    infoln("Led: on");
    digitalWrite(LED_BUILTIN, HIGH);  
  } else {
    infoln("Led: off");
    digitalWrite(LED_BUILTIN, LOW);
  }

  // TODO: Deberíamos publicar el estado del dispositivo cada vez que cambie
}

void setInternalLedFromRemote(uint8_t status) {
  // lock control to remote commands
  ledRemoteLocked = true;
  if ( ledStatus == status ) return;
  ledStatus = status;
  if ( status ) {
    infoln("Led: on");
    digitalWrite(LED_BUILTIN, HIGH);
  } else {
    infoln("Led: off");
    digitalWrite(LED_BUILTIN, LOW);
  }
}

bool isInternalLedRemoteLocked() {
  return ledRemoteLocked;
}

bool bottonPressed() {
  return digitalRead(BUTTON_PIN) == LOW;
}


void handleButtonState(bool pressed) {
  static bool previousPressed = false;

  // If LED is controlled by remote commands, ignore button presses
  if (ledRemoteLocked) {
    previousPressed = pressed;
    return;
  }

  if (pressed && !previousPressed) {
    infoln("Button pressed");
    //enviarMensajePorTopic(BUTTON_TOPIC, String("esta polsat"));
  }

  previousPressed = pressed;
  setInternalLed(pressed ? 1 : 0);
}

long leerUltrasonidos() {
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



