# Table d'Echange - Reference Technique

La table d'echange est la structure de donnees centrale du systeme Essensys. C'est un tableau d'octets en memoire (`unsigned char Tb_Echange[]`) partage entre le firmware, l'ecran tactile et le serveur. Chaque indice represente un etat, une configuration ou une commande.

Ce document est extrait directement du code source C du firmware : `H/TableEchange.h`, `H/TableEchangeDroits.h`, `C/TableEchangeAcces.c` et `C/TableEchangeFlash.c`.

## 1. Structure Memoire

```c
// Tableau principal en RAM
unsigned char Tb_Echange[Nb_Tbb_Donnees];

// Copie precedente (pour detecter les changements)
unsigned char Tb_EchangePrecedent[Nb_Tbb_Donnees];

// Droits d'acces par indice
const unsigned char Tb_Echange_Droits[Nb_Tbb_Donnees];
```

- Chaque indice contient **1 octet** (0-255)
- La taille totale est definie par l'enum `Nb_Tbb_Donnees` (~600 indices)
- Les valeurs superieures a 255 utilisent des paires LSB/MSB

## 2. Droits d'Acces

Chaque indice possede un masque de droits defini dans `H/TableEchangeDroits.h` :

| Code | Masque | Signification |
|------|--------|---------------|
| `__` | `0x00` | Aucun acces (ecran/serveur). Seul le BP lit/ecrit directement |
| `R_` | `0x01` | Lecture seule (ecran/serveur) |
| `_W` | `0x02` | Ecriture seule (ex: cle d'acces distance) |
| `RW` | `0x03` | Lecture et ecriture |
| `RWS` | `0x83` | Lecture, ecriture, et **sauvegardee en Flash** au redemarrage |

### Regles d'Acces

Source : `C/TableEchangeAcces.c`

```
BP (firmware)     : acces direct en lecture/ecriture (pas de controle)
Ecran et Ethernet : acces via uc_TableEchange_Ecrit_Data() et uc_TableEchange_Lit_Data()
                    avec verification des droits et traitements speciaux
```

### Traitements Speciaux a l'Ecriture

Certains indices declenchent une logique supplementaire quand ils sont ecrits :

| Indices | Comportement |
|---------|-------------|
| Minutes, Heure, Jour, Mois, Annee | Mise a jour de la structure date/heure RTC |
| VacanceFin_A | Declenchement de la verification date retour vacances |
| Chauf_zj_Auto ... Chauf_zsb2_Mode | Recalcul immediat de la consigne chauffage |
| Chauf_zj_Mode (depuis serveur) | Flag `uc_ChauffageModifieDepuisServeur_zj` |
| Cumulus_Mode (depuis serveur) | Flag `uc_CumulusModifieDepuisServeur` |

## 3. Cartographie Complete des Indices

Extraite de l'enum `Tbb_Donnees_Index` dans `H/TableEchange.h`.

### 3.1 Versions (indices 0-4)

| Indice | Mnemonique | Droits | Description |
|--------|-----------|--------|-------------|
| 0 | `Version_SoftBP_Embedded` | R_ | Version firmware du BP (numero sauvegarde) |
| 1 | `Version_SoftBP_Web` | R_ | Version web (pour gestion telechargement) |
| 2 | `Version_SoftIHM_Majeur` | RWS | Version ecran tactile (majeur) |
| 3 | `Version_SoftIHM_Mineur` | RWS | Version ecran tactile (mineur) |
| 4 | `Version_TableEchange` | R_ | Version de la table d'echange (compatibilite) |

### 3.2 Date et Heure (indices 5-9)

| Indice | Mnemonique | Droits | Description |
|--------|-----------|--------|-------------|
| 5 | `Minutes` | RW | Minutes (base de l'horloge RTC) |
| 6 | `Heure` | RW | Heure |
| 7 | `Jour` | RW | Jour du mois |
| 8 | `Mois` | RW | Mois |
| 9 | `Annee` | RW | Annee (2 chiffres) |

### 3.3 Etat du Systeme (indices 10-12)

| Indice | Mnemonique | Droits | Description | Bits |
|--------|-----------|--------|-------------|------|
| 10 | `Status` | RW | Etat global | b0: heures creuses, b1: delestage, b2: secouru |
| 11 | `Alerte` | RW | Alertes actives | b0: alarme, b1: fuite lave-linge, b2: fuite lave-vaisselle |
| 12 | `Information` | RW | Defauts communication | b0: compteur ERDF, b1: IHM, b2: BA PDV, b3: BA CHB, b4: BA PDE |

### 3.4 Chauffage - Planning Automatique (indices 13-348)

Programmation horaire sur 1 semaine : 1 ordre par heure sur 7 jours, 6 modes possibles (4 bits). Soit **84 octets par zone**.

| Plage | Mnemonique | Zone |
|-------|-----------|------|
| 13-96 | `Chauf_zj_Auto` | Zone jour (salon, sejour) |
| 97-180 | `Chauf_zn_Auto` | Zone nuit (chambres) |
| 181-264 | `Chauf_zsb1_Auto` | Salle de bain 1 |
| 265-348 | `Chauf_zsb2_Auto` | Salle de bain 2 |

Consignes possibles (bits 0-3) :

| Valeur | Mode |
|--------|------|
| 0 | OFF |
| 1 | CONFORT |
| 2 | ECO |
| 3 | ECO+ |
| 4 | ECO++ |
| 5 | HORS GEL |

### 3.5 Chauffage - Mode Immediat (indices 349-352)

Forcement immediat des consignes chauffage. **Proteges par mutex** (acces concurrent Main/Ecran/Ethernet).

| Indice | Mnemonique | Description | Encodage |
|--------|-----------|-------------|----------|
| 349 | `Chauf_zj_Mode` | Zone jour | Voir ci-dessous |
| 350 | `Chauf_zn_Mode` | Zone nuit | |
| 351 | `Chauf_zsb1_Mode` | Salle de bain 1 | |
| 352 | `Chauf_zsb2_Mode` | Salle de bain 2 | |

Encodage de l'octet mode :

```
b0-b3 : consigne (0=OFF, 1=CONFORT, 2=ECO, 3=ECO+, 4=ECO++, 5=HORS GEL)
b4-b5 : mode (0=automatique, 1=force, 2=anticipe)
b6    : 1 = reprendre le dernier fonctionnement memorise
b7    : 1 = continuer le fonctionnement actuel

Exemples :
  0x00-0x05 : forcage en automatique
  0x10-0x15 : forcage en mode force + consigne
  0x20-0x25 : forcage en mode anticipe
  0x40      : reprendre le dernier mode memorise
  0x80      : continuer le mode actuel
```

### 3.6 Cumulus (indice 353)

| Indice | Mnemonique | Droits | Valeurs |
|--------|-----------|--------|---------|
| 353 | `Cumulus_Mode` | RWS | 0=Autonome (ON), 1=Gestion HC, 2=OFF |

### 3.7 Vacances (indices 354-363)

| Indice | Mnemonique | Description |
|--------|-----------|-------------|
| 354 | `VacanceFin_H` | Heure retour vacances |
| 355 | `VacanceFin_Mn` | Minute |
| 356 | `VacanceFin_J` | Jour |
| 357 | `VacanceFin_M` | Mois |
| 358 | `VacanceFin_A` | Annee (declenche verification date) |
| 359 | `VacanceFin_zj_Force` | Consigne chauffage zone jour au retour |
| 360 | `VacanceFin_zn_Force` | Consigne chauffage zone nuit au retour |
| 361 | `VacanceFin_zsb1_Force` | Consigne SDB 1 au retour |
| 362 | `VacanceFin_zsb2_Force` | Consigne SDB 2 au retour |

### 3.8 Arrosage (indices 363-406)

| Plage | Mnemonique | Description |
|-------|-----------|-------------|
| 363 | `Arrose_Mode` | 0=OFF, 1-254=duree forcage (min), 255=auto |
| 364-405 | `Arrose_Auto` | Planning hebdo (42 octets, 1 bit / 30 min) |
| 406 | `Arrose_Detect` | 0=detecteur pluie OFF, 1=actif |

### 3.9 Alarme (indices 407-435)

| Indice | Mnemonique | Description |
|--------|-----------|-------------|
| 407 | `Alarme_AccesADistance` | 1=autorise modification a distance |
| 408 | `Alarme_Mode` | 0=OFF, 1=reglage, 2=independante, 3-6=sur scenario |
| 409 | `Alarme_Commande` | 1=demande mise sous alarme |
| 410 | `Alarme_CodeSaisiLSB` | Code saisi (chiffres 1-2, 4 bits chacun) |
| 411 | `Alarme_CodeSaisiMSB` | Code saisi (chiffres 3-4) |
| 412 | `Alarme_Autorisation` | 0=attente, 1=code valide, 2=code invalide |
| 413 | `Alarme_SuiviAlarme` | Etape automate (0=depart, 3=sortie, 4=croisiere, 5=entree, 6=intrusion) |
| 414 | `Alarme_Detection` | Bitmask : b0=ouverture, b1=presence1, b2=presence2 |
| 415 | `Alarme_Fraude` | Bitmask : b0=tableau, b1=IHM, b2-5=detecteurs/sirenes, b6=batterie |
| 416 | `Alarme_SuiviChangementCode` | Etape changement code |
| 417-418 | `Alarme_CodeUser1 LSB/MSB` | Code alarme 1 (acces __ = indirect uniquement) |
| 419-420 | `Alarme_CodeUser2 LSB/MSB` | Code alarme 2 (non utilise) |
| 421 | `Alarme_CompteARebours` | Temps restant (sec) en procedure sortie/entree |
| 423 | `Alarme_TestRAZPresence` | RAZ detecteurs en mode reglage |
| 424 | `Alarme_TestSirenes` | 1=sirene int, 2=sirene ext |
| 425-435 | `AlarmeConfig` | 11 parametres config (code requis, detecteurs actifs, sirenes, blocage volets) |

### 3.10 Alerte et Securite (indices 436-443)

| Indice | Mnemonique | Description |
|--------|-----------|-------------|
| 436 | `Alerte_Intensite` | Intensite sirene (25=fort, 50=moyen, 75=faible) |
| 437 | `Alerte_Duree` | 0=jusqu'a disparition, 1-255=secondes |
| 438 | `Alerte_TestSirene` | Activer sirene test |
| 439 | `Alerte_Acquit` | Acquittement alerte |
| 440 | `Securite_PriseCoupe` | 1=prises securite coupees |
| 441 | `Securite_FuiteLinge` | 1=detection fuite lave-linge active |
| 442 | `Securite_FuiteVaisselle` | 1=detection fuite lave-vaisselle active |
| 443 | `Securite_FuiteAlerte` | 1=alerte sonore en cas de fuite |

### 3.11 Reveil (indices 444-458)

Fonction reveil : provoque l'ouverture des volets roulants a l'heure programmee.

| Plage | Zone | Indices : H / Mn / ON |
|-------|------|----------------------|
| 444-446 | Grande chambre | H=444, Mn=445, ON=446 |
| 447-449 | Chambre 1 | H=447, Mn=448, ON=449 |
| 450-452 | Chambre 2 | H=450, Mn=451, ON=452 |
| 453-455 | Chambre 3 | H=453, Mn=454, ON=455 |
| 456-458 | Bureau | H=456, Mn=457, ON=458 |

### 3.12 Delestage (indice 459)

| Indice | Mnemonique | Description |
|--------|-----------|-------------|
| 459 | `Delestage` | 0=OFF, <>0=actif |

### 3.13 Teleinfo Compteur ERDF (indices 460-484)

| Indice | Mnemonique | Description |
|--------|-----------|-------------|
| 460 | `TeleInf_OPTARIF` | Option tarifaire (BASE, HC, EJP, BBR) |
| 461 | `TeleInf_PTEC` | Periode tarifaire en cours (HC, HP, etc.) |
| 462 | `TeleInf_ADPS` | Avertissement depassement puissance souscrite |
| 463-464 | `TeleInf_PAPP LSB/MSB` | Puissance apparente (VA) |
| 465-476 | `TeleInf_HPB_*` | Consommation heures pleines/base (6 paires LSB/MSB) |
| 477-488 | `TeleInf_HC_*` | Consommation heures creuses (6 paires LSB/MSB) |
| 489-493 | `TeleInf_Repartition_*` | Repartition en % (chauffage, refroid, eau chaude, prises, autres) |

### 3.14 Eclairage et Volets (indices ~494-532)

| Plage | Mnemonique | Description |
|-------|-----------|-------------|
| ~494-501 | `Variateurs_PDV_Conf` | Config variateurs PDV (8 max par BA) : 0=TOR rampe, 1=gradateur, 2=TOR sans rampe |
| ~502-509 | `Variateurs_CHB_Conf` | Config variateurs CHB |
| ~510-517 | `Variateurs_PDE_Conf` | Config variateurs PDE |
| ~518-533 | `Lampes_PDV_Temps` | Temps extinction lampes PDV (1-255 min, 0=pas d'auto) |
| ~534-549 | `Lampes_CHB_Temps` | Temps extinction lampes CHB |
| ~550-565 | `Lampes_PDE_Temps` | Temps extinction lampes PDE |
| ~566-573 | `Volets_PDV_Temps` | Temps action volets PDV (1-255 sec) |
| ~574-581 | `Volets_CHB_Temps` | Temps action volets CHB |
| ~582-589 | `Volets_PDE_Temps` | Temps action volets PDE |

### 3.15 Scenarios (indices 590+)

| Indice | Mnemonique | Description |
|--------|-----------|-------------|
| 590 | `Scenario` | Numero du scenario a lancer (0=aucun, 1-8) |
| 591 | `Scenario_DernierLance` | Dernier scenario lance |
| 592-632 | `Scenario1` | Parametres scenario 1 (41 valeurs, voir section 4) |
| 633-673 | `Scenario2` | "Je sors" |
| 674-714 | `Scenario3` | "Je pars en vacances" |
| 715-755 | `Scenario4` | "Je rentre" |
| 756-796 | `Scenario5` | "Je vais me coucher" |
| 797-837 | `Scenario6` | "Je me leve" |
| 838-878 | `Scenario7` | "Personnalise 1" |
| 879-919 | `Scenario8` | "Personnalise 2" |

Puis en fin de table :

| Indice | Mnemonique | Description |
|--------|-----------|-------------|
| ~920-921 | `EtatBP1/2` | Etat du BP (b0: alarme activee, b1: alarme declenchee) |
| ~922-937 | `Cle_Acces_Distance` | Cle 32 chiffres (16 octets, 2 chiffres / octet, acces `_W`) |
| ~938 | `Store_VR` | 0=store normal, 1=store comme 15e VR |
| ~939 | `Store_Vitesse_Vent_Repliage` | Seuil repliage auto (km/h) |
| ~940 | `Store_Vitesse_Vent_Instantane` | Vitesse vent actuelle (km/h) |
| ~941-942 | `Constructeur_Code LSB/MSB` | Code constructeur (lecture seule, en dur: 0x1119) |
| ~943-944 | `Test_ETOR_1/2` | Etat entrees logiques (detecteurs, fraudes) |
| ~945 | `EtatEthernet` | b0=cable, b1=DHCP, b2=DNS, b3=serveur |
| ~946 | `Mode_Test` | 0=normal, 1=test (desactive sauvegarde Flash) |
| ~947-952 | `AdresseMAC_1..6` | Adresse MAC du BP (lecture seule) |

## 4. Zoom : Parametres de Scenario (enumScenario)

Chaque scenario contient 41 parametres definis dans `enumScenario`. La base est 600 pour le Scenario1 (indice 592 dans la table + offset enum).

**Indices absolus = indice du scenario dans la table + position dans l'enum.**

Pour les ordres envoyes par le serveur via `/api/myactions`, les indices sont ceux du scenario 1, soit la plage **600-640**.

### 4.1 Controle Alarme et Configuration (offset 0-12)

| Offset | Indice abs | Mnemonique | Description |
|--------|-----------|-----------|-------------|
| 0 | 600 | `Scenario_Confirme_Scenario` | 1=demander confirmation a l'ecran |
| 1 | 601 | `Scenario_Alarme_ON` | 0=rien, 1=activer alarme, 2=desactiver |
| 2-12 | 602-612 | `Scenario_AlarmeConfig` | 11 parametres config alarme |

### 4.2 Eteindre Lumieres (offset 13-18, indices 613-618)

Chaque indice est un **bitmask** : chaque bit represente une lampe ou un variateur.

| Indice | Mnemonique | Zone | Mapping des bits |
|--------|-----------|------|-----------------|
| **613** | `Eteindre_PDV_LSB` | Pieces de vie (bas) | b0=entree, b1=salon1, b2=salon2, b3=dressing1, b4=dressing2 |
| **614** | `Eteindre_PDV_MSB` | Pieces de vie (haut) | b5=variateur bureau, b6=variateur salle a manger, b7=variateur salon |
| **615** | `Eteindre_CHB_LSB` | Chambres (bas) | b0=escalier, b1=gr.chambre1, b2=gr.chambre2, b3=pet.chambre1-1, b4=pet.chambre1-2, b5=pet.chambre2, b6=pet.chambre3 |
| **616** | `Eteindre_CHB_MSB` | Chambres (haut) | b4=var.pet.chambre3, b5=var.pet.chambre2, b6=var.pet.chambre1, b7=var.gr.chambre |
| **617** | `Eteindre_PDE_LSB` | Pieces d'eau (bas) | b0=cuisine1, b1=cuisine2, b2=SDB1, b3=SDB2-1, b4=SDB2-2, b5=WC1, b6=WC2, b7=service |
| **618** | `Eteindre_PDE_MSB` | Pieces d'eau (haut) | b0=degagement1, b1=degagement2, b2=terrasse, b3=annexe1, b4=annexe2, b7=var.SDB1 |

### 4.3 Allumer Lumieres (offset 19-24, indices 619-624)

Meme structure que les indices "eteindre" mais pour allumer.

| Indice | Mnemonique | Zone |
|--------|-----------|------|
| **619** | `Allumer_PDV_LSB` | Pieces de vie (bas) — meme mapping que 613 |
| **620** | `Allumer_PDV_MSB` | Pieces de vie (haut) — meme mapping que 614 |
| **621** | `Allumer_CHB_LSB` | Chambres (bas) — meme mapping que 615 |
| **622** | `Allumer_CHB_MSB` | Chambres (haut) — meme mapping que 616 |
| **623** | `Allumer_PDE_LSB` | Pieces d'eau (bas) — meme mapping que 617 |
| **624** | `Allumer_PDE_MSB` | Pieces d'eau (haut) — meme mapping que 618 |

### 4.4 Volets (offset 25-30, indices 625-630)

| Indice | Mnemonique | Zone | Mapping des bits |
|--------|-----------|------|-----------------|
| **625** | `OuvrirVolets_PDV` | Ouvrir PDV | b0-2=salon(3), b3-4=SAM(2), b5=bureau |
| **626** | `OuvrirVolets_CHB` | Ouvrir CHB | b0-1=gr.chambre(2), b2=pet.ch1, b3=pet.ch2, b4=pet.ch3 |
| **627** | `OuvrirVolets_PDE` | Ouvrir PDE | b0-1=cuisine(2), b2=SDB1, b3=store terrasse |
| **628** | `FermerVolets_PDV` | Fermer PDV | meme mapping que 625 |
| **629** | `FermerVolets_CHB` | Fermer CHB | meme mapping que 626 |
| **630** | `FermerVolets_PDE` | Fermer PDE | meme mapping que 627 |

### 4.5 Securite, Chauffage, Cumulus, Reveil (offset 31-40)

| Indice | Mnemonique | Description |
|--------|-----------|-------------|
| 631 | `Scenario_Securite` | 0=rien, 1=couper prises, 2=remettre |
| 632 | `Scenario_Machines` | 0=rien, 1=couper machines a laver, 2=remettre |
| 633 | `Scenario_Chauf_zj` | Consigne chauffage zone jour (meme encodage que 3.5) |
| 634 | `Scenario_Chauf_zn` | Consigne chauffage zone nuit |
| 635 | `Scenario_Chauf_zsb1` | Consigne SDB 1 |
| 636 | `Scenario_Chauf_zsb2` | Consigne SDB 2 |
| 637 | `Scenario_Cumulus` | 0=autonome, 1=HC, 2=OFF, 0x40=reprendre, 0x80=continuer |
| 638 | `Scenario_Reveil_Reglage` | 1=lancer procedure reglage reveils |
| 639 | `Scenario_Reveil_ON` | 0=rien, 1=armer reveil, 2=desactiver |
| 640 | `Scenario_Efface` | 1=effacer, 2-6=init predefinies |

## 5. L'Indice 590 : Trigger Scenario

L'indice 590 (`Scenario`) est le **declencheur**. Sans lui, aucun parametre de scenario n'est applique.

```json
{"k": 590, "v": "1"}
```

Le backend Go ajoute automatiquement cet indice lors de la generation du bloc complet via `ActionService.GenerateCompleteBlock()`.

## 6. Regle du Bloc Complet (605-622)

### Pourquoi Envoyer la Table Complete ?

Le firmware lit les indices scenario comme un **bloc atomique**. L'absence d'un indice signifie "garder l'etat actuel". Pour garantir un comportement deterministe, il faut :

1. Toujours inclure **tous les indices 605 a 622** (min. requis par le backend actuel)
2. Initialiser les indices non utilises a **0**
3. Inclure l'indice **590 = 1** comme trigger

### Exemple : Allumer la Lampe de la Petite Chambre 3

La lampe de la petite chambre 3 est sur l'indice 621 (Allumer_CHB_LSB), bit 6 (valeur 64).

```json
{
  "_de67f": null,
  "actions": [{
    "guid": "550e8400-e29b-41d4-a716-446655440000",
    "params": [
      {"k": 590, "v": "1"},
      {"k": 605, "v": "0"}, {"k": 606, "v": "0"}, {"k": 607, "v": "0"},
      {"k": 608, "v": "0"}, {"k": 609, "v": "0"}, {"k": 610, "v": "0"},
      {"k": 611, "v": "0"}, {"k": 612, "v": "0"}, {"k": 613, "v": "0"},
      {"k": 614, "v": "0"}, {"k": 615, "v": "0"}, {"k": 616, "v": "0"},
      {"k": 617, "v": "0"}, {"k": 618, "v": "0"}, {"k": 619, "v": "0"},
      {"k": 620, "v": "0"},
      {"k": 621, "v": "64"},
      {"k": 622, "v": "0"}
    ]
  }]
}
```

### Logique de Merge (Bitwise OR)

Quand plusieurs commandes arrivent simultanement, le backend les combine avec un **OR bitwise** :

```
Commande 1 : allumer entree (619, bit 0 = 1)
Commande 2 : allumer salon  (619, bit 1 = 2)
Resultat    : 619 = 1 | 2 = 3 (les deux s'allument)
```

L'OR ne permet pas d'eteindre. Pour eteindre, utiliser les indices 613-618.

## 7. Persistance Flash

Source : `C/TableEchangeFlash.c`

### Mecanisme de Sauvegarde

La table d'echange est sauvegardee en Flash interne du MCF52259 :

| Parametre | Valeur |
|-----------|--------|
| Adresse Flash | `0x7E000` |
| Taille secteur | 4096 octets (1 secteur) |
| CRC | CRC-16 sur toute la zone (hors 2 premiers octets) |
| Position CRC | 2 premiers octets du secteur |

### Sequence de Sauvegarde

```
1. Verifier Mode_Test != 1 (sinon sauvegarde desactivee)
2. Bloquer les interruptions fil pilote
3. Effacer le secteur Flash (ioctl FLASH_IOCTL_ERASE_SECTOR)
4. Ecrire les Nb_Tbb_Donnees octets de Tb_Echange[]
5. Completer le reste du secteur par des 0
6. Calculer le CRC-16 et l'ecrire aux octets 0-1
7. Reactiver les interruptions
```

### Sequence de Restauration (au Demarrage)

```
1. Initialiser toute la table avec les valeurs par defaut (vd_Init_Echange())
2. Calculer le CRC de la zone Flash
3. Comparer avec le CRC stocke
4. Si CRC OK : pour chaque indice avec droit VALEUR_SAUVEGARDEE (0x80),
   remplacer la valeur par defaut par la valeur lue en Flash
5. Copier Tb_Echange[] dans Tb_EchangePrecedent[] (eviter les faux changements au demarrage)
```

### Indices Sauvegardes

Seuls les indices avec le flag `VALEUR_SAUVEGARDEE` (0x80) dans `Tb_Echange_Droits[]` sont restaures depuis la Flash. Les indices critiques comme les codes alarme sont geres separement via l'EEPROM SPI.

## 8. Correspondance Serveur

### Cles Redis

Le serveur stocke la table d'echange dans Redis :

```
essensys:client:{clientID}:exchange → Redis Hash (indice → valeur)
essensys:global:actions             → Redis List (queue d'ordres)
```

### Points d'Entree pour Modifier la Table

| Source | Endpoint / Mecanisme | Normalisation |
|--------|---------------------|---------------|
| Frontend web | `POST /api/admin/inject` | `ActionService.AddAction()` → bloc complet |
| Frontend web (alarme) | `POST /api/web/actions` | `ActionService.AddAction()` → bloc complet |
| MQTT (Home Assistant) | Topic MQTT → `CommandHandler` | `ActionService.AddAction()` → bloc complet |
| MCP (OpenClaw / IA) | Outil `send_order` | Auto-expansion 605-622 dans le MCP server |
| Control Plane | `PUT /api/redis/exchange/{clientID}/{index}` | Ecriture directe Redis (pas de bloc complet) |

## References Sources

- Definition des indices : `client-essensys-legacy/H/TableEchange.h`
- Droits d'acces : `client-essensys-legacy/H/TableEchangeDroits.h`
- Fonctions d'acces : `client-essensys-legacy/C/TableEchangeAcces.c`
- Persistance Flash : `client-essensys-legacy/C/TableEchangeFlash.c`
- Backend Go (bloc complet) : `essensys-server-backend/internal/core/action_service.go`
- MCP (auto-expansion) : `essensys-server-backend/cmd/mcp-server/main.go`
