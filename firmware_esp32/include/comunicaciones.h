/**
 * @file    comunicaciones.h
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Declaraciones de funciones de comunicaciones MQTT
 */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef COMUNICACIONES_H
#define COMUNICACIONES_H

/* Evita el name mangling con c++ ------------------------------------------- */
#ifdef __cplusplus
 extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/

#include <Arduino.h>
#include <ArduinoJson.h>
#include <cstring>

/* Exported types ------------------------------------------------------------*/

/* Exported constants --------------------------------------------------------*/

/* Exported macro ------------------------------------------------------------*/

/* Exported functions --------------------------------------------------------*/

/******************************************************************************/
/**
 * @brief  Suscribe el cliente MQTT a los topics del sistema
 * @retval None
 */
void suscribirseATopics();

/******************************************************************************/
/**
 * @brief  Procesa un mensaje recibido por un topic MQTT
 * @param  topic Topic del mensaje
 * @param  incomingMessage Carga util recibida
 * @retval None
 */
void alRecibirMensajePorTopic(char* topic, String incomingMessage);

/******************************************************************************/
/**
 * @brief  Publica un mensaje en un topic MQTT
 * @param  topic Topic de destino
 * @param  outgoingMessage Mensaje a publicar
 * @retval None
 */
void enviarMensajePorTopic(const char* topic, String outgoingMessage);

#ifdef __cplusplus
}
#endif

#endif // COMUNICACIONES_H

/* End of file ****************************************************************/