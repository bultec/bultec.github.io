/* mesures de tensions par réception de commandes envoyées sur la liaison série
 * montage potentiométrique sur A0
 * ref sur 5,0V
 * commande acceptée: mesure
 * à la réception de la commande "mesure", le programme envoie la valeur
 * mesurée sur l'entrée A0 vers la liaison série
 */

#include <math.h>

float Uref = 5.0;

void setup() {
  Serial.begin(9600);
  delay(1);
}

void loop() {
  if (Serial.available()) {
    // effectue une mesure de la durée tension sur l'antrée A0  
    if (Serial.readString() == "mesure") {
      int a = analogRead(A0);
      float U = float(Uref/1023)*a;
      Serial.println(String(U));
    }
    else {
      Serial.println("error");
    }
  }
}
