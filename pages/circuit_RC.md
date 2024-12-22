# Circuit RC - Montage sans déclenchement

La charge ou la décharge d'un condensateur à travers une résistance est un cas d'école pour illustrer toutes les possibilité des mesures temporelle offertes par la biblothèque `web-sciences`.

**Important**

Comme dans tous les exemples utilisant `web-sciences` le dialogue entre le programme _Javascript_ et la carte _arduino_  doit impérativement suivre le protocole suivant:

- le programme _python_ envoie une commande sous forme de chaine de caractères sur la liaison série.
- le programme _arduino_ reçoit la commande, la traite et envoie une réponse sur la liaison série.

## I. Montage
Dans ce montage, c'est le programme qui déclenche la charge du condensateur en plaçant le pin 3 l'état haut au début des mesures.

#### Montage 

<img src="images/circuit_rc_1_schema.svg" style = "width:800px">

![](images/circuit_rc_bb.svg)

Les leds sont présentes uniquement dans un but de visualisation. Il est possible de les supprimer.

### Code arduino

Deux versions du programme sont fournies&nbsp;:

- le programme  [condo.ino](../../arduino/condo/condo.ino) pour lequel la constante de temps du circuit peut être de quelques secondes qui envoie les valeurs de $E$ (tension aux bornes du circuit) et de $u_c$ (tension aux bornes du condensateur) sur la liaison série après chaque mesure.
- le programme  [condo_rapide.ino](../../arduino/condo_rapide/condo_rapide.ino) pour lequel la constante de temps du circuit peut être de quelques centaines de millisecondes qui, dans un but de rapidité, envoie les toutes valeurs une fois que les mesures sont terminées.

##### Fonctionnement

Le programme:

- attend l'arrivée d'une commande (`charge` ou `decharge`) sur la liaison série et réagit en conséquence:
- si la commande est `charge`, il place le pin 3 à l'état haut et effectue la série de mesure. Chaque mesure est envoyée sur la liaison série juste après sa réalisation. la série se termine par l'envoi du mot `end`.
- si la commande est `decharge`, il place le pin 3 à l'état bas  et effectue la série de mesures comme précédement.

### Code python
Le programme _javascript_

    Le code _Javascript_ à utiliser est le suivant :
    
```javascript
    mode = "temporel";
    var commandes = [{texte_bouton:"Charge", arduino:"charge"},
                     {texte_bouton:"Décharge", arduino:"decharge"}];
    var series = [{grandeur: "Uc", unite: "V"}, {grandeur: "E", unite: "V"}];
    var titre_graphe = "Circuit RC";
    var axes = [{grandeur: "t", unite: "ms"}, {grandeur: "U", unite: "V"}];
```

Le code complet à insérer dans une cellule _Jupyter_

```python
    from IPython.display import HTML, display
    from web_sciences import get_interface

    my_init = '''
    mode = "temporel";
    var commandes = [{texte_bouton:"Charge", arduino:"charge"},
                     {texte_bouton:"Décharge", arduino:"decharge"}];
    var series = [{grandeur: "Uc", unite: "V"}, {grandeur: "E", unite: "V"}];
    var titre_graphe = "Circuit RC";
    var axes = [{grandeur: "t", unite: "ms"}, {grandeur: "U", unite: "V"}];
    '''

    S = get_interface(my_init)
    display(HTML(S))
```

- envoie une commande parmi `charge` ou `decharge` ou sur la liaison série.
- recupère les données lues sur la liaison série.
- affiche le graphe $U = f(t)$.


### Exemple d'éxécution

ici images

ici vidéo youtube


### Démo en ligne

Démo en ligne

### Liens

lien vers Binder
lien vers capytale
liens vers fichier arduino







## III. Exemple d'utilisation

Le notebook [circuit_rc_traitement.ipynb](circuit_rc_traitement.ipynb) propose un exemple d'utilisation d'un fichier de mesures dans le but de déterminer la constante de temps d'un circuit RC.