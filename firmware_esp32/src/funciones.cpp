/**
 * @file    funciones.cpp
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Implementacion de funciones auxiliares (LED y ultrasonidos)
 */

/* Includes ------------------------------------------------------------------*/
#include <Arduino.h>
#include "comunicaciones.h"
#include "funciones.h"
#include "config.h"
#include "c_logger.h"
#include "buffer_circular.h"

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Variables -----------------------------------------------------------------*/
extern bool PARAR;
uint8_t ledStatus = 0;
// When true, button presses won't change the LED; remote commands control it
static bool ledRemoteLocked = false;

/* Private function prototypes -----------------------------------------------*/

/* Exported functions --------------------------------------------------------*/
void setInternalLedFromRemote(uint8_t status) 
{
    // lock control to remote commands
    ledRemoteLocked = true;
    if (ledStatus == status) 
    {
        return;
    }
    
    ledStatus = status;
  
    if (status) 
    {
      infoln("Led: on");
      digitalWrite(LED_BUILTIN, HIGH);
    } else {
      infoln("Led: off");
      digitalWrite(LED_BUILTIN, LOW);
    }
}

void tareaLED(void *parameter)
{
  Buffer_Circ* buff_led = (Buffer_Circ*) parameter;
  const TickType_t xFrequency = pdMS_TO_TICKS(100);
  TickType_t xLastWakeTime = xTaskGetTickCount();
  int orden_recibida;
  while(!PARAR)
  {
    if(pop(buff_led, &orden_recibida) == 0)
    {
      if(orden_recibida == LED_ENCENDIDO)
      {
        setInternalLedFromRemote(1);
        vTaskDelay(pdMS_TO_TICKS(1000));
        setInternalLedFromRemote(0);
      }
    }
    vTaskDelayUntil(&xLastWakeTime, xFrequency);
  }
  vTaskDelete(NULL);
}

long leerUltrasonidos() 
{
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    
    long duration = pulseIn(ECHO_PIN, HIGH);
    
    // Calculating the distance
    // Speed of sound wave divided by 2 (go and back)
    return duration * 0.034 / 2;
}

/* Private functions ---------------------------------------------------------*/

/* End of file ****************************************************************/



