/**
 * @file    setup.cpp
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Implementacion de la configuracion inicial de pines
 */

/* Includes ------------------------------------------------------------------*/
#include <ArduinoJson.h>
#include "setup.h"
#include "config.h"
#include "funciones.h"
#include "comunicaciones.h"
#include "web.h"

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/
/* Private function prototypes -----------------------------------------------*/
/* Exported functions --------------------------------------------------------*/
void on_setup() 
{
    // initialize digital pin LED_BUILTIN as an output.
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    initWebServer();
}

/* Private functions ---------------------------------------------------------*/

/* End of file ****************************************************************/

