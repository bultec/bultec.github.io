/* déclaration des constantes */
// ...

void setup() {
  Serial.begin(9600);
  
  delay(1);
}

void loop() {
  /* la boucle attend une commande reçue sur la liaison série,
   * réagit en conséquence (allume ou éteint les leds)
   * et renvoie un message (indispensable car la bibliothèque pduino attend une réponse)
   */
  if (Serial.available()) {
    String chaine = Serial.readString();
    // remplacer ... par les commandes et les actions respectives
    if (chaine=="...") {
      // ...    
    }
    if (chaine=="...") {
      // ...   
    }
    // ...   
    Serial.println("commande non reconnue");   
  }
}
