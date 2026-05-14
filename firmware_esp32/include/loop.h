/**
 * @file    loop.h
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Declaracion del bucle principal
 */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef LOOP_H
#define LOOP_H

/* Evita el name mangling con c++ ------------------------------------------- */
#ifdef __cplusplus
 extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/

/* Exported types ------------------------------------------------------------*/

/* Exported constants --------------------------------------------------------*/

/* Exported macro ------------------------------------------------------------*/

/* Exported functions --------------------------------------------------------*/

/******************************************************************************/
/**
 * @brief  Ejecuta tareas ciclicas del dispositivo
 * @retval None
 */
void tareaUltrasonidos(void *parameter);

#ifdef __cplusplus
}
#endif

#endif // LOOP_H

/* End of file ****************************************************************/
