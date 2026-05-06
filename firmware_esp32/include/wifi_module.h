/**
 * @file    wifi_module.h
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Interfaz del modulo WiFi y cliente de red
 */

/* Define to prevent recursive inclusion -------------------------------------*/
#pragma once

/* Includes ------------------------------------------------------------------*/

#include <Arduino.h>
#include <WiFi.h>
#include <WiFiClient.h>
#ifdef SSL_ROOT_CA
#include <WiFiClientSecure.h>
#endif

/* Exported types ------------------------------------------------------------*/

/* Exported constants --------------------------------------------------------*/

/* Exported macro ------------------------------------------------------------*/

#ifdef SSL_ROOT_CA
extern WiFiClientSecure espWifiClient;
#else
extern WiFiClient espWifiClient;
#endif

/* Exported functions --------------------------------------------------------*/

/******************************************************************************/
/**
 * @brief  Mantiene la conexion WiFi activa
 * @retval None
 */
void wifi_loop();

/******************************************************************************/
/**
 * @brief  Configura y conecta la interfaz WiFi
 * @retval None
 */
void wifi_connect();

/******************************************************************************/
/**
 * @brief  Reintenta la conexion WiFi
 * @param  retries Numero maximo de reintentos
 * @retval None
 */
void wifi_reconnect(uint retries);

/* End of file ****************************************************************/
