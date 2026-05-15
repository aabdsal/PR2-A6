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

/* Includes ------------------------------------------------------------------*/
#include <Arduino.h>

/* Exported types ------------------------------------------------------------*/

/* Exported constants --------------------------------------------------------*/

/* Exported macro ------------------------------------------------------------*/

/* Exported functions --------------------------------------------------------*/

extern volatile bool button_pressed_flag;
void button_isr();

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
 * @brief  Tarea que encender y apagar el LED
 * @param pvParameters parametros opcionales de FreeRTOS
 * @retval None
 */
void led_task(void *pvParameters);

/******************************************************************************/
/**
 * @brief  Ejecuta tareas ciclicas del dispositivo
 * @param pvParameters parametros opcionales de FreeRTOS
 * @retval None
 */
void ultrasonidos_task(void *pvParameters);

/******************************************************************************/
/**
 * @brief  Tarea que gestiona el envío de mensajes de emergencia por MQTT
 * @param pvParameters parametros opcionales de FreeRTOS
 * @retval None
 */
void handle_mqtt_task(void *pvParameters);

#endif // FUNCIONES_H

/* End of file ****************************************************************/