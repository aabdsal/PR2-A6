#pragma once

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>
#ifdef SSL_ROOT_CA
#include <WiFiClientSecure.h>
#endif

#ifdef SSL_ROOT_CA
extern WiFiClientSecure espWifiClient;
#else
extern WiFiClient espWifiClient;
#endif

void wifi_loop();
void wifi_connect();
void wifi_reconnect(uint retries);
