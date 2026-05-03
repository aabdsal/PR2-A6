#include <Arduino.h>

#define BUFSIZE 10          // Número máximo de elementos
#define PIN_BUTTON 13
portMUX_TYPE taskMux = portMUX_INITIALIZER_UNLOCKED; // Mutex para la sección crítica

/* 
    NOTA: Uso de uint32_t en vez de int para asegurar 32 bits, 
    son buenas prácticas de programación de sistemas empotrados
*/

typedef struct
{ 
  uint32_t bufIN = 0;            // Índice inferior
  uint32_t bufOUT = 0;           // Índice superior
  uint32_t contador = 0;         // Para contar el nº de elementos
  uint32_t colaCirc[BUFSIZE];    // Array de nº enteros

} Buffer_Circ;

typedef struct 
{
  const uint8_t PIN;
  uint32_t numberKeyPresses;
  bool pressed;
} Button;

volatile Button button1 = {PIN_BUTTON, 0, false}; // Regla 1.8 del barr-c, declarar variable global que es accecida por una ISR
Buffer_Circ lista;

uint32_t push(Buffer_Circ *lista, uint32_t dato);   // Insertar dato en buffer
uint32_t pop(Buffer_Circ *lista, uint32_t *dato);   // Eliminar dato de buffer
bool isFull(Buffer_Circ *lista);          // Comprobar si esta lleno el buffer
bool isEmpty(Buffer_Circ *lista);         // Comprobar si esta vacio el buffer
uint32_t getTam(Buffer_Circ *lista);      // Funcion para acceder al tamaño del buffer
void listar(Buffer_Circ *lista);          // Listar los elementos del buffer

/* 
    WARNING:
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

// Interrupción que hace el papel de un productor e intenta evitar rebotes (aunque no me acaba de funcionar)
void IRAM_ATTR productor_isr() 
{
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

// Es la encargada de consumir el elemento que hay en el buffer
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

void setup() 
{
  Serial.begin(115200);
  pinMode(button1.PIN, INPUT_PULLUP);
  attachInterrupt(button1.PIN, productor_isr, FALLING);
  xTaskCreatePinnedToCore(consumidor, "consumidor", 10000, NULL, 1, NULL, 1);
}

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

//  Insertar dato
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

// Sacar dato
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

// Ver si esta lleno
bool isFull(Buffer_Circ *lista)
{
  if(lista->contador == BUFSIZE)
  {
    return true;
  }
  return false;
}
// Ver si esta vacío
bool isEmpty(Buffer_Circ *lista)
{
  if(lista->contador == 0)
  {
    return true;
  }
  return false;
}

// Listar el contenido
void listar(Buffer_Circ *lista)
{
  for(uint32_t i = 0; i < lista->contador; i++)
  {
    Serial.printf("Elemento nº %d: %d", i, lista->colaCirc[i]);
  }
}

//Conocer la cantidad de datos que alberga
uint32_t getTam(Buffer_Circ *lista)
{
  return lista->contador;
}


