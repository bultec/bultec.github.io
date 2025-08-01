

int split(String chaine, char separateur, String morceaux[]) {
  /* split un chaine de caractères et renvoie un tableau */  
  const int MAX_MORCEAUX = 10;
  int nb = 0;
  int debut = 0;
  int fin = chaine.indexOf(separateur);
  while (fin != -1 && nb < MAX_MORCEAUX) {
    morceaux[nb++] = chaine.substring(debut, fin);
    debut = fin + 1;
    fin = chaine.indexOf(separateur, debut);
  }
  // Dernier morceau
  if (nb < MAX_MORCEAUX) {
    morceaux[nb++] = chaine.substring(debut);
  }
  return nb;
}
