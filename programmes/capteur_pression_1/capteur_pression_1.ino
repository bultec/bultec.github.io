
const float uref = 5.0;

// Résolution de l'ADC (généralement 10 bits, soit une valeur entre 0 et 1023)

void setup() {
  Serial.begin(9600);
}

void loop() {
  float u, k, p;
  delay(100);
  int mesure_A0 = analogRead(A0);
  u = mesure_A0*uref / 1023;
  k = 0.110;
  p = (u-k)*7000/(uref-k);
  Serial.println(p);
}
