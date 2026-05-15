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

uint8_t ledStatus = 0;
static bool ledRemoteLocked = false; /* When true, button presses won't change the LED; remote commands control it */
bool emergencyLatched = false;
volatile bool button_pressed_flag = false;

/* Private function prototypes -----------------------------------------------*/

/* Exported functions --------------------------------------------------------*/

void IRAM_ATTR button_isr() 
{
    button_pressed_flag = true;
}

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
        digitalWrite(LED_PIN, HIGH);
    } 
    else 
    {
        infoln("Led: off");
        digitalWrite(LED_PIN, LOW);
    }
}

long leerUltrasonidos() 
{
    digitalWrite(TRIG_PIN, LOW);
    delayMicroseconds(2);
    digitalWrite(TRIG_PIN, HIGH);
    delayMicroseconds(10);
    digitalWrite(TRIG_PIN, LOW);
    
    unsigned long duration = pulseIn(ECHO_PIN, HIGH);
    return (long)(duration * 0.034 / 2);
}

void led_task(void *pvParameters)
{
    Buffer_Circ* buff_led = (Buffer_Circ*) pvParameters;

    const TickType_t xFrequency = pdMS_TO_TICKS(100);
    TickType_t xLastWakeTime = xTaskGetTickCount();
    
    int orden_recibida;

    /* while(!PARAR) */
    for(;;)
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

void ultrasonidos_task(void *pvParameters)
{
    Buffer_Circ* buff_prod = (Buffer_Circ*) pvParameters;
    const TickType_t xFrequency = pdMS_TO_TICKS(250);
    TickType_t xLastWakeTime = xTaskGetTickCount();
    
    /* while(!PARAR)*/
    for(;;)
    {
        long lectura_ultrasonidos = leerUltrasonidos();
        
        if(lectura_ultrasonidos < DISTANCIA_EMERGENCIA)
        {
            if(!emergencyLatched)
            {
                push(buff_prod, PLANTA_STOP);
                emergencyLatched = true;
            }
        }
        else if(emergencyLatched)
        {
            push(buff_prod, PLANTA_GO);
            emergencyLatched = false;
        }
        vTaskDelayUntil(&xLastWakeTime, xFrequency);
    }
    vTaskDelete(NULL);
}

void handle_mqtt_task(void *pvParameters)
{
    Buffer_Circ* buff_cons = (Buffer_Circ*) pvParameters;
    const TickType_t xFrequency = pdMS_TO_TICKS(100);
    TickType_t xLastWakeTime = xTaskGetTickCount();
    int estado_recibido;

    /*while(!PARAR)*/
    for(;;)
    {
        if(pop(buff_cons, &estado_recibido) == 0)
        {
            JsonDocument doc;
            if(estado_recibido == PLANTA_GO)
            {
                doc["estado_simulacion"] = "GO";
                String payload;
                serializeJson(doc, payload);

                enviarMensajePorTopic(EMERGENCY_STOP_TOPIC, payload);
                Serial.println("EMERGENCY CLEARED!");
            }
            else
            {
                doc["estado_simulacion"] = "STOP";

                String payload;
                serializeJson(doc, payload);

                enviarMensajePorTopic(EMERGENCY_STOP_TOPIC, payload);
                Serial.println("EMERGENCY STOP!");
            }
        }
        vTaskDelayUntil(&xLastWakeTime, xFrequency);
    }
    vTaskDelete(NULL);
}
/* Private functions ---------------------------------------------------------*/

/* End of file ****************************************************************/



