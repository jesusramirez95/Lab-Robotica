#include <Servo.h>
char sensores[50] = {0};
const int trigPin = 8;
const int echoPin = 7;
long duration;
long distance;
int inByte = '0';
int SV1 = 0, SV2 = 0, US = 0;
Servo base;               //Definir objetos servos
Servo shoulder;
Servo elbow;
Servo hand;
int hands = 0;
int elbows = 145;
int shoulders = 1;
int bases = 134;

int pos_base;
int pos_shoulder;
int pos_elbow;

char res;
void setup() {

  Serial.begin(115200);
  pinMode(trigPin, OUTPUT);
  pinMode(echoPin, INPUT);
  hand.attach(10);           //definir conexiones servo
  elbow.attach(11);
  shoulder.attach(12);
  base.attach(13);
  hand.write(0);
  base.write(134);
  shoulder.write(1);
  elbow.write(145);
}

void loop() {

  if (Serial.available()) {
    inByte = Serial.read();
    if (inByte == '1') {    //recoger pieza
      hands = 80;
      shoulders = 72;
      bases = 134;
      base.write(bases);
      delay(10);
      hand.write(hands); //pinza cerrada
      delay(10);
      servo_move_shoulder(shoulders);
      delay(1000);
      Serial.println("nnnn");
    }
    else if (inByte == '2') {         //abandonar pieza
      hands = 80;
      shoulders = 1;
      bases = 50;
      base.write(bases);
      delay(10);
      servo_move_shoulder(shoulders);
      delay(1000);
      hand.write(hands); //pinza cerrada
      delay(1000);
      Serial.println("nnnn");
    }
    else if (inByte == 's') {
      SV1 = analogRead(A0);
      delay(0.02);
      SV2 = analogRead(A1);
      delay(0.02);
      digitalWrite(trigPin, LOW);
      delay(10);
      digitalWrite(trigPin, HIGH);
      delayMicroseconds(10);
      digitalWrite(trigPin, LOW);

      // Read pulse comes from HC-SR04 Echo pin
      duration = pulseIn(echoPin, HIGH);
      // Read echo pulse width
      US = duration / 58;
      delay(0.02);
      String Sensores = String(SV1) + " " + String(SV2) + " " + String(US) + " ";
      Serial.println(Sensores); //enviar string a raspberry pi

    }
  }
  else {
    base.write(134);
    delay(10);
    hand.write(0); //pinza cerrada
    delay(10);
    servo_move_shoulder(1);

  }


}

int ultrasonido() {
  digitalWrite(trigPin, LOW);
  delay(10);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  // Read pulse comes from HC-SR04 Echo pin
  duration = pulseIn(echoPin, HIGH);
  // Read echo pulse width
  distance = duration / 58;

  return distance;

}

void servo_move_shoulder(int x) {
  if (pos_shoulder < x) {
    for (int i = pos_shoulder; i <= x; i += 1) { // goes from 0 degrees to 180 degrees
      // in steps of 1 degree
      shoulder.write(i);              // tell servo to go to position in variable 'pos'
      delay(15);
      pos_shoulder = i;
    }

  }
  else if (pos_shoulder > x) {
    for (int i = pos_shoulder; i >= 0; i -= 1) { // goes from 180 degrees to 0 degrees
      shoulder.write(i);              // tell servo to go to position in variable 'pos'
      delay(15);
      pos_shoulder = i;
    }
  }
  else {
    shoulder.write(pos_shoulder);
    delay(15);
  }
}

