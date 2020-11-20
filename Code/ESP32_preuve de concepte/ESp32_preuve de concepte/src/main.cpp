#include <Arduino.h>




//*********************************************************************************************************************************************************************
// get bluetooth addrress
#include <PS4Controller.h>


void setup()
{
    Serial.begin(9600);
    PS4.begin("01:01:01:01:01:01");
    Serial.println("Ready.");
}

void loop()
{
  if (PS4.isConnected()){
    Serial.println("Connected!");
  }

  delay(1000);
}