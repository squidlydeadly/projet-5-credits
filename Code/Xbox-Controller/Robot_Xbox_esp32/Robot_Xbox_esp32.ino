/* Here ESP32 will keep 2 roles: 
1/ read data from DHT11/DHT22 sensor
2/ control led on-off
So it willpublish temperature topic and scribe topic bulb on/off
*/

#include <ArduinoJson.h>
#include <PubSubClient.h>
#include <WiFi.h>
#include <ESP32Servo.h>
//#include <ESP8266WiFi.h>

/* change it with your ssid-password */
const char* ssid = "rasp_wifi";
const char* password = "rpi3_2356";
/* this is the IP of PC/raspberry where you installed MQTT Server 
on Wins use "ipconfig" 
on Linux use "ifconfig" to get its IP address */
const char* mqtt_server = "192.168.0.217";

/* create an instance of PubSubClient client */
WiFiClient espClient;
PubSubClient client(espClient);
//neopixel

Servo myservo;

#define servo_pin 21

#define l_motor_pwm_pin 26
int l_motor_pwm_channel = 1;
#define l_motor_A_pin 25
#define l_motor_B_pin 33

#define r_motor_pwm_pin   32
int r_motor_pwm_channel = 2;
#define r_motor_A_pin 11
#define r_motor_B_pin 10


const char* Axis_Topic = "robot/axis";
const char* Button_Topic = "robot/button";

int motor_chanel = 0;

int X_pot = 0;
int Y_pot = 0;

/* topics */
#define update_Topic "update"
#define ROBO_AXIS_TOPIC "robot/axis"
#define ROBO_BUTTON_TOPIC "robot/button"

long lastMsg = 0;
char msg[20];

void receivedCallback(char* topic, byte* payload, unsigned int length)
{
    String inData;
    StaticJsonBuffer<200> jsonBuffer;

    for (int i = 0; i < length; i++) {
        //Serial.print((char)payload[i]);
        inData += (char)payload[i];
    }
    //Serial.println();
    //Serial.println(topic);
    //Serial.println(inData);
    JsonObject& root = jsonBuffer.parseObject(inData);

    String axis = root["axis"];
    int button = root["button"];

    //Serial.println(axis);
    //Serial.println(button);

    if (axis != "") {
        Serial.println(axis);
        if (axis == "l_thumb_x") {
            X_pot = root["value"];
            if (abs(X_pot) < 150)
                X_pot = 0;

        } else if (axis == "l_thumb_y") {
            Y_pot = root["value"];
            if (abs(Y_pot) < 150)
                Y_pot = 0;
        }

    
// INPUTS
    int nJoyX = map(X_pot, -500, 500, -512, 512); // Joystick X input                     (-128..+127)
    int nJoyY = map(Y_pot, -500, 500, -512, 512);
    ; // Joystick Y input                     (-128..+127)

    // OUTPUTS
    int nMotMixL; // Motor (left)  mixed output           (-128..+127)
    int nMotMixR; // Motor (right) mixed output           (-128..+127)

    // CONFIG
    // - fPivYLimt  : The threshold at which the pivot action starts
    //                This threshold is measured in units on the Y-axis
    //                away from the X-axis (Y=0). A greater value will assign
    //                more of the joystick's range to pivot actions.
    //                Allowable range: (0..+127)
    float fPivYLimit = 72.0;

    // TEMP VARIABLES
    float nMotPremixL; // Motor (left)  premixed output        (-128..+127)
    float nMotPremixR; // Motor (right) premixed output        (-128..+127)
    int nPivSpeed; // Pivot Speed                          (-128..+127)
    float fPivScale; // Balance scale b/w drive and pivot    (   0..1   )

    // Calculate Drive Turn output due to Joystick X input
    if (nJoyY >= 0) {
        // Forward
        nMotPremixL = (nJoyX >= 0) ? 1023.0 : (1023.0 + nJoyX);
        nMotPremixR = (nJoyX >= 0) ? (1023.0 - nJoyX) : 1023.0;
    } else {
        // Reverse
        nMotPremixL = (nJoyX >= 0) ? (1023.0 - nJoyX) : 1023.0;
        nMotPremixR = (nJoyX >= 0) ? 1023.0 : (1023.0 + nJoyX);
    }

    // Scale Drive output due to Joystick Y input (throttle)
    nMotPremixL = nMotPremixL * nJoyY / 1023.0;
    nMotPremixR = nMotPremixR * nJoyY / 1023.0;

    // Now calculate pivot amount
    // - Strength of pivot (nPivSpeed) based on Joystick X input
    // - Blending of pivot vs drive (fPivScale) based on Joystick Y input
    nPivSpeed = nJoyX;
    fPivScale = (abs(nJoyY) > fPivYLimit) ? 0.0 : (1.0 - abs(nJoyY) / fPivYLimit);

    // Calculate final mix of Drive and Pivot
    nMotMixL = (1.0 - fPivScale) * nMotPremixL + fPivScale * (nPivSpeed);
    nMotMixR = (1.0 - fPivScale) * nMotPremixR + fPivScale * (-nPivSpeed);

    // nMotMixL = map(nMotMixL, -1024, 1014, -512, 512);
    // nMotMixR = map(nMotMixR, -1024, 1014, -512, 512);

    // left motor output
    if (nMotMixL < 0) {
        digitalWrite(l_motor_A_pin, 1);
        digitalWrite(l_motor_B_pin, 0);

    } else {
        digitalWrite(l_motor_A_pin, 0);
        digitalWrite(l_motor_B_pin, 1);
    }
    // right motor output
    if (nMotMixR < 0) {
        digitalWrite(r_motor_A_pin, 0);
        digitalWrite(r_motor_B_pin, 1);

    } else {
        digitalWrite(r_motor_A_pin, 1);
        digitalWrite(r_motor_B_pin, 0);
    }

     ledcWrite(r_motor_pwm_channel, abs(nMotMixR));
     ledcWrite(l_motor_pwm_channel, abs(nMotMixL));

    //analogWrite(r_motor_pwm_pin, abs(nMotMixR));
    //analogWrite(l_motor_pwm_pin, abs(nMotMixL));
    //}
    Serial.println("X axis:" + String(nJoyX) + " Y_axis:" + String(nJoyY));
    Serial.println("L mot:" + String(nMotMixL) + " R mot:" + String(nMotMixR));
    // if (axis == "right_trigger") {
    //     ledcWrite(motor_chanel, root["value"]);
    // }

        
    }


    else if(button != 0){
        if(button == 13){
            Serial.println(button);
            Serial.println("kick !!!");
            myservo.write(0);
            delay(250);
            myservo.write(90);
        }
        
    }

    
}

