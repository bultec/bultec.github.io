import re

# --- code personalisable ---
# nom du fichier html de sortie
nom_fichier_html = "temperature_tab.html"

# code javascrit à insérer

my_init = '''

votre code javascript ici

'''

# -----------------------------------------------
# --- écriture du fichier final - ne pas modifier
fichier = open("web_sciences_complet.html", "r", encoding='utf8')
_html = fichier.read()
fichier.close()

sortie = _html.replace('// --- inserer ici ---', my_init)

fichier = open(nom_fichier_html, "w", encoding='utf8')
fichier.write(sortie)
fichier.close()

