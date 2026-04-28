#pragma once

#include <Arduino.h>

void setInternalLed(uint8_t status);
bool bottonPressed();
void handleButtonState(bool pressed);
