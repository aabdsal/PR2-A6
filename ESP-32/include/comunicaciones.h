#pragma once

#include <Arduino.h>
#include <ArduinoJson.h>
#include <cstring>

void suscribirseATopics();
void alRecibirMensajePorTopic(char* topic, String incomingMessage);
void enviarMensajePorTopic(const char* topic, String outgoingMessage);