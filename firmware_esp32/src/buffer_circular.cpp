/**
 * @file    buffer_circular.cpp
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-06
 * @brief   Ejemplo de cola circular con mutex  
 */

/* Includes ------------------------------------------------------------------*/
#include "buffer_circular.h"
/* Private typedef -----------------------------------------------------------*/
/* Private define ------------------------------------------------------------*/
/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/
Buffer_Circ lista;
portMUX_TYPE taskMux = portMUX_INITIALIZER_UNLOCKED;
/* Private function prototypes -----------------------------------------------*/
/* Exported functions --------------------------------------------------------*/
/* Private functions ---------------------------------------------------------*/

uint32_t push(Buffer_Circ *lista, int dato)
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

uint32_t pop(Buffer_Circ *lista, int *dato)
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

/* End of file ****************************************************************/