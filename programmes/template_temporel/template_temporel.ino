#define TEMPS // ...
#define N_PTS // ...

unsigned long t_total = TEMPS;
// définition des constantes
// ...

void setup() {
    Serial.begin(9600);
    // ...
    delay(1);
}

void mesures(int command) {
  // ...
  if (command == 1) {
    // ...
  }
  else {
    // ...
  }
  while (millis() - temps_depart <= t_total) {
    t_mesure = (millis() - temps_depart);
    // ...
    // envoi des séries
    Serial.println(String(t_mesure)+","+String(...)+","+String(...));
    //un delai personnalisé pour optimiser la mesure du temps
    while ((millis() - temps_depart) - t_mesure < dt) {}
  }
  /...
  Serial.println("end");
}

void loop() {
  if (Serial.available()) {
    String chaine = Serial.readString();
    if (chaine=="...") {
      mesures(...);          
    }
    else if (chaine=="...") {
           mesures(...);      
         }
         else {
           String message = "commande non reconnue";
           Serial.println(message);
         } 
  }
}
