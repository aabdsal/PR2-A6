#include <Arduino.h>
#include "comunicaciones.h"
#include "funciones.h"
#include "config.h"
#include "c_logger.h"

uint8_t ledStatus = 0;

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

bool bottonPressed() {
  return digitalRead(BUTTON_PIN) == LOW;
}

void handleButtonState(bool pressed) {
  static bool previousPressed = false;

  if (pressed && !previousPressed) {
    infoln("Button pressed");
    enviarMensajePorTopic(BUTTON_TOPIC, String("esta polsat"));
  }

  previousPressed = pressed;
  setInternalLed(pressed ? 1 : 0);
}



