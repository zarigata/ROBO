#include <ESP8266WiFi.h>
#include <espnow.h>

// Motor Control Pins
#define MOTOR_A1 D1
#define MOTOR_A2 D2
#define MOTOR_B1 D3
#define MOTOR_B2 D4
#define MOTOR_PWM_A D5
#define MOTOR_PWM_B D6

// ESP-NOW Peer MAC Address (Raspberry Pi's MAC)
uint8_t raspberryPiAddress[] = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF};

// Incoming message structure
typedef struct motor_message {
    char command[20];
    int speed;
} motor_message;

void setup() {
    Serial.begin(115200);
    
    // Motor pin setup
    pinMode(MOTOR_A1, OUTPUT);
    pinMode(MOTOR_A2, OUTPUT);
    pinMode(MOTOR_B1, OUTPUT);
    pinMode(MOTOR_B2, OUTPUT);
    pinMode(MOTOR_PWM_A, OUTPUT);
    pinMode(MOTOR_PWM_B, OUTPUT);
    
    // Initialize ESP-NOW
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
    // Main loop can be used for additional tasks if needed
    delay(10);
}

void onReceiveData(uint8_t *mac, uint8_t *incomingData, uint8_t len) {
    motor_message msg;
    memcpy(&msg, incomingData, sizeof(msg));
    
    Serial.printf("Received command: %s, Speed: %d\n", msg.command, msg.speed);
    
    // Process motor commands
    if (strcmp(msg.command, "forward") == 0) {
        moveForward(msg.speed);
    } else if (strcmp(msg.command, "backward") == 0) {
        moveBackward(msg.speed);
    } else if (strcmp(msg.command, "stop") == 0) {
        stopMotors();
    }
}

void moveForward(int speed) {
    digitalWrite(MOTOR_A1, HIGH);
    digitalWrite(MOTOR_A2, LOW);
    digitalWrite(MOTOR_B1, HIGH);
    digitalWrite(MOTOR_B2, LOW);
    
    analogWrite(MOTOR_PWM_A, speed);
    analogWrite(MOTOR_PWM_B, speed);
}

void moveBackward(int speed) {
    digitalWrite(MOTOR_A1, LOW);
    digitalWrite(MOTOR_A2, HIGH);
    digitalWrite(MOTOR_B1, LOW);
    digitalWrite(MOTOR_B2, HIGH);
    
    analogWrite(MOTOR_PWM_A, speed);
    analogWrite(MOTOR_PWM_B, speed);
}

void stopMotors() {
    digitalWrite(MOTOR_A1, LOW);
    digitalWrite(MOTOR_A2, LOW);
    digitalWrite(MOTOR_B1, LOW);
    digitalWrite(MOTOR_B2, LOW);
    
    analogWrite(MOTOR_PWM_A, 0);
    analogWrite(MOTOR_PWM_B, 0);
}
