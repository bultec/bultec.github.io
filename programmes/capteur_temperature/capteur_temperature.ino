#include <math.h> // Pour utiliser la fonction log()

// Configuration du capteur de température Grove
const int pinCapteur = A1; // Entrée analogique utilisée pour le capteur

// Paramètres du capteur
const float R0 = 10000.0; // Résistance à 25°C (en ohms)
const float B = 3950.0;   // Constante B du thermistor
const float tensionRef = 5.0; // Tension d'alimentation (en volts)
const int resolution = 1023; // Résolution de l'ADC (10 bits)
const float resistancePullup = 10000.0; // Résistance de pull-up (en ohms)

void setup() {
  // Initialisation de la liaison série
  Serial.begin(9600);
}

void loop() {
  // Vérifier si des données sont disponibles sur la liaison série
  if (Serial.available() > 0) {
    // Lire la commande complète envoyée sur la liaison série
    String commande = Serial.readString();
    commande.trim(); // Supprimer les espaces ou sauts de ligne superflus

    // Vérifier si la commande est "vas_y"
    if (commande == "vas_y") {
      mesurerTemperature();
    }
  }
}

// Fonction pour mesurer la température
void mesurerTemperature() {
  int valeurAnalogique = analogRead(pinCapteur); // Lire la valeur brute du capteur
  float tension = (valeurAnalogique / resolution) * tensionRef; // Convertir en tension (en volts)

  // Calcul de la résistance du thermistor
  float resistance = resistancePullup * ((tensionRef / tension) - 1);

  // Calcul de la température en °C
  float temperature = 1.0 / (log(resistance / R0) / B + 1 / 298.15) - 273.15;

  // Envoyer uniquement la mesure de température sur la liaison série
  Serial.println(temperature);
}
