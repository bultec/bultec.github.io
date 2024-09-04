/* mesures de tensions par réception de commandes envoyées sur la liaison série
 * montage potentiométrique sur A0
 * ref sur 5,0V
 * commandes acceptées: mesure, stop
 * à la réception de la commande "mesure", le programme envoie les valeurs
 * mesurées sur l'entrée A0 vers la liaison série
 * les mesures peuvent^êtres arrêtées en envoyant la commande "stop"
 */

#include <math.h>
#define TEMPS 20000
#define N_PTS 250

/* TEMPS : durée de la mesure en millisecondes
 * N_PTS : nombre de points de mesure 
 */

unsigned long t_total = TEMPS;
float Uref = 5.0;

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
    int a = analogRead(A0);
    float U = float(Uref/1023)*a;
    Serial.println(String(t_mesure) + "," + String(U));
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
