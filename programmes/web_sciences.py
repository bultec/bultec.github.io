def get_interface(code_init):
	S='''
	<!doctype html>
	<html lang="fr">
	<head>
	  <meta charset="utf-8">
	  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
	  <style>.menu {
	    display: flex;
	    padding: 10px;
	}
	.vert {
	    background-color: darkseagreen;
	}
	
	.bleu {
	    background-color:cadetblue;
	}
	
	.rouge {
	    background-color:lightcoral;
	}
	.element {
	    margin-left:20px;
	}
	
	#myChart {
	    width:0px;
	    height:auto;
	}
	
	button {
	    cursor: pointer;
	    text-decoration: none;
	    padding: 6px;
	    font-family: arial;
	    font-size: 1em;
	    background-color: rgb(79, 150, 185);
	    color: #FFFFFF;
	    border-radius: 6px;
	    border: 2px solid #FFFFFF;
	    box-shadow: 2px 2px 6px #444444;
	    }
	    
	button:active {
	    box-shadow: 1px 1px 4px #777777;
	}
	
	button:disabled {
	    
	    background-color: darkgray;
	}
	</style>
	
	</head>
	
	<body>
	  <div class="menu" id="id_menu">
	    <div id="id_boutons_commandes">
	      <button class="rouge" id="id_button_connexion">Connexion</button>
	    </div>
	  </div>
	  <div><canvas id="myChart"></canvas></div>
	  <p id="id_resultat"></p>
	  <script>
	/*
	Name:       webardu.js
	Version     V 1.0.0
	Purpose:    utilitaires de mesures Arduino utilisant la bibliotheque web serial
	            Copyright (C) 2024 Philippe Campion
	License    GNU GENERAL PUBLIC LICENSE Version 3
	------------------------------------------------
	*/
	
	// grandeurs modifiables par l'utilisateur
	var series = [{grandeur: "", unite: ""}, {grandeur: "", unite: ""}];
	var titre_graphe = "";
	var axes = [{grandeur: "", unite: ""}, {grandeur: "", unite: ""}];
	var commandes =[];
	var abscisse_is_saisie  =  true;
	var tableau_masjuscule = false;
	var tableur = false;
	/*
	var commandes = [{texte_bouton:"", arduino:""},
	                 {texte_bouton:"", arduino:""}];
	*/
	// modes : "temporel", "point" ou "commande" 
	var mode = "";
	var precision = 3;
	var car_par_ligne = 70;
	
	//------------------------------------------------------------------------
	
	// --- modifications utilisateur --- 
	// --- inserer ici ---
	
	// --- variables globales -> ne pas modifier ---
	var port = null;
	var my_chart = null;
	var  a_desactiver = ["id_zone_saisie", "id_bouton_commande_1",
	                     "id_bouton_commande_2", "id_bouton_supprime", "id_bouton_copie"];
	var affichage_resultat = true;
	var tab_boutons_commande = [];
	
	// --- initialisations ---
	document.getElementById("myChart").style.display = "none";
	
	//--- fonctions de communication ---
	async function do_connect() {
	// Selection du port serie
	  try {
	    if (port == null)  {
	      port = await navigator.serial.requestPort();
	      await port.open({ baudRate: 9600 });
	      bouton_connexion.className = "vert";
	      setTimeout (() => disable_status(a_desactiver, false), 1500);
	      if ((mode == "point") || (mode == "temporel")) {
	        document.getElementById("myChart").style.width = "100%";
	        document.getElementById("myChart").style.display = "block";
	      }
	      valeurs = [];
	    }
	    else {
	      bouton_connexion.className = "bleu";
	      await port.close();
	      port = null;
	      bouton_connexion.className = "rouge";
	      disable_status(a_desactiver, true);
	      if ((mode == "point") || (mode == "temporel")) {
	        document.getElementById("myChart").style.width = "inherit";
	        document.getElementById("myChart").style.display = "none";
	      }
	    }
	  }
	  catch (error) {
	    await port.close();
	    port = null;
	    bouton_connexion.className = "rouge";
	    disable_status(a_desactiver, true);
	  }
	  if ((my_chart == null) && (mode != "commande")) {
	    // correction pour capytale
	    my_chart = cree_chart();
	  }
	}
	
	async function set_command(command) {
	  // envoi command sur le liaison serie et attend le resultat
	  const encoder = new TextEncoder();
	  const writer = await port.writable.getWriter();
	  await writer.write(encoder.encode(command));
	  await writer.releaseLock();
	  return await get_one_result();
	}
	
	async function get_one_result() {
	  // attend un resultat sur la liaison serie
	  chaine = "";
	  try {
	    if (port != null) {
	      const textDecoder = new TextDecoder();
	      const reader = port.readable.getReader(); 
	      ok = true;
	      while (ok) {
	        const {value, done } = await reader.read();
	        ch = textDecoder.decode(value);
	        if (ch.includes("\\n")) {
	          await reader.releaseLock();
	          ok =false;
	        }
	        chaine = chaine + ch;
	      }
	    }
	    return chaine;
	  }
	  catch (error) {
	    return null;
	  }
	}
	
	function update_affichage(index, chaine) {
	  // met a jour regulierement l'affichage 
	  // appele par readUntilClosed() {
	  let tableau = chaine.split("\\n");
	  let l_index = index;
	  for (i=index; i<tableau.length-1; i++) {
	    //on ne prend pas la dernière valeur
	    //ajoute les valeurs au graphe
	    l_index = i+1;
	    mes = tableau[i].split(',');
	    for (let i=0; i<series.length; i++) {
	      try {
	        my_chart.data.datasets[i].data.push({x: parseFloat(mes[0]),
	                                             y: parseFloat(mes[i+1]).toPrecision(precision)});
	      }
	      catch (error) {}
	    }
	    my_chart.update();
	  }
	  return l_index;
	}
	
	function vide_graphe() {
	  for (let i=0; i<series.length; i++) {
	    my_chart.data.datasets[i].data = [];
	    /*
	    my_chart.data.datasets[0].data = [];
	    my_chart.data.datasets[1].data = [];
	    */
	  }
	  my_chart.update();
	}
	
	async function readUntilClosed() {
	  // lit les valeurs sur la liaison serie jusqu'a la
	  // detection du mot "end";
	  var keepReading = true;
	  var index = 0;
	  const textDecoder = new TextDecoder();
	  chaine = "";
	  vide_graphe();
	  while (port.readable && keepReading) {
	    reader = port.readable.getReader();
	    try {
	      while (true) {
	        const { value, done } = await reader.read();
	        if (done) {
	          chaine = chaine + textDecoder.decode(value);
	          break;
	        }
	        chaine = chaine + textDecoder.decode(value);
	        if (chaine.includes("end\\r\\n")) {
	          keepReading = false;
	          //console.log("fin détectée");
	          await reader.releaseLock();
	        }
	        else {
	          index = update_affichage(index, chaine);
	        }  
	      }
	    }
	    catch (error) {}
	    finally {
	      await reader.releaseLock();
	    }
	  }
	  return chaine;
	}
	
	// --- graphique ---
	function cree_chart() {
	  
	  const couleurs = [{back:'rgba(255, 99, 132, 0.2)', border:'rgba(255, 99, 132, 1)'},
	                    {back:'rgba(75, 192, 192, 0.2)', border:'rgba(75, 192, 192, 1)'},
	                    {back:'rgba(0, 192, 0, 0.2)', border:'rgba(0, 192, 0, 1)'},
	                    {back:'rgba(0, 0, 255, 1)', border:'rgba(0, 0, 139, 1)'},
	                    {back:'rgba(255, 0, 0, 1)', border:'rgba(139, 0, 0, 1)'}
	                   ];
	  /*
	  const couleurs = [{back:'rgba(255, 165, 0, 0.5)', border:'rgba(255, 165, 0, 1)'},
	                    {back:'rgba(75, 192, 192, 0.2)', border:'rgba(75, 192, 192, 1)'}];
	                    */
	  const ctx = document.getElementById('myChart');
	  const l_datasets = [];
	  const l_color = 'blue';
	  for (let i=0; i<series.length; i++) {
	    let l_data = {label : series[i]["grandeur"]+" ("+series[i]["unite"]+")", data: [],
	                  //backgroundColor: couleurs[i]["back"], borderColor: couleurs[i]["border"], 
	                  borderWidth: 1};
	    l_datasets.push(l_data);
	  }
	  the_chart = new Chart(ctx, {
	      type: 'scatter',
	      data: { datasets: l_datasets},
	      options: {
	        responsive: true,
	        animation: false,
	        plugins: {
	          legend: {
	            position: 'right',
	          },
	          title: {
	            display: true,
	            text: titre_graphe,
	            font: {size: 16}
	          }
	        },
	        scales: {
	          x: {
	            type: 'linear', 
	            title: {display : true,
	                    text : axes[0]["grandeur"]+" ("+axes[0]["unite"]+")",
	                    color: l_color,
	                  },
	            ticks: {
	              color: l_color,
	            }
	          },
	          y: {
	            type: 'linear', 
	            title: {display : true,
	                    text : axes[1]["grandeur"]+" ("+axes[1]["unite"]+")",
	                    color: l_color,
	                  },
	            position: 'left',
	            ticks: {
	              color: l_color,
	            }
	          },
	        }
	      }
	    });
	  return the_chart;
	}
	
	// --- code personalisable ---
	async function do_commande(command) {
	  // traite le résultat renvoye par la fonction get_one_result
	  let resultat = document.getElementById("id_resultat");
	  // si command est vide, on utilise le mot de la zone de saisie
	  if (command == "") {
	    command = zone_saisie.value;
	  }
	  try {
	    resultat.innerHTML = await set_command(command);
	  }
	  catch (error){
	    console.log("Erreur");
	  }
	}
	
	async function do_mesure_ponctuelle(command) {
	  // traite le résultat renvoye par la fonction get_one_result
	  let resultat = document.getElementById("id_resultat");
	  try {
	    chaine = await set_command(command);
	    if (series.length > 1) {
	      mes = chaine.split(',');
	    }
	    else {
	      mes = [chaine];
	    }
	    if (!(abscisse_is_saisie)) {
	      // l'abscisse est la première valeur envoyée par arduino
	      X = mes[0];
	    }
	    else {
	      // l'abscisse est la valeur saisie
	      X = zone_saisie.value; 
	    }
	    for (let i=0; i<series.length; i++) {
	      try {
	        my_chart.data.datasets[i].data.push({x: parseFloat(X).toPrecision(precision),
	                                             y: parseFloat(mes[i]).toPrecision(precision)});
	      }
	      catch (error) {}
	    }
	    my_chart.update();
	    resultat.innerHTML = tableaux_pyhon(true);
	    // resultat.innerHTML = `A = [${valeurs}]`;
	  }
	  catch (error){
	    console.log("Erreur");
	  }
	}
	
	async function do_mesures_tempo(commande) {
	  // traite le resultat envoye par readUntilClosed()
	  try {
	    disable_status(a_desactiver, true);
	    set_command(commande);
	    let resultat = document.getElementById("id_resultat");
	    resultat.innerHTML = '';
	    let v = await readUntilClosed();
	    resultat = document.getElementById("id_resultat");
	    resultat.innerHTML = tableaux_pyhon(true);
	  }
	  finally {
	    disable_status(a_desactiver, false);
	  }
	}
	
	//--- fonctions utilitaire ---
	function disable_status(tab_id, b)  {
	  for (e of a_desactiver) {
	    e.disabled = b;
	  }
	}
	
	function formatte(chaine) {
	  try {
	    let tension = parseInt(chaine) * 5 / 1023;
	    tension = tension.toPrecision(3);
	    return tension
	  }
	  catch (error) {
	    return "Erreur de conversion";
	  }
	}
	
	function supprime_dernier_point() {
	  for (let i=0; i<series.length; i++) {
	    try {
	      my_chart.data.datasets[i].data.pop();
	      my_chart.update();
	      document.getElementById("id_resultat").innerHTML = tableaux_pyhon(true);
	    }
	    catch (error) {}
	  }
	}
	
	function tableaux_pyhon(for_web) {
	  const nb_car = car_par_ligne;
	  affichage = "";
	  if ((mode == "temporel") || (mode == "point")){
	    // on commence par le tableau des temps (ou de la zone de saisie si mode = "point")
	    if (mode == "temporel") {
	      if (tableau_masjuscule)
	        nom_tab = "T";
	      else
	        nom_tab = "t";
	    }
	    else {
	      if (tableau_masjuscule)
	        nom_tab = axes[0]["grandeur"].toUpperCase();
	      else
	        nom_tab = axes[0]["grandeur"];
	    }
	    let lignes = 1;
	    if (for_web) {
	      une_grandeur = `<ul><li>${nom_tab} = [`;
	    }
	    else {
	      une_grandeur = `${nom_tab} = [`;
	    }
	    for (let i=0; i<my_chart.data.datasets[0].data.length; i++) {
	      une_grandeur += +my_chart.data.datasets[0].data[i]["x"] + ", ";
	      if ((!for_web) && (une_grandeur.length > lignes * nb_car)) {
	        une_grandeur += "\\n";
	        lignes += 1;
	      }
	    }
	    // si saut de ligne a la fin de la chaine, il faut le supprimer
	    if (une_grandeur[une_grandeur.length - 1] == "\\n") 
	      une_grandeur = une_grandeur.substring(0, une_grandeur.length - 1);
	    //supprime la virgule et l'espace de fin
	    affichage = une_grandeur.substring(0, une_grandeur.length - 2) + "]";
	  }
	  // ensuite, on traite toutes les autres grandeurs
	  for (let i=0; i<series.length; i++) {
	    let lignes = 1;
	    if (tableau_masjuscule) 
	      une_grandeur = series[i]["grandeur"].toUpperCase() + " = [";
	    else
	      une_grandeur = series[i]["grandeur"] + " = [";
	    for (let j=0; j<my_chart.data.datasets[i].data.length; j++) {
	      une_grandeur += my_chart.data.datasets[i].data[j]["y"] + ", ";
	      if ((!for_web) && (une_grandeur.length > lignes*nb_car)) {
	        une_grandeur += "\\n";
	        lignes +=1;
	      }
	    }
	    // si saut de ligne a la fin de la chaine, il faut le supprimer
	    if (une_grandeur[une_grandeur.length - 1] == "\\n") 
	      une_grandeur = une_grandeur.substring(0, une_grandeur.length - 1);
	    if (for_web) {
	      affichage = affichage + "</li><li>" + une_grandeur.substring(0, une_grandeur.length - 2) + "]";
	    }
	    else {
	      //supprime la virgule et l'espace de fin
	      affichage = affichage + "\\n" + une_grandeur.substring(0, une_grandeur.length - 2) + "]";
	    }
	  }
	  if (for_web) {
	    affichage += "</li></ul>";
	  }
	  return affichage;
	}
	
	function tableaux_tableur() {
	  affichage = "Mesures Arduino" + "\\n";
	  if (mode == "temporel")
	      affichage += "t" + "	";
	  if (mode == "point")
	      affichage += axes[0]["grandeur"] + "	";
	  for (let i=0; i<series.length; i++)
	    affichage += series[i]["grandeur"] + "	";
	  affichage += "\\n";
	  if ((mode == "temporel") || (mode == "point"))
	    affichage += axes[0]["unite"] + "	";
	  for (let i=0; i<series.length; i++)
	    affichage += series[i]["unite"] + "	";
	  affichage += "\\n";
	  for (i=0; i<my_chart.data.datasets[0].data.length; i++) {
	    affichage += my_chart.data.datasets[0].data[i]["x"] + "	";
	    for (let j=0; j<my_chart.data.datasets.length; j++) {
	      affichage += my_chart.data.datasets[j].data[i]["y"]  + "	";
	    }
	    affichage += "\\n";
	  }  
	  return affichage;
	}
	
	function copie_presse_papier () {
	  // Copie dans le presse papier
	  if (tableur)
	    texte = tableaux_tableur();
	  else
	    texte = tableaux_pyhon(false);
	  navigator.clipboard.writeText(texte);
	}
	
	function cree_boutons_commandes(){
	  // creation des boutons si commandes[i]["arduino"]!=""
	  l_div = document.getElementById("id_boutons_commandes");
	  for (let i=0; i<commandes.length; i++) {
	    let l_btn = document.createElement("BUTTON");
	    if (commandes[i]["arduino"]!="") {
	      let l_txt = document.createTextNode(commandes[i]["texte_bouton"]);
	      l_btn.appendChild(l_txt);
	      l_btn.className = "element bouton";
	      l_div.appendChild(l_btn);
	      tab_boutons_commande.push(l_btn);
	    }
	  }
	}
	
	function cree_bouton_copie() { 
	  let l_btn = document.createElement("BUTTON");
	  let l_txt = document.createTextNode("Copie presse papier");
	  l_btn.appendChild(l_txt);
	  l_btn.className = "element";
	  document.getElementById("id_boutons_commandes").appendChild(l_btn);
	  return l_btn;
	}
	
	function cree_bouton_supprime() { 
	  let l_btn = document.createElement("BUTTON");
	  let l_txt = document.createTextNode("Supp. dernier");
	  l_btn.appendChild(l_txt);
	  l_btn.className = "element";
	  document.getElementById("id_boutons_commandes").appendChild(l_btn);
	  return l_btn;
	}
	
	function cree_zone_saisie(texte_saisie) {
	  // creation de la zone saisie
	  var label_saisie = document.createElement("label");
	  label_saisie.innerText = texte_saisie;
	  label_saisie.className = "element";
	  document.getElementById("id_boutons_commandes").appendChild(label_saisie);
	  zone_saisie = document.createElement("input");
	  zone_saisie.type = "text";
	  zone_saisie.className = "element";
	  document.getElementById("id_boutons_commandes").appendChild(zone_saisie);
	  return zone_saisie;
	}
	
	// ------ programme principal ------
	
	
	if ("serial" in navigator) {
	  // The Web Serial API is supported.
	  bouton_connexion = document.getElementById("id_button_connexion");
	  document.getElementById("myChart").style.display = "none";
	  // affichage des elements en fonction du mode 
	  switch (mode) {
	    case "temporel":
	      affichage_resultat = false;
	      cree_boutons_commandes();
	      var action_traitement = do_mesures_tempo;
	      bouton_copie = cree_bouton_copie();
	      bouton_copie.addEventListener('click', copie_presse_papier);
	      a_desactiver = tab_boutons_commande;
	      a_desactiver.push(bouton_copie);
	      break;
	    case "point":
	      if (abscisse_is_saisie)
	        zone_saisie = cree_zone_saisie(axes[0]["grandeur"] + " (" + axes[0]["unite"] + ")");
	      cree_boutons_commandes();
	      var action_traitement = do_mesure_ponctuelle;
	      // creer les boutons supprime et copie
	      bouton_supprime =cree_bouton_supprime();
	      bouton_supprime.addEventListener('click', supprime_dernier_point);
	      bouton_copie = cree_bouton_copie();
	      bouton_copie.addEventListener('click', copie_presse_papier);
	      break;
	    case "commande":
	      cree_boutons_commandes();
	      var action_traitement = do_commande;
	      if ((commandes.length == 0) || ((commandes[0]["arduino"] == ""))) {
	        l_btn = document.createElement("BUTTON");
	        if (commandes.length == 0) {
	          zone_saisie = cree_zone_saisie("Commande");
	          l_txt = document.createTextNode("Envoyer");
	          l_btn.appendChild(l_txt);
	          l_btn.addEventListener('click', async => action_traitement(""));
	        }
	        else {
	          let l_tab = commandes[0]["texte_bouton"].split(",");
	          if (l_tab.length > 1) {
	            zone_saisie = cree_zone_saisie(l_tab[0]);
	            l_txt = document.createTextNode(l_tab[1]);
	          }
	          else {
	            zone_saisie = cree_zone_saisie("Commande");
	            l_txt = document.createTextNode(l_tab[0]);
	          }
	          l_btn.appendChild(l_txt);
	        }
	        l_btn.className = "element";
	        document.getElementById("id_boutons_commandes").appendChild(l_btn);
	        tab_boutons_commande.push(l_btn);
	        zone_saisie.addEventListener("keypress", function(event) {
	          if (event.key === "Enter") {
	              event.preventDefault();
	            l_btn.click();
	            }
	          }
	        );
	      }
	      else {
	        a_desactiver = tab_boutons_commande;
	      }
	      document.getElementById("myChart").style.display = "none";
	      break;
	  }
	
	  // affichage ou non du resultat
	  if (!affichage_resultat) {
	    document.getElementById("id_resultat").style.display = "none";
	  }
	  
	  // connexions des boutons aux commandes
	  bouton_connexion.addEventListener('click', async => do_connect());
	  for (let i=0; i<commandes.length; i++) {
	    tab_boutons_commande[i].addEventListener('click', async => action_traitement(commandes[i]["arduino"]));
	  }
	
	  disable_status(a_desactiver, true);
	  if (mode != "commande") {
	    try {
	      my_chart = cree_chart();
	    }
	      catch (error) {console.log("Erreur chart")}
	  }
	}
	else {
	  alert("Web Serial n'est pas supporté par le navigateur");
	}
	</script>
	
	</body>
	</html>

	'''
	S = S.replace('// --- inserer ici ---', code_init)
	return S
