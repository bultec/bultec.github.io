/* charge ou décharge d'un condensateur par réception de commandes envoyées par la liaison série
 * pour obtenir une charge rapide, les données sont stockées
 * et envoyées sur la liaison série après la boucle de mesures
 * montage: - un condensateur en série avec  une résistance sur le pin 3
 *            constante de temps d'environ 100 ms avec les valeurs par défaut 
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

#define TEMPS 650
#define N_PTS 75

// condensateur sur EA0, générateur sur EA1
const int pin_led_condo = 3;
const int pin_led_rouge = 4;
const int pin_led_verte = 5;

const int nb = N_PTS;
unsigned long t_total = TEMPS;
unsigned long temps[nb];
int mesures[nb][2];
 
void setup() {
  for (int i=0; i<nb; i++)
    temps[i] = -1;
  t_total = t_total * 1000; //en µs
  pinMode(pin_led_condo, OUTPUT);
  pinMode(pin_led_verte, OUTPUT);
  pinMode(pin_led_rouge, OUTPUT);
  digitalWrite(pin_led_condo, LOW);
  Serial.begin(9600);
  delay(1);
}

void get_mesures(int command) {
  int n = 0;
  unsigned long dt = t_total / (N_PTS-1); //en µs
  unsigned long temps_depart = micros();
  unsigned long t = temps_depart;
  //Serial.println(t_total);
  //Serial.println(dt);
  if (command == 1) {
    digitalWrite(pin_led_verte, HIGH); 
    digitalWrite(pin_led_condo, HIGH); 
  }
  else {
    digitalWrite(pin_led_rouge, HIGH); 
    digitalWrite(pin_led_condo, LOW); 
  }
  while (t - temps_depart <= t_total) {
    temps[n] = (micros() - temps_depart); // t en µs
    mesures[n][0] = analogRead(A0);
    mesures[n][1] = analogRead(A1);
    //Serial.println(t - temps_depart);
    //un delai personnalisé pour optimiser la rapidité
    while ((micros() - temps_depart) - long(n*dt) <= dt) {}
    n = n + 1;
    t = micros();
  }
  digitalWrite(pin_led_verte, LOW);
  digitalWrite(pin_led_rouge, LOW);
}

void envoie_mesures() {
  int n = 0;
  for(int i=0 ; i<nb; i++) {
    if (temps[i] != -1) {
      // le temps est convertit en ms pour compatibilité avec le programe de charge lente condo.ino
      Serial.println(String(float(temps[i])/1000) + "," + String(mesures[i][0]*5.0/1023) + "," + String(mesures[i][1]*5.0/1023));
      n = n+1;
    }
    delay(1);
  }
  //Serial.println(n);
}

void loop() {
  if (Serial.available()) {
    String chaine = Serial.readString();
    if (chaine=="charge") {
      get_mesures(1);
      envoie_mesures();
      Serial.println("end");    
    }
    else if (chaine=="decharge") {
      get_mesures(0);
      envoie_mesures();
      Serial.println("end");
    }
    else {
      Serial.println("commande non reconnue");
    }
  }   
}
