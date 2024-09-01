/* allumage de leds par réception de commandes envoyées par la bibiothèque pduino.py 
 * une led rouge (en série avec une résistance de 220 ohms) sur le pin 4
 * une led verte (en série avec une résistance de 220 ohms) sur le pin 5
 * commandes acceptées: rouge, verte, stop
 * 
    Pin 4   Pin 5
      |       |
     +++     +++
     | |     | |
     | |     | |
     +++     +++
      |       |
    --+--   --+--
    \   /   \   /
     \ /     \ /
     -+-     -+-
      |       |
      |       |
     -+-     -+-
     GND     GND
 */
 
const int pin_led_rouge = 4;
const int pin_led_verte = 5;

void setup() {
  pinMode(pin_led_rouge, OUTPUT);
  pinMode(pin_led_verte, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  /* la boucle attend une commande reçue sur la liaison série,
   * réagit en conséquence (allume ou éteint les leds)
   * et renvoie un message (indispensable car la bibliothèque pduino attend une réponse)
   */
  if (Serial.available()) {
    String chaine = Serial.readString();
    String message = "commande non reconnue";
    if (chaine=="rouge") {
      message = "led rouge allumée";
      digitalWrite(pin_led_rouge, HIGH);      
    }
    if (chaine=="vert") {
      message = "led verte allumée";
      digitalWrite(pin_led_verte, HIGH);       
    }
    if (chaine=="stop") {
      message = "leds éteintes";
      digitalWrite(pin_led_rouge, LOW);
      digitalWrite(pin_led_verte, LOW);        
    }
    Serial.println(message);   
  }
}
