/* mesures de température  par réception de commandes envoyées par la bibiothèque pduino.py 
 * montage: capteur température grove sur A0
 * ref sur 5,0V
 * commandes acceptées: mesure , stop 
 * à la réception de la commande "mesure", le programme envoie la valeur de la température
 * mesurée à partir de A0 sur la liaison série
 */

#include <math.h>
#define TEMPS 400000
#define N_PTS 50

/* TEMPS : durée de la mesure en millisecondes
 * N_PTS : nombre de points de mesure 
 */

unsigned long t_total = TEMPS;
const int B = 4275;           // B value of the thermistor
const long R0 = 100000;       // R0 = 100k
const int pinTempSensor = A0; // Grove - Temperature Sensor connect to A0

void setup() {
  Serial.begin(9600);
  delay(1);
}

void mesures() {
  unsigned long dt = t_total / N_PTS; //en ms
  unsigned long temps_depart = millis();
  unsigned long t_mesure;
  bool ok = true;
  while ((millis() - temps_depart <= t_total) and (ok)) {
    t_mesure = (millis() - temps_depart);
    int a = analogRead(pinTempSensor);
    float R = 1023.0/a - 1.0;
    R = R0*R;
    float temperature = 1.0/(log(R/R0)/B+1/298.15)-273.15; // convert to temperature via datasheet
    Serial.println(String(t_mesure) + "," + String(temperature));
    //un delai personnalisé pour optimiser la mesure du temps
    while ((millis() - temps_depart) - t_mesure < dt) {
      if (Serial.available()) {
        if (Serial.readString() == "stop") {
          ok = false;
        }
      }
    }
  }
  Serial.println("end");
}

void loop() {
  if (Serial.available()) {
    if (Serial.readString() == "mesure") {
        mesures();
    }
  }
}
