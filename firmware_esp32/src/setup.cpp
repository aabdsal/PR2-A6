/**
 * @file    setup.cpp
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Implementacion de la configuracion inicial de pines
 */

/* Includes ------------------------------------------------------------------*/
#include <ArduinoJson.h>
#include "buffer_circular.h"
#include "loop.h"
#include "setup.h"
#include "config.h"
#include "funciones.h"
#include "comunicaciones.h"

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/
Buffer_Circ buzon_mqtt;
Buffer_Circ buzon_led;
/* Private function prototypes -----------------------------------------------*/
/* Exported functions --------------------------------------------------------*/
void on_setup() 
{
    // initialize digital pin LED_BUILTIN as an output.
    pinMode(LED_BUILTIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);
    xTaskCreatePinnedToCore(tareaUltrasonidos, "T_Ultrasonidos", 10000, &buzon_mqtt, 1, NULL, 0);
    xTaskCreatePinnedToCore(tareaGestorMQTT, "T_GestorMQTT", 10000, &buzon_mqtt, 1, NULL, 0);
    xTaskCreatePinnedToCore(tareaLED, "T_LED", 10000, &buzon_led, 1, NULL, 0);
   
}

/* Private functions ---------------------------------------------------------*/

/* End of file ****************************************************************/

