/* mesures de pression par réception de commandes envoyées par la bibiothèque pduino.py 
 * montage: capteur pression grove sur A0
 * ref sur 5,0V
 * commande acceptée: mesure
 * à la réception de la commande "mesure", le programme envoie la valeur numérique (entre 0 et 1023)
 * de A0 sur la liaison série
 */
const int pin_capteur_pression = A0;
const float uref = 5.0;

void setup() {
  Serial.begin(9600);
  delay(1);
}

void loop() {
  if (Serial.available()) {
    if (Serial.readString() == "mesure") {
      float u, k, p;
      int mesure_A0 = analogRead(pin_capteur_pression);
      u = mesure_A0*uref / 1023;
      k = 0.110;
      p = (u-k)*7000/(uref-k);
      Serial.println(p);         
    }
  }     
}
