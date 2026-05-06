
#define LED_BUILTIN 2


// COMM BAUDS
#define BAUDS 115200

#define LOGGER_ENABLED            // Comentar para deshabilitar el logger por consola serie

#define LOG_LEVEL TRACE           // nivells en c_logger: TRACE, DEBUG, INFO, WARN, ERROR, FATAL, NONE

// DEVICE
//#define DEVICE_ESP_ID             "54CE0361421"   // ESP32 ID
#define DEVICE_GIIROB_PR2_ID      "00" //"giirobpr2_00"

// BUTTON
#define BUTTON_PIN                0

// ULTRASONIC SENSOR
#define TRIG_PIN                  4
#define ECHO_PIN                  5
#define DISTANCIA_EMERGENCIA      10 //10cm de puro placer

// WIFI
#define NET_SSID                  "DIGIFIBRA-RC6D"
#define NET_PASSWD                "S5ZDsNzsR7Re"

// MQTT
#define MQTT_SERVER_IP            "broker.emqx.io"   // IP del broker MQTT al que se conectará el dispositivo
#define MQTT_SERVER_PORT          1883
//#define MQTT_USERNAME             "giirob"    // Descomentar esta línea (y la siguiente) para que se conecte al broker MQTT usando usuario y contraseña
//#define MQTT_PASSWORD             "UPV2024"

#define HELLO_TOPIC               "giirob/pr2/erro/hello"    // TODO: topic ejemplo para ejercicio inicial de saludo de los dispositivos
#define BUTTON_TOPIC              "giirob/pr2/erro/button"
#define EMERGENCY_STOP_TOPIC      "giirob/pr2/erro/emergency_stop"
#define ESTADO_PROCESO_TOPIC      "giirob/pr2/erro/estado_proceso"




