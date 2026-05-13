/**
 * @file    funciones.h
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Prototipos de funciones auxiliares del dispositivo
 */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef FUNCIONES_H
#define FUNCIONES_H

/* Evita el name mangling con c++ ------------------------------------------- */
#ifdef __cplusplus
 extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include <Arduino.h>

/* Exported types ------------------------------------------------------------*/

/* Exported constants --------------------------------------------------------*/

/* Exported macro ------------------------------------------------------------*/

/* Exported functions --------------------------------------------------------*/

/******************************************************************************/
/**
 * @brief  Lee el estado del boton
 * @retval true si el boton esta pulsado
 */
bool bottonPressed();

/******************************************************************************/
/**
 * @brief  Gestiona el estado del boton
 * @param  pressed Estado actual del boton
 * @retval None
 */
void handleButtonState(bool pressed);

/******************************************************************************/
/**
 * @brief  Mide la distancia con el sensor ultrasonico
 * @retval Distancia en centimetros
 */
long leerUltrasonidos();

/******************************************************************************/
/**
 * @brief  Actualiza el LED interno con control remoto
 * @param  status Estado del LED (0 apagado, 1 encendido)
 * @retval None
 */
void setInternalLedFromRemote(uint8_t status);

/******************************************************************************/
/**
 * @brief  Indica si el control remoto del LED esta activo
 * @retval true si el control remoto esta bloqueado
 */
bool isInternalLedRemoteLocked();

/******************************************************************************/
/**
 * @brief  Actualiza el LED de proceso
 * @param  proceso Estado o codigo de proceso
 * @retval None
 */
void setLedProceso(uint8_t proceso);

#ifdef __cplusplus
}
#endif

#endif // FUNCIONES_H

/* End of file ****************************************************************/