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
void IRAM_ATTR isrBotonEmergencia()
{
    PARAR = true;
}

void on_setup() 
{
    pinMode(LED_PIN, OUTPUT);
    pinMode(LED_WELDING_PIN, OUTPUT);
    pinMode(BUTTON_PIN, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(BUTTON_PIN), isrBotonEmergencia, FALLING);
    pinMode(TRIG_PIN, OUTPUT);
    pinMode(ECHO_PIN, INPUT);

    xTaskCreatePinnedToCore(led_task, "led_task", 10000, &buzon_led, 1, NULL, 0);
    xTaskCreatePinnedToCore(ultrasonidos_task, "ultrasonidos_task", 10000, &buzon_mqtt, 1, NULL, 0);
    xTaskCreatePinnedToCore(handle_mqtt_task, "handle_mqtt_task", 10000, &buzon_mqtt, 1, NULL, 0);
}

/* Private functions ---------------------------------------------------------*/

/* End of file ****************************************************************/
