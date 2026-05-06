#pragma once

#include <Arduino.h>

//void setInternalLed(uint8_t status);
bool bottonPressed();
void handleButtonState(bool pressed);
long leerUltrasonidos();
// Remote control helpers: set LED and lock control to remote commands
void setInternalLedFromRemote(uint8_t status);
bool isInternalLedRemoteLocked();
void setLedProceso(uint8_t proceso);