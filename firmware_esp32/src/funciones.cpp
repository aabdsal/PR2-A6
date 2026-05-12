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

/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/

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

long leerUltrasonidos() 
{
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    
    // Timeout de 30ms (30000us) para no bloquear la CPU en caso de fallo o eco muy lejano
    long duration = pulseIn(ECHO_PIN, HIGH, 30000); 
    
    // Calculating the distance
    // Speed of sound wave divided by 2 (go and back)
    return duration * 0.034 / 2;
}

/* Private functions ---------------------------------------------------------*/

/* End of file ****************************************************************/



