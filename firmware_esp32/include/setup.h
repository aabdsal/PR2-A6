/**
 * @file    setup.h
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Declaracion de la configuracion inicial del dispositivo
 */

/* Define to prevent recursive inclusion -------------------------------------*/
#pragma once

/* Includes ------------------------------------------------------------------*/

#include <Arduino.h>

/* Exported types ------------------------------------------------------------*/

/* Exported constants --------------------------------------------------------*/

/* Exported macro ------------------------------------------------------------*/

/* Exported functions --------------------------------------------------------*/

extern String deviceID;

/******************************************************************************/
/**
 * @brief  Configura pines y estado inicial del dispositivo
 * @retval None
 */
void on_setup();

/* End of file ****************************************************************/
