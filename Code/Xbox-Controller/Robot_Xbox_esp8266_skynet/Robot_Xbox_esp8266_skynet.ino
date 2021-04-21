#include <ArduinoJson.h>
#include <PubSubClient.h>
//#include <WiFi.h>
#include <ESP8266WiFi.h>
#include <Servo.h>

/* change it with your ssid-password */
//const char* ssid = "COGECO-2D80";
const char* ssid = "TP-Link_90B4";
const char* password = "64460826";
/* this is the IP of PC/raspberry where you installed MQTT Server
  on Wins use "ipconfig"
  on Linux use "ifconfig" to get its IP address */
const char* mqtt_server = "192.168.0.198";
const int port = 1884;

//#define ROBOT_NAME "HUMANITY_0"
//#define ROBOT_NAME "HUMANITY_1"
//#define ROBOT_NAME "SKYNET_0"
#define ROBOT_NAME "SKYNET_1"

/* create an instance of PubSubClient client */
WiFiClient espClient;
PubSubClient client(espClient);

Servo kickservo;

#define servo_pin D7

#define l_motor_pwm_pin D1
//int l_motor_pwm_channel = 1;
#define l_motor_A_pin D2
#define l_motor_B_pin D3

#define r_motor_pwm_pin D6
//int r_motor_pwm_channel = 2;
#define r_motor_A_pin D4
#define r_motor_B_pin D5

int motor_chanel = 0;

int X_pot = 0;
int Y_pot = 0;

/* topics */
//#define update_Topic "update"
//#define ROBO_AXIS_TOPIC "robot/axis"
//define ROBO_BUTTON_TOPIC "robot/button"


long lastMsg = 0;
char msg[20];

void receivedCallback(char* topic, byte* payload, unsigned int length)
{
  lastMsg = micros();
  String inData;
  StaticJsonBuffer<200> jsonBuffer;

  for (int i = 0; i < length; i++) {
    inData += (char)payload[i];
  }
  //Serial.println();
  //Serial.println(topic);
  //Serial.println(inData);
  JsonObject& root = jsonBuffer.parseObject(inData);

  String axis = root["axis"];
  int button = root["button"];

  if (axis != "") {

    X_pot = root["x_axis"];
    Y_pot = root["y_axis"];

    int ratio_X = 400; // on 1000
    int ratio_Y = 1000 - ratio_X; //on 1000

    // INPUTS
    int nJoyX = map(X_pot, -500, 500, -ratio_X, ratio_X); // Joystick X input                     (-128..+127)
    int nJoyY = map(Y_pot, -500, 500, -ratio_Y, ratio_Y); // Joystick Y input                     (-128..+127)

    // OUTPUTS
    int nMotMixL; // Motor (left)  mixed output           (-128..+127)
    int nMotMixR; // Motor (right) mixed output           (-128..+127)

    nMotMixL = nJoyY + nJoyX;
    nMotMixR = nJoyY - nJoyX;

    nMotMixL = map(nMotMixL, -1000, 1000, -1023, 1023);
    nMotMixR = map(nMotMixR, -1000, 1000, -1023, 1023);


    // left motor output
    if (nMotMixL < 0) {
      digitalWrite(l_motor_A_pin, HIGH);
      digitalWrite(l_motor_B_pin, LOW);

    } else {
      digitalWrite(l_motor_A_pin, LOW);
      digitalWrite(l_motor_B_pin, HIGH);
    }
    // right motor output
    if (nMotMixR < 0) {
      digitalWrite(r_motor_A_pin, LOW);
      digitalWrite(r_motor_B_pin, HIGH);

    } else {
      digitalWrite(r_motor_A_pin, HIGH);
      digitalWrite(r_motor_B_pin, LOW);
    }

    // for esp32
    // ledcWrite(r_motor_pwm_channel, abs(nMotMixR));
    // ledcWrite(l_motor_pwm_channel, abs(nMotMixL));

    //for esp8266
    analogWrite(r_motor_pwm_pin, abs(nMotMixR));
    analogWrite(l_motor_pwm_pin, abs(nMotMixL));

    //Serial.println("X axis:" + String(nJoyX) + " Y_axis:" + String(nJoyY));
    Serial.println("L_mot:" + String(nMotMixL) + " R_mot:" + String(nMotMixR) + " compute time: " + String(micros() - lastMsg) );
  }

  if (button != 0) {
    if (button == 13) {
      Serial.println(button);
      Serial.println("kick !!!");
      kickservo.write(0);
      delay(180);
      kickservo.write(90);
    }
  }
}

void mqttconnect()
{
  /* Loop until reconnected */
  while (!client.connected()) {
    Serial.print("MQTT connecting ...");
    /* client ID */
    String clientId = ROBOT_NAME;
    /* connect now */
    if (client.connect(clientId.c_str())) {
      Serial.println("connected");

      client.subscribe(ROBOT_NAME);

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
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  kickservo.attach(servo_pin);
  kickservo.write(90);

  pinMode(r_motor_pwm_pin, OUTPUT);
  pinMode(r_motor_A_pin, OUTPUT);
  pinMode(r_motor_B_pin, OUTPUT);

  pinMode(l_motor_pwm_pin, OUTPUT);
  pinMode(l_motor_A_pin, OUTPUT);
  pinMode(l_motor_B_pin, OUTPUT);

  /* set led as output to control led on-off */
  // ledcSetup(0, 2000, 10);
  // ledcAttachPin(led_pin, motor_chanel);
  // ledcAttachPin(l_motor_pwm_pin, l_motor_pwm_channel);
  // ledcAttachPin(r_motor_pwm_pin, r_motor_pwm_channel);

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
  client.setServer(mqtt_server, port);
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
    analogWrite(r_motor_pwm_pin, 0);
    analogWrite(l_motor_pwm_pin, 0);
    mqttconnect();
  }
  client.loop();
}
