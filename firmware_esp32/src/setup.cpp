#include <ArduinoJson.h>
#include "setup.h"
#include "config.h"
#include "funciones.h"
#include "comunicaciones.h"

void on_setup() {

    // initialize digital pin LED_BUILTIN as an output.
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    setInternalLed(0);

    

}

