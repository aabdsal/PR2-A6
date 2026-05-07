/**
 * @file    colaCirc_mutex.cpp
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Ejemplo de cola circular con mutex (comentado)
 */
#if 0
/* Includes ------------------------------------------------------------------*/
#include "buffer_circular.h"
/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/
volatile Button button1 = {PIN_BUTTON, 0, false}; // Regla 1.8 del barr-c, declarar variable global que es accecida por una ISR
Buffer_Circ lista;

/* Private function prototypes -----------------------------------------------*/
/* Exported functions --------------------------------------------------------*/
/* Private functions ---------------------------------------------------------*/

/******************************************************************************/
/**
 * @brief  Interrupcion que actua como productor del buffer circular
 * @retval None
 */
void IRAM_ATTR productor_isr() 
{
    /* WARNING:
    portENTER_CRITICAL deshabilita las interrupciones
    (está en la última diapositiva del tema de semáforos y mutex de PR2)
    y el planificador de tareas, por lo que la función Serial, que usa 
    internamente semáforos, se queda bloqueada esperando indefinidamente, 
    ya que el planificador no puede ceder la CPU, detecta ese bloqueo y lanza error. 
    
    La solución es hacer cualquier I/O fuera de las secciones 
    críticas y ISR, con solo accesos a memoria compartida, 
    con variables locales que copien los datos protegidos antes 
    de salir de la sección crítica (Ejemplo de uso en la sección crítica del loop).
    */ 

    static uint32_t lastTime = 0; // Variable que no se reinicia a 0 cada vez que hay un ISR, sino que mantiene el valor de lastTime = now;
    uint32_t now = esp_timer_get_time(); // En microsegundos

    /* 
    NOTA: Técnica de debounce por software, 
    vista en IIS, en el tema de buenas prácticas, 
    no es la mejor pero es la más fácil de implementar.
    */
  
    if (now - lastTime < 50000)
    {  
      return;
    }
    lastTime = now;

    button1.numberKeyPresses += 1;
    portENTER_CRITICAL_ISR(&taskMux);
    push(&lista, button1.numberKeyPresses);
    portEXIT_CRITICAL_ISR(&taskMux); 
    button1.pressed = true;
}

/******************************************************************************/
/**
 * @brief  Tarea que consume elementos del buffer circular
 * @param  pvParameters Parametros de la tarea (no usado)
 * @retval None
 */
void consumidor (void *pvParameters) 
{
    uint32_t dato = 0;
    for(;;)
    {
        portENTER_CRITICAL(&taskMux); 
        uint32_t res = pop(&lista, &dato);
        portEXIT_CRITICAL(&taskMux);

        if(!res)
        {
        Serial.printf("Elemento %d eliminado\n", dato);
        }

    }
    vTaskDelete(NULL);
}

/******************************************************************************/
/**
 * @brief  Configura pines y crea la tarea consumidora
 * @retval None
 */
void setup() 
{
    Serial.begin(115200);
    pinMode(button1.PIN, INPUT_PULLUP);
    attachInterrupt(button1.PIN, productor_isr, FALLING);
    xTaskCreatePinnedToCore(consumidor, "consumidor", 10000, NULL, 1, NULL, 1);
}

/******************************************************************************/
/**
 * @brief  Lee el estado del boton y procesa eventos
 * @retval None
 */
void loop() 
{
    bool pressed;
    uint32_t presses;

    portENTER_CRITICAL(&taskMux);
    pressed = button1.pressed;
    if (pressed) 
    {
      presses = button1.numberKeyPresses;
      button1.pressed = false;
    }
    portEXIT_CRITICAL(&taskMux);

    if (pressed)
    {
      Serial.printf("Elemento %u añadido por el botón\n", presses);
    }
}

uint32_t push(Buffer_Circ *lista, uint32_t dato)
{
    if(isFull(lista))
    { 
        return -1;
    }

    lista->colaCirc[lista->bufIN] = dato;
    lista->bufIN = (lista->bufIN + 1) % BUFSIZE;
    lista->contador++;

    return 0;
}

uint32_t pop(Buffer_Circ *lista, uint32_t *dato)
{
    if(isEmpty(lista))
    {
        return -1;
    }

    *dato = lista->colaCirc[lista->bufOUT];
    lista->colaCirc[lista->bufOUT] = 0;
    lista->bufOUT = (lista->bufOUT + 1) % BUFSIZE;
    lista->contador--;
  
    return 0;
}

bool isFull(Buffer_Circ *lista)
{
    if(lista->contador == BUFSIZE)
    {
        return true;
    }
    return false;
}

bool isEmpty(Buffer_Circ *lista)
{
    if(lista->contador == 0)
    {
        return true;
    }
    return false;
}

void listar(Buffer_Circ *lista)
{
    for(uint32_t i = 0; i < lista->contador; i++)
    {
        Serial.printf("Elemento nº %d: %d", i, lista->colaCirc[i]);
    }
}

uint32_t getTam(Buffer_Circ *lista)
{
    return lista->contador;
}


#endif

/* End of file ****************************************************************/