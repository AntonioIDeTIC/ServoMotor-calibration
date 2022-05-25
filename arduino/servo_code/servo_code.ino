#include <Servo.h> // servo library

Servo myservo_htec; // servo variable
Servo myservo_futaba; // servo variable
 
String strAngle; // Angle entered by serial communication
boolean flag = false; // Enable when data is entered by serial communications

int degrees[2] = {0, 0}; // First servo position
int i;

void setup(){
    myservo_futaba.attach(3, 500, 2500);
    myservo_futaba.write(degrees[1]);
    Serial.begin(9600);
    Serial.println("Input Angle 0 ~ 180: ");

}
 
void loop(){
    if(flag == 1){ // Run when serial data is received
        flag = 0;
        int temp = strAngle.toInt();
        strAngle = "";
        if((temp >= 0) && (temp <= 180)){ 
            degrees[1] = temp;
          if(degrees[1] > degrees[0]){
            for(i=degrees[0]; i < degrees[1]; i++){
              myservo_futaba.write(i);
              delay(25);
            }
          }
          else if(degrees[1] < degrees[0]){
             for(i=degrees[0]; i > degrees[1]; i--){
              myservo_futaba.write(i);
              delay(25);
            }
          }
          else{
           Serial.println("Not in range...!!");
          }
        }
        else{ // for error handling
            Serial.println("Please Input Reand 0 ~ 180...!");
        }
        Serial.print("Last Servo position at: ");
        Serial.print(degrees[0]);
        Serial.print("º");
        Serial.println("");
        Serial.println("Input Angle 0 ~ 180: ");
        degrees[0] = degrees[1];
    }
}
 
 
void serialEvent(){
   strAngle = Serial.readStringUntil('\n');
   flag = true;
    
   
}
