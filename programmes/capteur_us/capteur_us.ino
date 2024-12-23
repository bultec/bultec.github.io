/* mesures de la célérité des ultrasons par réception de commandes envoyées par la liaison série
 * montage: capteur ultrasons grove sur pin 4
 * commande acceptée: mesure
 * à la réception de la commande "mesure", le programme envoie le temps de parcours
 * aller-retour des ultrasons en µs sur la liaison série
 */

const int pin_Trigger = 4;
const int TIMEOUT = 20000;             // en µs

void setup() {
  pinMode(pin_Trigger, OUTPUT);
  Serial.begin(9600);
  delay(1);
}

unsigned long mesure() {
  unsigned long temps1;
  unsigned long duree_ar;
  pinMode(pin_Trigger, OUTPUT);
  digitalWrite(pin_Trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(pin_Trigger, LOW);
  pinMode(pin_Trigger, INPUT);
  while (digitalRead(pin_Trigger) == LOW) { }
  temps1 = micros();
  while (digitalRead(pin_Trigger) == HIGH and micros() - temps1 < TIMEOUT) { }
  // Attente ECHO passe à l'état bas : la salve d'ondes ultrasonore est revenue
  duree_ar = micros() - temps1;
  return duree_ar;
}

void loop() {
  if (Serial.available()) {
    // effectue une mesure de la durée à la réception du mot "mesure"  
    if (Serial.readString() == "mesure") {
      unsigned long duree_ar = mesure();
      Serial.println(duree_ar);
    }
    else {
      Serial.println("error");
    }
  }
}
