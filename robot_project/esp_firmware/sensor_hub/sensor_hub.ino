#include <ESP8266WiFi.h>
#include <espnow.h>
#include <Wire.h>
#include <VL53L0X.h>  // Time-of-Flight distance sensor

VL53L0X distanceSensor;

// ESP-NOW Peer MAC Address (Raspberry Pi's MAC)
uint8_t raspberryPiAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

// Sensor data message structure
typedef struct sensor_message {
    float distance;
    float temperature;
    float humidity;
} sensor_message;

// Incoming request structure
typedef struct sensor_request {
    char sensor[20];
} sensor_request;

void setup() {
    Serial.begin(115200);
    Wire.begin();

    // Initialize Time-of-Flight sensor
    distanceSensor.init();
    distanceSensor.setTimeout(500);
    distanceSensor.setMeasurementTimingBudget(20000);  // High accuracy mode

    // WiFi and ESP-NOW Setup
    WiFi.mode(WIFI_STA);
    if (esp_now_init() != 0) {
        Serial.println("ESP-NOW initialization failed");
        return;
    }

    // Register peer
    esp_now_set_self_role(ESP_NOW_ROLE_SLAVE);
    esp_now_add_peer(raspberryPiAddress, ESP_NOW_ROLE_SLAVE, 1, NULL, 0);

    // Register receive callback
    esp_now_register_recv_cb(onReceiveData);
}

void loop() {
    // Periodic sensor readings can be added here if needed
    delay(10);
}

void onReceiveData(uint8_t *mac, uint8_t *incomingData, uint8_t len) {
    sensor_request req;
    memcpy(&req, incomingData, sizeof(req));

    sensor_message sensorData;
    
    if (strcmp(req.sensor, "distance") == 0) {
        sensorData.distance = readDistanceSensor();
    } else if (strcmp(req.sensor, "environment") == 0) {
        // Placeholder for additional sensor data
        sensorData.temperature = readTemperature();
        sensorData.humidity = readHumidity();
    }

    // Send sensor data back to Raspberry Pi
    esp_now_send(raspberryPiAddress, (uint8_t *) &sensorData, sizeof(sensorData));
}

float readDistanceSensor() {
    return distanceSensor.readRangeSingleMillimeters() / 10.0;  // Convert to cm
}

float readTemperature() {
    // Placeholder - replace with actual temperature sensor reading
    return 25.5;
}

float readHumidity() {
    // Placeholder - replace with actual humidity sensor reading
    return 45.0;
}
