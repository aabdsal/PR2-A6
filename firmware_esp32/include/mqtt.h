/**
 * @file    mqtt.h
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Interfaz del modulo MQTT
 */

/* Define to prevent recursive inclusion -------------------------------------*/
#pragma once

/* Includes ------------------------------------------------------------------*/

#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>

/* Exported types ------------------------------------------------------------*/

/* Exported constants --------------------------------------------------------*/

/* Exported macro ------------------------------------------------------------*/

/* Exported functions --------------------------------------------------------*/

/******************************************************************************/
/**
 * @brief  Mantiene el bucle MQTT y gestiona reconexiones
 * @retval None
 */
void mqtt_loop();

/******************************************************************************/
/**
 * @brief  Configura y conecta el cliente MQTT
 * @param  clientID Identificador del cliente
 * @retval None
 */
void mqtt_connect(String clientID);

/******************************************************************************/
/**
 * @brief  Reintenta la conexion al broker MQTT
 * @param  retries Numero maximo de reintentos
 * @retval None
 */
void mqtt_reconnect(int retries);

/******************************************************************************/
/**
 * @brief  Callback al recibir un mensaje MQTT
 * @param  topic Topic recibido
 * @param  message Payload recibido
 * @param  length Longitud del payload
 * @retval None
 */
void mqttCallback(char* topic, byte* message, unsigned int length);

/******************************************************************************/
/**
 * @brief  Publica un mensaje MQTT
 * @param  topic Topic de destino
 * @param  outgoingMessage Mensaje a publicar
 * @retval None
 */
void mqtt_publish(const char* topic, String outgoingMessage);

/******************************************************************************/
/**
 * @brief  Se suscribe a un topic MQTT
 * @param  topic Topic de suscripcion
 * @retval None
 */
void mqtt_subscribe(const char* topic);

/* End of file ****************************************************************/