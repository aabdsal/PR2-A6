/**
 * @file    buffer_circular.h
 * @author  PR2-A6
 * @version V0.0
 * @date    2026-05-07
 * @brief   Especificación de buffer circular para comunicacion entre tareas
 */

/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef BUFFER_CIRCULAR_H
#define BUFFER_CIRCULAR_H

/* Includes ------------------------------------------------------------------*/
#include <Arduino.h>
#include <stdint.h>

/* Private define ------------------------------------------------------------*/

#define BUFSIZE 10          // Número máximo de elementos
#define PIN_BUTTON 13

/* Private typedef -----------------------------------------------------------*/
typedef enum
{
    LED_APAGADO,
    LED_ENCENDIDO,
    WELDING
} Estado_Led;

typedef enum 
{
    PLANTA_GO,
    PLANTA_STOP
}  Estado_Planta;

typedef struct
{ 
    uint32_t bufIN = 0;            // Índice inferior
    uint32_t bufOUT = 0;           // Índice superior
    uint32_t contador = 0;         // Para contar el nº de elementos
    int colaCirc[BUFSIZE];    // Array de nº enteros

} Buffer_Circ;

typedef struct 
{
    const uint8_t PIN;
    uint32_t numberKeyPresses;
    bool pressed;
} Button;

/* Private macro -------------------------------------------------------------*/
/* Private variables ---------------------------------------------------------*/

/* 
NOTA: extern portMUX_TYPE taskMux; 
Hay que mirar si hay que proteger, si no se elimina esta variable.
*/ 

/* Private function prototypes -----------------------------------------------*/
/* Exported functions --------------------------------------------------------*/

/******************************************************************************/
/**
 * @brief  Inserta un dato en el buffer circular
 * @param  lista Buffer circular
 * @param  dato Dato a insertar
 * @retval 0 si ok, -1 si lleno
 */
uint32_t push(Buffer_Circ *lista, int dato);   

/******************************************************************************/
/**
 * @brief  Extrae un dato del buffer circular
 * @param  lista Buffer circular
 * @param  dato Puntero al dato extraido
 * @retval 0 si ok, -1 si vacio
 */
uint32_t pop(Buffer_Circ *lista, int *dato);   

/******************************************************************************/
/**
 * @brief  Comprueba si el buffer esta lleno
 * @param  lista Buffer circular
 * @retval true si lleno
 */
bool isFull(Buffer_Circ *lista);          

/******************************************************************************/
/**
 * @brief  Comprueba si el buffer esta vacio
 * @param  lista Buffer circular
 * @retval true si vacio
 */
bool isEmpty(Buffer_Circ *lista);         

/******************************************************************************/
/**
 * @brief  Devuelve el numero de elementos en el buffer
 * @param  lista Buffer circular
 * @retval Numero de elementos
 */
uint32_t getTam(Buffer_Circ *lista);      

/******************************************************************************/
/**
 * @brief  Lista el contenido del buffer por serie
 * @param  lista Buffer circular
 * @retval None
 */
void listar(Buffer_Circ *lista);          




#endif // BUFFER_CIRCULAR_H

/* End of file ****************************************************************/