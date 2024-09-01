




Sur une carte Arduino, réaliser le montage suivant:

<img src="images/leds.svg" style="width:250px;">

<img src="images/leds_bb.svg" style="width:550px;">

<img src="images/image_3.jpeg">

- Télécharger le programme leds.ino
- Téléverser le programme dans la carte à l'aide du logiciel Arduino


- Cliquer sur le bouton "Connexion" et sélectionner le port corrspondant à la carte.

Le bouton Rouge allume la led rouge

Le bouton vert allume la led verte

Le bouton Stop éteint les deux leds



L'exemple ici


Le code Javascript nécessaire à cette application est le suivant:

``` javascript
mode = "commande";
commandes = [{texte_bouton:"Rouge", arduino:"rouge"},
             {texte_bouton:"Vert", arduino:"vert"},
             {texte_bouton:"Stop", arduino:"stop"}];
```