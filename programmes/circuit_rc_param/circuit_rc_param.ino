/* charge ou décharge d'un condensateur par réception de commandes envoyées sur la liason série
 * paramètres : temps et nombre de points de mesure (encodés dans la commande)
 * montage: - un condensateur en série avec  une résistance sur le pin 3
 *            constante de temps d'environ 1,1 s avec les valeurs par défaut 
 *          - pour la visualisation : - une led rouge (en série avec une résistance de 220 ohms) sur le pin 4
 *                                    - une led verte (en série avec une résistance de 220 ohms) sur le pin 5                                                
                                                Pin 4   Pin 5
                                      GND         |       |
 Pin 3                                --+--      +++     +++
  ^                                     |        | |     | |
  |                                     |        | |     | |
  |                              | |    |        +++     +++
  |        +----------+          | |    |         |       |
--+---+----+   R      +---+------+ +----+       --+--   --+--
      |    +----------+   |      | |C           \   /   \   /
      |                   |      | |             \ /     \ /
      |                   |                      -+-     -+-
      |                   |                       |       |
      v                   v                       |       |
       A1                  A0                    -+-     -+-
                                                 GND     GND  
 * la tension aux bornes du condensateur est mesurée sur A0
 * la tension aux bornes du générateur est mesurée sur A1
 * les deux tensions sont renvoyées sous forme d'un entier (0 à 1023)
 * commandes acceptées: charge, decharge
 */


unsigned long N_PTS = 50;
unsigned long t_total = 7000;
// condensateur sur EA0, générateur sur EA1
const int pin_led_condo = 3;
const int pin_led_rouge = 4;
const int pin_led_verte = 5;

void setup() {
    pinMode(pin_led_condo, OUTPUT);
    pinMode(pin_led_verte, OUTPUT);
    pinMode(pin_led_rouge, OUTPUT);
    Serial.begin(9600);
    delay(1);
}

void mesures(int command) {
  float uc = 0;
  float E = 0;
  unsigned long dt = t_total / (N_PTS - 1); //en ms
  unsigned long temps_depart = millis();
  unsigned long t_mesure;
  if (command == 1) {
    digitalWrite(pin_led_verte, HIGH);
    digitalWrite(pin_led_condo, HIGH);
  }
  else {
    digitalWrite(pin_led_rouge, HIGH);
    digitalWrite(pin_led_condo, LOW);
  }
  while (millis() - temps_depart <= t_total) {
    t_mesure = (millis() - temps_depart);
    uc = analogRead(A0) * 5.0 /1023;
    E = analogRead(A1) * 5.0 /1023; 
    Serial.println(String(t_mesure)+","+String(uc)+","+String(E));
    //un delai personnalisé pour optimiser la mesure du temps
    while ((millis() - temps_depart) - t_mesure < dt) {}
  }
  digitalWrite(pin_led_verte, LOW);
  digitalWrite(pin_led_rouge, LOW);
  Serial.println("end");
}

void loop() {
  if (Serial.available()) {
    String chaine = Serial.readString();
    String mots[3];
    int n = split(chaine, ';', mots);
    chaine = mots[0];
    if (mots[1]!="") {
      t_total = mots[1].toInt();
    }
    if (mots[2]!="") {
      N_PTS = mots[2].toInt();
    }
    if (chaine=="charge") {
      mesures(1);          
    }
    else if (chaine=="decharge") {
      mesures(0);      
      }
      else {
        String message = "commande non reconnue";
        Serial.println(message);
      } 
  }
}
