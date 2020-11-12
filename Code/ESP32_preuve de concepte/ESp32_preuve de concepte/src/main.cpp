#include <Arduino.h>
#include <Ps3Controller.h>

//*********************************************************************************************************************


/*********
  Rui Santos
  Complete project details at https://randomnerdtutorials.com  
*********/

// Motor A
int motor1Pin1 = 27; 
int motor1Pin2 = 26; 
int enable1Pin = 14; 

// Setting PWM properties
const int freq = 30000;
const int pwmChannel = 0;
const int resolution = 8;
int dutyCycle = 200;

void setup() {
  // sets the pins as outputs:
  pinMode(motor1Pin1, OUTPUT);
  pinMode(motor1Pin2, OUTPUT);
  pinMode(enable1Pin, OUTPUT);
  
  // configure LED PWM functionalitites
  ledcSetup(pwmChannel, freq, resolution);
  
  // attach the channel to the GPIO to be controlled
  ledcAttachPin(enable1Pin, pwmChannel);

  Serial.begin(115200);

  // testing
  Serial.print("Testing DC Motor...");
}

void loop() {
  // Move the DC motor forward at maximum speed
  Serial.println("Moving Forward");
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, HIGH); 
  delay(2000);

  // Stop the DC motor
  Serial.println("Motor stopped");
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  delay(1000);

  // Move DC motor backwards at maximum speed
  Serial.println("Moving Backwards");
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW); 
  delay(2000);

  // Stop the DC motor
  Serial.println("Motor stopped");
  digitalWrite(motor1Pin1, LOW);
  digitalWrite(motor1Pin2, LOW);
  delay(1000);

  // Move DC motor forward with increasing speed
  digitalWrite(motor1Pin1, HIGH);
  digitalWrite(motor1Pin2, LOW);
  while (dutyCycle <= 255){
    ledcWrite(pwmChannel, dutyCycle);   
    Serial.print("Forward with duty cycle: ");
    Serial.println(dutyCycle);
    dutyCycle = dutyCycle + 5;
    delay(500);
  }
  dutyCycle = 200;
}

//int LED_BUILTIN = 2;
//void setup() {

//Ps3.begin("01:02:03:04:05:06");
//pinMode (LED_BUILTIN, OUTPUT);
//}
//void loop() {
//digitalWrite(LED_BUILTIN, HIGH);
//delay(1000);
////digitalWrite(LED_BUILTIN, LOW);
////delay(1000);
//}

//********************************************************************************************************************************
//Standard DLL Speed control

// int E1 = 4; //M1 Speed Control
// int E2 = 7; //M2 Speed Control
// int M1 = 5; //M1 Direction Control
// int M2 = 6; //M1 Direction Control

// //When m1p/m2p is 127, it stops the motor
// //when m1p/m2p is 255, it gives the maximum speed for one direction
// //When m1p/m2p is 0, it gives the maximum speed for reverse direction

// // setting PWM properties
// const int freq = 5000;
// const int ledChannel = 0;
// const int resolution = 8;

// void DriveMotorP(byte m1p, byte m2p) //Drive Motor Power Mode
// {

//   digitalWrite(E1, HIGH);
//   //analogWrite(M1, (m1p));
//   ledcWrite(M1, (m1p));
//   digitalWrite(E2, HIGH);
//   //analogWrite(M2, (m2p));
//   ledcWrite(M2, (m2p));
// }

// void setup(void)
// {
//   int i;
//   for (i = 4; i <= 7; i++)
//     pinMode(i, OUTPUT);
//   Serial.begin(19200); //Set Baud Rate

//   ledcSetup(ledChannel, freq, resolution);

//   // attach the channel to the GPIO to be controlled
//   ledcAttachPin(M1, ledChannel);
//   ledcAttachPin(M2, ledChannel);
// }

// void loop(void)
// {
//   if (Serial.available())
//   {
//     char val = Serial.read();
//     if (val != -1)
//     {
//       switch (val)
//       {
//       case 'w':                  //Move Forward
//         DriveMotorP(0xff, 0xff); // Max speed
//         break;
//       case 'x': //Move Backward
//         DriveMotorP(0x00, 0x00);
//         ; // Max speed
//         break;
//       case 's': //Stop
//         DriveMotorP(0x7f, 0x7f);
//         break;
//       }
//     }
//   }
// }

//*********************************************************************************************************************************************************************
