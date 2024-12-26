/* mesure de la célérité des ultrasons par réception de commande envoyée par la liaison série
 * pour obtenir des mesures rapides, le temps ainsi que les valeurs de l'état du pin 4 sont stockées
 * puis envoyées sur la liaison série après la boucle de mesures
 * montage: capteur ultrasons sur pin 4
 * l'état du pin 4 est stocké sous forme d'un entier (0 ou 1)
 * commande acceptée: mesure
 */

// mesures de 200 points pendant de durée de 5 ms
#define TEMPS 5
#define N_PTS 200

const int pin_Trigger = 4;
const int TIMEOUT = 20000;  // en µs

const int nb = N_PTS;
unsigned long t_total = TEMPS;
unsigned long temps[nb];
int mesures[nb];
 
void setup() {
  for (int i=0; i<nb; i++)
    temps[i] = -1;
  t_total = t_total * 1000; //en µs
  pinMode(pin_Trigger, OUTPUT);
  Serial.begin(9600);
  delay(1);
}

void get_mesures() {
  int n = 0;
  unsigned long dt = t_total / (N_PTS); //en µs
  pinMode(pin_Trigger, OUTPUT);
  digitalWrite(pin_Trigger, HIGH);
  delayMicroseconds(10);
  digitalWrite(pin_Trigger, LOW);
  pinMode(pin_Trigger, INPUT);
  unsigned long temps_depart = micros();
  unsigned long t = temps_depart;
  while (t - temps_depart <= t_total) {
    temps[n] = (micros() - temps_depart); // t en µs
    mesures[n] = digitalRead(pin_Trigger);
    //un delai personnalisé pour optimiser la rapidité
    while ((micros() - temps_depart) - long(n*dt) <= dt) {}
    n = n + 1;
    t = micros();
  }
}

void envoie_mesures() {
  int n = 0;
  for(int i=0 ; i<nb; i++) {
    if (temps[i] != -1) {
      Serial.println(String(long(temps[i])) + "," + String(mesures[i]));
      n = n+1;
    }
    delay(1);
  }
  //debogage
  //Serial.println(n);
}

void loop() {
 if (Serial.available()) {
  String C = Serial.readString();
  if (C == "mesure") {
    get_mesures();
    envoie_mesures();
    Serial.println("end");    
  }
  else {
    Serial.println(C);
    Serial.println("commande non reconnue");
  } 
 }
}