void mqttconnect()
{
    /* Loop until reconnected */
    while (!client.connected()) {
        Serial.print("MQTT connecting ...");
        /* client ID */
        String clientId = "ESP32Client";
        /* connect now */
        if (client.connect(clientId.c_str())) {
            Serial.println("connected");
            /* subscribe topic with default QoS 0*/
            client.subscribe(ROBO_AXIS_TOPIC);
            client.subscribe(ROBO_BUTTON_TOPIC);

            client.publish(update_Topic, "1");
            Serial.println("send update");

        } else {
            Serial.print("failed, status code =");
            Serial.print(client.state());
            Serial.println("try again in 5 seconds");
            /* Wait 5 seconds before retrying */
            delay(5000);
        }
    }
}

void setup()
{
    Serial.begin(115200);
    // We start by connecting to a WiFi network
    Serial.println();
    Serial.print("Connecting to ");
    Serial.println(ssid);

    //pinMode(led_pin, OUTPUT);

    //pinMode(r_motor_pwm_pin, OUTPUT);
    pinMode(r_motor_A_pin, OUTPUT);
    pinMode(r_motor_B_pin, OUTPUT);

    //pinMode(l_motor_pwm_pin, OUTPUT);
    pinMode(l_motor_A_pin, OUTPUT);
    pinMode(l_motor_B_pin, OUTPUT);

    /* set led as output to control led on-off */
    ledcSetup(0, 2000, 10);
    
    ledcAttachPin(l_motor_pwm_pin, l_motor_pwm_channel);
    ledcAttachPin(r_motor_pwm_pin, r_motor_pwm_channel);
    ESP32PWM::allocateTimer(0);
	ESP32PWM::allocateTimer(1);
	ESP32PWM::allocateTimer(2);
	//ESP32PWM::allocateTimer(3);
    myservo.setPeriodHertz(50);
    //myservo.attach(servo_pin, 500, 2400);
    myservo.write(0); 

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("");
    Serial.println("WiFi connected");
    Serial.println("IP address: ");
    Serial.println(WiFi.localIP());

    /* configure the MQTT server with IPaddress and port */
    client.setServer(mqtt_server, 1883);
    /* this receivedCallback function will be invoked 
  when client received subscribed topic */
    client.setCallback(receivedCallback);
    /*start DHT sensor */
    delay(50);
}
void loop()
{
    /* if client was disconnected then try to reconnect again */
    if (!client.connected()) {
        mqttconnect();
    }

    client.loop();
}
