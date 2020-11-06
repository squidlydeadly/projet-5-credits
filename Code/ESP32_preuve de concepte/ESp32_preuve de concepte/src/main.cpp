#include <Arduino.h>
#include <Ps3Controller.h>

//*********************************************************************************************************************



void setup()
{
    Serial.begin(115200);
    Ps3.begin("03:A7:77:84:63:25");
    Serial.println("Ready.");
}

void loop()
{
  if (Ps3.isConnected()){
    Serial.println("Connected!");
  }

  delay(3000);
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
