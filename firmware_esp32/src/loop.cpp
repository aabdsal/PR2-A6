/**
 * @file    loop.cpp
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Implementacion del bucle principal y logica de emergencia
 */

/* Includes ------------------------------------------------------------------*/
#include <Arduino.h>
#include "loop.h"
#include "funciones.h"
#include "config.h"
#include "comunicaciones.h"
#include "setup.h"
#include "buffer_circular.h"

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/

long now, lastMsg = 0;
long sensorsUpdateInterval = 5000; // tiempo de actualización de los sensores

bool PARAR = false;

/* Private function prototypes -----------------------------------------------*/

/* Exported functions --------------------------------------------------------*/

/* Private functions ---------------------------------------------------------*/

/* End of file ****************************************************************/