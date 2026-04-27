#pragma once

#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

void mqtt_loop();
void mqtt_connect(String clientID);
void mqtt_reconnect(int retries);
void mqttCallback(char* topic, byte* message, unsigned int length);
void mqtt_publish(const char* topic, String outgoingMessage);
void mqtt_subscribe(const char* topic);