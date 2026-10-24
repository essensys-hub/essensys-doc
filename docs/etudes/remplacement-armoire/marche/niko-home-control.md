---
title: "Niko Home Control II : remplacer l'armoire sans recâblage"
description: "Niko Home Control II en câblage bus pour remplacer les quatre cartes de l'armoire ESSENSYS sans toucher aux fils : modules capteurs à trois entrées pour les 63 poussoirs, modules de commutation, moteurs et variateurs sur un bus propriétaire, un contrôleur unique par installation. Seul, chaque bouton passe par le contrôleur ; en dérivation, la couche la plus chère du comparatif. Environ 9 200 € HT en configuration par zone."
---

# Niko Home Control II

Niko Home Control II est le système domotique bus du fabricant belge Niko : un contrôleur connecté, un bus deux fils propriétaire de 26 V, des modules d'armoire sur rail DIN et des commandes murales bus. Ce dossier du [comparatif](index.md) regarde sa version bus avec les 63 poussoirs classiques ramenés en armoire sur des modules à contacts secs, et ce qu'il reste quand le contrôleur se tait.

!!! abstract "Synthèse"
    - **Seule** : Niko reprend les 63 poussoirs sans recâblage, mais à contre-emploi : le seul module d'armoire pour contacts secs à 50 m, le module capteurs 550-00210, n'a que **trois entrées** ; il en faut 21, et son emploi comme entrée poussoir n'est pas décrit. Le système est centralisé et le fabricant impose **un contrôleur par installation** : chaque bouton passe par lui, **règle 1 non tenue**. En configuration par zone (trois installations Niko distinctes), aucune des huit défaillances uniques ne prive toute la maison de ses boutons, **sous réserve de la dépendance à Internet** : la documentation officielle de l'API écrit que le contrôleur « requires internet connectivity for correct operation », sans que Niko dise ce qui s'arrête ; six pannes privent une zone. Les relais d'éclairage sont bistables ; les boutons manuels des modules sont « temporaires, écrasés par la prochaine communication bus ».
    - **En dérivation** : ≈ 8 100 € HT, la couche la plus chère du comparatif, pour des sorties qui ne sont pas des contacts secs, trois entrées par module, un jeton d'API à renouveler chaque année en ligne, et aucun signal cyclique identifié.
    - **Coût estimé** : ≈ 7 600 € HT en configuration minimale, ≈ 9 200 € HT par zone, logiciel gratuit ; ≈ 8 100 € HT en couche domotique seule. Prix hors TVA d'une boutique néerlandaise, octobre 2026 ; aucun prix public Niko ni belge trouvé.
    - **Réserve** : estimations à confirmer par un électricien, des devis, le fabricant et des essais. Aucun forum d'utilisateurs n'a pu être lu.

## Principe et gamme

Niko (Sint-Niklaas, Belgique) est une entreprise familiale fondée en 1919, 700 salariés, dix filiales européennes. Niko Home Control existe en deux déclinaisons : **câblage bus**, avec le contrôleur connecté 550-00003, et câblage traditionnel, avec un concentrateur Zigbee. Ce dossier traite la version bus. La génération I (contrôleur 550-00001, logiciel 1.x) a précédé la génération II (contrôleur 550-00003, logiciel 2.x, version 2.28.1 en octobre 2026) ; les dates de lancement n'ont pas été trouvées. La vente passe par les grossistes.

Le système est **centralisé**. Le contrôleur « stocke la logique de l'installation localement », alimente le bus (26 V continu, 400 mA, TBTS) et intègre un routeur (un port WAN, trois ports LAN). Le manuel matériel est explicite : « chaque installation doit comporter un contrôleur connecté ». Un relais de module « ne change que lorsqu'une impulsion de données est générée par le contrôleur ou par l'un des poussoirs ».

Le bus est un câble deux fils **non polarisé**, en topologie libre vers les commandes murales (étoile, ligne ou mixte, sans boucle). Dans l'armoire, bus et alimentation passent de module en module par un contact glissant sur le rail ; chaque rail commence par le contrôleur, une alimentation ou un **coupleur de rail**. Au plus 12 modules par rail, 20 rails par installation, deux alimentations supplémentaires par installation.

## Dans l'armoire sans recâblage

Niko prévoit deux façons de lire un contact sec, toutes deux en TBTS. L'**interface poussoirs** 550-20000 (4 entrées, 8 V de repos) se loge derrière le poussoir et admet **2 m** jusqu'au bouton : au bout des nappes de 5 à 30 m, elle sort de la spécification, et la poser aux murs tirerait le bus dans la maison. Reste le **module capteurs** 550-00210, en armoire, prévu pour les détecteurs de fumée, de mouvement et les contacts de porte : trois entrées, 50 m.

| Fonction | Module | Voies | Largeur | Ce qu'il faut savoir |
| --- | --- | --- | --- | --- |
| Contrôleur | Contrôleur connecté 550-00003 | logique, alimentation du bus 26 V 400 mA, 1 WAN + 3 LAN, USB | 6 modules | 24 modules d'armoire et 70 commandes sur l'alimentation intégrée ; disjoncteur ≤ 6 A ; 0 à 45 °C ; boutons TEST, SERVICE, PROG ; LED SERVER et STATUS ; **un par installation** |
| Alimentation supplémentaire | 550-00010 | 26 V 400 mA, 10 W | 4 modules | Une par 800 points supplémentaires ; **deux au plus** par installation ; protégée contre le court-circuit, la surtension et la surchauffe |
| Coupleur de rail | 550-00020 | bus et alimentation | 2 modules | En tête de chaque rail ; ≤ 20 m entre deux coffrets |
| 63 poussoirs | Module capteurs 550-00210 | **3 entrées** contacts secs NO ou NPN, 50 m | 2 modules | **21 modules** ; emploi en poussoir (appui court, long, double fonction) non décrit ; tension de repos, type d'entrée et points de consommation bus **non publiés** |
| 25 éclairages | 550-00106 ou 550-00103 | 6 ou 3 contacts 16 A | 4 ou 2 modules | **Relais bistables** ; 3 A par contact en LED ; **une seule phase par module** ; les sorties ne sont pas libres de potentiel : le module distribue la phase qu'il reçoit ; boutons manuels « temporaires » |
| 15 volets dont le store | Module moteurs 550-00130 | 3 moteurs, 6 A par contact | 4 modules | Boutons « D » de manœuvre manuelle ; **verrouillage des deux sens non mentionné** |
| 8 variateurs | Variateur universel 550-00340 | 2 voies, 5 à 400 VA à 45 °C | 4 modules | Type de lampe par micro-interrupteurs ; protections thermique et contre le court-circuit ; **restaure ses réglages après une coupure** ; pas à côté du contrôleur ; ventilateur si le coffret dépasse 35 °C |
| Fil pilote, cumulus, prises, arrosage, machines | 550-00106 | 6 contacts 16 A | 4 modules | Aucun module fil pilote ; relais externes à prévoir |

Les contacts secs des poussoirs conviennent aux jonctions IDC données pour 1 A, le courant de boucle n'étant pas publié. Les poussoirs bus, les écrans tactiles et les commandes « Digital black » ne sont pas retenus : ils demanderaient de tirer le bus jusqu'aux murs.

### Configuration minimale

Un contrôleur, un bus, nappes conservées : contrôleur 550-00003, 21 modules capteurs (63 entrées), cinq 550-00106 (30 contacts d'éclairage), cinq modules moteurs (15 volets), quatre variateurs (8 voies), un 550-00106 pour les contacts divers, une alimentation supplémentaire, neuf coupleurs de rail pour une dizaine de rails. **≈ 130 modules, soit ≈ 2,3 m de rail.** Les 36 modules d'armoire dépassent les 24 de l'alimentation intégrée ; une alimentation supplémentaire est comptée, le calcul en points du module capteurs n'étant pas publié.

La variante à 16 interfaces poussoirs en armoire tiendrait en ≈ 88 modules (≈ 1,6 m) pour ≈ 4 675 € HT, mais sort de la spécification des 2 m : elle n'est pas retenue.

### Configuration résiliente

Le manuel impose un contrôleur par installation et deux alimentations au plus ; la gamme n'a ni coupleur de ligne ni répéteur, et le coupleur de rail ne fait que prolonger le même bus. Trois segments indépendants sont donc **trois installations Niko distinctes** : trois contrôleurs, trois enregistrements, trois projets, reliés seulement par le réseau IP.

| Zone | Modules | Largeur |
| --- | --- | --- |
| Pièces de vie (20 poussoirs, 5 éclairages, 6 volets, 3 variateurs) | Contrôleur, 7 × 550-00210, 1 × 550-00106, 2 × 550-00130, 2 × 550-00340, coupleur | 42 |
| Chambres (21, 7, 5, 4) | Contrôleur, 7 × 550-00210, 550-00106 et 550-00103, 2 × 550-00130, 2 × 550-00340, coupleur | 44 |
| Pièces d'eau (22, 13, 4 dont le store, 1) | Contrôleur, 8 × 550-00210, 2 × 550-00106 et 1 × 550-00103, 2 × 550-00130, 1 × 550-00340, coupleur | 46 |

Avec un 550-00106 pour les contacts divers : **≈ 136 modules, soit ≈ 2,5 m de rail**, trois contrôleurs. Chaque zone compte 12 à 16 modules d'armoire : l'alimentation intégrée de son contrôleur suffit.

## Seule face à l'exigence

### Les sept règles

| Règle | Tenue | Pourquoi |
| --- | --- | --- |
| 1. Pas de calculateur entre le bouton et sa charge | **Non tenue** | Le poussoir attaque un module capteurs, qui « envoie l'adresse au contrôleur, qui active alors » l'action programmée ; le module de sortie n'agit que sur une impulsion de données du contrôleur. Aucune logique locale entrée → sortie documentée |
| 2. L'état vit dans un organe bistable | Tenue pour les éclairages, à confirmer | Relais bistables « à faible consommation » dans les modules de commutation : l'état survit par construction à la coupure ; le variateur restaure ses réglages. Mais aucun énoncé Niko sur le comportement des modules à la perte du bus ou du contrôleur |
| 3. La domotique ajoute, ne retire jamais | Non tenue | Le bus **est** la domotique : un ordre faux ou un contrôleur compromis commute n'importe quelle voie. Les boutons manuels des modules sont « écrasés par la prochaine communication bus » |
| 4. Une source et un fusible par zone, un fusible pour la domotique | Partielle | Un contrôleur, son alimentation et son disjoncteur par zone, oui ; mais poussoirs et domotique partagent le même bus et la même alimentation |
| 5. Barrière 4 kV et 8 mm, 0 V jamais au PE, parafoudres hors coffrets | Partielle | Bus et entrées en TBTS, séparation des câbles 230 V demandée ; **aucune tension d'essai, aucune catégorie de surtension publiée** ; aucun parafoudre recommandé ; la garantie exclut la surtension |
| 6. Replis choisis au câblage, essayés à la recette | Non tenue | Aucun repli documenté ; le fonctionnement des boutons manuels sans bus n'est pas précisé ; le mode TEST ne fait qu'allumer les LED des modules présents |
| 7. Isolement mesuré chaque année | Tenue | Rien ne l'empêche ; le journal du bus garde 3 à 7 jours de messages |

### Les causes communes

Dans la configuration résiliente, trois installations, un contrôleur par zone :

| Défaillance unique | Prive de ses boutons… | Pourquoi |
| --- | --- | --- |
| 1. Alimentation du bus | une zone | L'alimentation du bus est intégrée au contrôleur de la zone |
| 2. Court-circuit ou ligne collée sur le bus | une zone | Un bus par zone ; comportement et détection non documentés, seules les alimentations sont protégées |
| 3. Contrôleur central | une zone | Un contrôleur par zone, porteur de la logique de sa zone |
| 4. Logiciel figé | une zone | Le programme de chaque zone tourne dans son contrôleur ; aucun chien de garde documenté ; redémarrage manuel par le bouton SERVICE, jusqu'à deux minutes |
| 5. Mise à jour ratée | une zone | La mise à jour se fait contrôleur par contrôleur, à l'envoi du projet ; « l'installation ne doit en aucun cas être coupée » pendant ; conséquence d'un échec non documentée |
| 6. Licence, compte ou cloud | rien, à confirmer | Aucune licence. Mais la documentation Hobby API écrit que le contrôleur « requires internet connectivity for correct operation », et la LED SERVER passe au rouge sans serveur. Les intégrateurs tiers (openHAB) n'ont besoin d'Internet que pour valider le jeton, puis fonctionnent « strictement en réseau local » ; Niko ne dit pas ce qui s'arrête côté poussoirs. **Si la phrase s'applique au fonctionnement local, une coupure d'Internet prive toute la maison**, les trois contrôleurs à la fois |
| 7. Commutateur ou routeur | rien | Le chemin du bouton passe par le bus de sa zone ; le routeur intégré au contrôleur n'est pas sur ce chemin. Si la cause 6 se confirme, le routeur de la maison, qui porte l'Internet des trois contrôleurs, prend la même réserve |
| 8. Foudre sur le chemin du bus | une zone | Le bus reste dans l'armoire ; l'onde entre par les boucles des poussoirs (TBTS, 50 m) et frappe le module capteurs de la zone, dont l'isolement n'est pas publié |

**Total : 0 défaillance unique prive toute la maison**, sous réserve de la cause 6 (0 ou 1), 6 privent une zone. En configuration minimale, l'alimentation, le bus, le contrôleur, le logiciel figé, la mise à jour et la foudre privent toute la maison : **6**, et 7 si la dépendance à Internet se confirme.

Le découpage par zone demande trois installations que Niko n'a pas conçues pour cohabiter dans une maison : trois enregistrements, trois applications, trois jetons d'API, et aucun lien entre zones autre que le réseau. Dans la zone touchée, les éclairages restent sans doute dans leur état, mais aucun bouton ne répond et le fabricant ne garantit pas que les boutons des modules opèrent sans bus.

### Ce qui reste, panne par panne

| Panne | Ce qui reste |
| --- | --- |
| Contrôleur d'une zone, ou son alimentation | Les deux autres zones. Dans la zone : aucun bouton ; éclairages dans leur état (bistables, à confirmer) ; volets arrêtés ; boutons manuels des modules : fonctionnement sans contrôleur non précisé. Remplacement : nouveau contrôleur, nouvel enregistrement (adresse MAC et numéro de série), rechargement du projet ; redémarrage jusqu'à deux minutes |
| Bus d'une zone en court-circuit | Non documenté ; au pire la zone ; l'alimentation est protégée |
| Internet coupé | LED SERVER rouge ; perdus : application mobile, services Upgrade et Diagnostics, activation ou renouvellement du jeton Hobby API. Commande locale par les poussoirs : **à confirmer** |
| Réseau local ou passerelle | Les trois bus, sous la même réserve ; perdus : l'application, la Hobby API, la liaison entre zones |
| Coupure du secteur | Tout s'arrête ; au retour, le variateur restaure ses réglages, les relais bistables gardent leur position, chaque contrôleur redémarre en deux minutes au plus |
| Un module | Ses voies ; LED d'erreur (une impulsion toutes les deux secondes), mode TEST ; échange et réadressage dans le logiciel |
| Foudre par une boucle de poussoirs | Au pire la zone ; les autres zones. La garantie de quatre ans exclut la surtension |

## En dérivation sur le filaire V2

Les télérupteurs, les chaînes de volets et les variateurs à entrée locale gardent le chemin du bouton. Niko fournirait la couche domotique, avec quatre obstacles :

- **Sorties** : quinze 550-00106 (90 contacts) commandent les relais de couplage 38.51 de la V2. Mais ces contacts **ne sont pas secs** : chaque module distribue la phase qu'il reçoit, et il est donné pour 230 V. Pour des bobines 24 V, il faudrait vérifier auprès de Niko l'admissibilité d'une alimentation 24 V du module ; sinon, des 38.51 à bobine 230 V, au même prix que ceux de la recopie, commandés par la phase du module, ce qui ramène du 230 V sur le commun des contacts domotiques. Non chiffré en plus, le 38.51 étant déjà dans la V2.
- **Entrées** : 24 modules capteurs (72 entrées) lisent les contacts des relais de recopie, trois par module.
- **Limites d'installation** : 39 modules d'armoire pour une alimentation intégrée donnée pour 24 et deux alimentations supplémentaires au plus ; le calcul en points n'a pas pu être fait, faute de valeur publiée pour le module capteurs. La tenue en une seule installation est à confirmer.
- **Battement de cœur** : aucun bloc d'impulsion périodique n'a été trouvé ; les routines « Time schedule » et « Free function » existent, cadence minimale non lue. Le réarmement viendrait de la **passerelle**, par la Hobby API en MQTT, qui commuterait un contact relié au relais de garde ; si la passerelle, le contrôleur ou le jeton se tait, le relais de garde retombe en moins d'une seconde et la couche se débranche. Le **jeton d'API expire chaque année** et se renouvelle en ligne : un oubli débranche la domotique sans toucher aux boutons.
- **Logique et interface** : la passerelle, en MQTT ; les routines du contrôleur restent utilisables par l'application Niko.

Ce que la couche apporte : un courtier MQTT dans le contrôleur, chiffré en TLS, un binding openHAB officiel et deux intégrations Home Assistant communautaires. Ce qu'elle coûte : ≈ 8 100 € HT, ≈ 142 modules (≈ 2,5 m de rail, en plus des 1,6 à 2,1 m de la couche filaire : trois ou quatre coffrets), un jeton annuel, et Niko « ne supporte pas les applications construites avec la Hobby API ». Face à la Revolution Pi Connect 5 (≈ 581 € HT nue, plus ses modules d'entrées-sorties), c'est plus de dix fois le prix du contrôleur pour la même fonction ; face au serveur d'entrées-sorties léger ([dossier Modbus](modbus-es.md)), l'écart est plus grand encore.

## Foudre et isolement

- **Le bus reste dans l'armoire** avec les modules capteurs : il ne relie que le contrôleur et ses modules. Seules des boucles TBTS de contacts secs, 50 m au plus, sortent de l'armoire, comme aujourd'hui. Avec les interfaces poussoirs aux murs, le bus 26 V parcourrait la maison (100 à 250 m jusqu'au point le plus éloigné selon le diamètre du cuivre, 1 000 m au total).
- **TBTS imposée** : bus, interfaces et module capteurs sont en TBTS ; un capteur alimenté en 230 V doit passer par « une sortie isolée galvaniquement ou un relais intermédiaire » ; les câbles à très basse tension se tiennent séparés des câbles 230 V, le câble réseau du contrôleur blindé.
- **Tensions d'essai** : **aucune valeur en kV, aucune catégorie de surtension, aucun type d'entrée** (optocouplée ou non) dans les pages du manuel consultées. La barrière de 4 kV et 8 mm de la V2 est à faire attester ; sans attestation, un 38.51 devant chaque voie.
- **Sorties non isolées** : les modules de commutation distribuent la phase reçue ; en dérivation, les contacts côté TBTS devraient venir d'un relais intermédiaire, ce que la V2 prévoit déjà avec les 38.51.
- **Parafoudres** : aucune recommandation Niko trouvée ; les conditions de garantie (quatre ans) excluent les dommages « dus à des causes externes telles que l'humidité ou la surtension ».
- **Retours de terrain** : aucun forum n'a pu être lu.

## Logiciel, paramétrage et passerelle Essensys

| Point | Ce qu'on a trouvé |
| --- | --- |
| Outil | **Logiciel de programmation Niko Home Control II**, gratuit, Windows et Mac, destiné à « l'installateur et l'utilisateur final averti » ; première connexion validée par le bouton TEST du contrôleur dans les dix minutes ; application Niko Home gratuite. Le manuel matériel demande un « installateur enregistré » |
| Enregistrement | Compte « My Niko Home Control », adresse MAC et numéro de série, ordinateur en ligne : requis pour l'application mobile, les services Upgrade et Diagnostics et le jeton d'API |
| Mise à jour | À l'envoi du projet (« Check for upgrades », « Upgrade ») ; ne jamais couper pendant ; retour arrière non documenté |
| Sécurité | MQTT en TLS 1.2 ou 1.3, certificat d'autorité fourni par Niko, jeton JWT |
| API pour la passerelle | **Hobby API** : courtier MQTT dans le contrôleur, port 8884, charges JSON, sujets `hobby/control/devices/…`, découverte DNS-SD, REST HTTPS pour l'historique des mesures ; jeton **renouvelé chaque année**, obtenu dans le logiciel, contrôleur en ligne au premier usage ; « Niko et les installateurs professionnels ne supportent pas » les applications construites dessus. Une « System integrator API » existe pour les professionnels |
| Bibliothèques libres | Binding **openHAB** officiel (pont « bridge2 » sur 8884, ou profil tactile sur 8883) ; Home Assistant : l'intégration officielle ne couvre que la génération I, deux intégrations HACS couvrent la II ; Node-RED cité par Niko. Bibliothèque Go : non vérifiée |
| Modbus, KNX | Non trouvés dans la documentation des partenaires |
| Cloud | Ports sortants 53, 80, 443, 22 et 123 ; « requires internet connectivity for correct operation » ; openHAB : « strictement en réseau local » après la validation du jeton |

Côté passerelle, le backend Go doit être client MQTT en TLS avec un jeton JWT, ce qui est courant. L'estimation est de **deux à quatre semaines-personne** pour l'intégration (estimation de cette étude, sans essai), plus une à deux semaines de programmation Niko, et une tâche d'exploitation : renouveler le jeton chaque année, en ligne. ≈ 3 à 6 semaines avant la bascule. Le contrôleur fait tourner un système propriétaire dans l'armoire ; aucun code du projet n'y tourne.

## Nomenclature et coût estimé

Prix relevés le 24 octobre 2026 chez Elektramat (Pays-Bas), qui affiche le **hors TVA** à côté du TTC néerlandais (21 %) ; le hors TVA est repris tel quel. Les grossistes belges n'affichent pas de prix sans compte et Niko ne publie pas de tarif. Les prix des modules de mesure, du compteur d'impulsions et des écrans n'ont pas été relevés.

### Configuration minimale

| Poste | Référence | Qté | Prix unitaire HT | Total HT | Source |
| --- | --- | --- | --- | --- | --- |
| Contrôleur | 550-00003 | 1 | 691,05 € | 691 € | Elektramat |
| Entrées | Module capteurs 550-00210 | 21 | 145,33 € | 3 052 € | Elektramat |
| Éclairages, divers | 550-00106 | 6 | 205,79 € | 1 235 € | Elektramat |
| Volets | Module moteurs 550-00130 | 5 | 187,81 € | 939 € | Elektramat |
| Variateurs | 550-00340 | 4 | 272,54 € | 1 090 € | Elektramat |
| Alimentation supplémentaire | 550-00010 | 1 | 188,01 € | 188 € | Elektramat |
| Coupleurs de rail | 550-00020 | 9 | 46,74 € | 421 € | Elektramat |
| **Matériel** | | | | **7 616 € HT** | |
| Logiciel | Logiciel de programmation Niko | 1 | 0 € | 0 € | guide.niko.eu |
| **Total** | | | | **≈ 7 600 € HT** | |

Les 21 modules capteurs pèsent 40 % du total : c'est le prix de lire 63 contacts secs trois par trois.

### Configuration résiliente

| Poste | Référence | Qté | Prix unitaire HT | Total HT |
| --- | --- | --- | --- | --- |
| Contrôleurs de zone | 550-00003 | 3 | 691,05 € | 2 073 € |
| Entrées | Module capteurs 550-00210 | 22 | 145,33 € | 3 197 € |
| Éclairages, divers | 550-00106 | 5 | 205,79 € | 1 029 € |
| Éclairages | 550-00103 | 2 | 157,96 € | 316 € |
| Volets | Module moteurs 550-00130 | 6 | 187,81 € | 1 127 € |
| Variateurs | 550-00340 | 5 | 272,54 € | 1 363 € |
| Coupleurs de rail | 550-00020 | 3 | 46,74 € | 140 € |
| **Matériel** | | | | **9 245 € HT** |
| Logiciel | Logiciel de programmation Niko | 1 | 0 € | 0 € |
| **Total** | | | | **≈ 9 200 € HT** |

Soit ≈ 1 600 € HT de plus que la configuration minimale, pour passer de 6 à 0 défaillance unique touchant toute la maison, la réserve sur Internet restant entière.

### Couche domotique en dérivation

| Poste | Référence | Qté | Total HT |
| --- | --- | --- | --- |
| Contrôleur | 550-00003 | 1 | 691 € |
| Sorties vers les relais de couplage | 550-00106 | 15 | 3 087 € |
| Entrées de recopie | Module capteurs 550-00210 | 24 | 3 488 € |
| Alimentations supplémentaires | 550-00010 | 2 | 376 € |
| Coupleurs de rail | 550-00020 | 10 | 467 € |
| **Matériel** | | | **8 109 € HT** |
| Logiciel | Logiciel de programmation Niko | 1 | 0 € |
| **Total** | | | **≈ 8 100 € HT**, ≈ 142 modules, tenue en une installation à confirmer |

### Ce qui n'est pas dans les totaux

- **Fonctions à reporter** : alarme par la routine « Warning mode » (lampes, clignotement, sirène par un relais, déclenchement manuel) et « Motion detection » ; pas de centrale certifiée. Écran : écran tactile IP 550-20103, prix non relevé ; l'application est incluse. Délestage : routine « Peak mode » (ordre de délestage, 1 à 100 kW, modes direct et prédictif), qui demande un module de mesure bus (prix non relevé).
- **Fil pilote** : aucune offre Niko ; relais externes.
- **Verrouillage des volets** : non mentionné sur le module moteurs ; un verrouillage câblé externe n'est pas chiffré.
- **Électricien** : de l'ordre de 4 à 6 jours (estimation sans devis).
- **Logiciel** : ≈ 3 à 6 semaines-personne (programmation Niko et passerelle), plus le renouvellement annuel du jeton.
- **Place** : ≈ 2,3 m (minimale), ≈ 2,5 m (par zone), ≈ 2,5 m (dérivation, en plus de la couche filaire).

## Ouverture et pérennité

- **Protocole propriétaire** : le bus Niko n'a qu'un fabricant. L'ouverture logicielle passe par la Hobby API (MQTT et JSON, locale, jeton annuel), sans support du fabricant, et par une API intégrateur pour les professionnels.
- **Générations** : le contrôleur de la génération I est « non compatible » avec le logiciel 2.x ; Niko propose de le retourner contre un « paquet de migration ». Les composants Nikobus n'ont « aucune alternative équivalente » et sont tous à remplacer ; un écran tactile a été remplacé puis son remplaçant marqué « arrêté ». Les modules d'armoire de la génération I semblent réutilisables, sans affirmation explicite. Le passage à la génération II est « fortement recommandé pour des raisons de sécurité ».
- **Vente et prix** : grossistes, aucun prix public ; logiciel gratuit ; « installateur enregistré » demandé par le manuel. Garantie de quatre ans.
- **Cloud** : enregistrement et Internet requis pour l'application, les services et le jeton ; la phrase « requires internet connectivity for correct operation » n'est pas commentée par Niko. Aucune déclaration « sans cloud ».
- **Communauté** : openHAB (binding officiel), Home Assistant (deux intégrations communautaires), Node-RED ; forums non consultés.

## Verdict

- **Seule** : Niko Home Control II reprend les 63 poussoirs sans toucher un fil, mais avec un module de capteurs à trois entrées détourné de son usage, et au prix d'une armoire et demie. Un contrôleur par installation oblige à trois installations pour éviter la panne unique ; chaque bouton passe par son contrôleur, sans repli documenté, et le fabricant écrit que le contrôleur a besoin d'Internet sans dire pour quoi. C'est une solution pour une maison câblée en bus Niko, pas pour celle-ci.
- **En dérivation** : la couche la plus chère et la plus large du comparatif, avec des sorties qui ne sont pas des contacts secs, un jeton d'API à renouveler chaque année et aucun signal cyclique identifié. Rien ne la recommande face à la Revolution Pi ou à un serveur Modbus.
- **À qui elle convient** : à qui construit ou rénove en tirant le bus Niko jusqu'aux poussoirs, avec un installateur Niko, et accepte un contrôleur unique enregistré chez le fabricant.

## Sources

Toutes consultées le 24 octobre 2026.

1. [Niko, à propos](https://www.niko.eu/en/about-niko) : fondation en 1919, Sint-Niklaas, 700 salariés, dix filiales.
2. [Câblage bus ou traditionnel](https://guide.niko.eu/en/hmnhc2/lv/bus-wiring-or-traditional-wiring) : contrôleur connecté 550-00003 ou concentrateur sans fil.
3. [Contrôleur connecté](https://guide.niko.eu/en/hmnhc2/lv/connected-controller) : logique locale, 26 V 400 mA, 24 modules et 70 commandes, 6 modules, LED SERVER et STATUS, boutons, disjoncteur 6 A, ports sortants, un contrôleur par installation.
4. [Préparation d'une installation bus](https://guide.niko.eu/en/hmnhc2/lv/installation-preparations-for-bus-wiring) : câble non polarisé, topologie libre, longueurs, séparation du 230 V, 12 modules par rail, 20 rails, deux alimentations, 20 m entre coffrets.
5. [Coupleur de rail](https://guide.niko.eu/en/hmnhc2/lv/rail-coupler) : 2 modules, bornes, 20 m.
6. [Alimentation supplémentaire](https://guide.niko.eu/en/hmnhc2/lv/additional-power-supply-unit) : 26 V 400 mA, 10 W, points, mise en parallèle, protections.
7. [Module capteurs à contacts secs](https://guide.niko.eu/en/hmnhc2/lv/digital-potential-free-sensor-module) : 3 entrées, TBTS, 50 m, usages prévus.
8. [Interfaces poussoirs](https://guide.niko.eu/en/hmnhc2/lv/push-button-interfaces) : 550-20000 et 550-20025, 8 V, 2 m, TBTS.
9. [Modules de commutation](https://guide.niko.eu/en/hmnhc2/lv/switching-modules) : 3 et 6 contacts, 16 A, relais bistables, 3 A en LED, une phase, boutons manuels temporaires, LED d'erreur.
10. [Module moteurs](https://guide.niko.eu/en/hmnhc2/lv/motor-module) : 3 moteurs, 6 A, boutons D.
11. [Variateur universel](https://guide.niko.eu/en/hmnhc2/lv/universal-dimming-module) : 2 voies, 5 à 400 VA, micro-interrupteurs, protections, restauration après coupure, ventilation.
12. [Compteur d'impulsions](https://guide.niko.eu/en/hmnhc2/lv/pulse-counter) et [modules de mesure](https://guide.niko.eu/en/hmnhc2/lv/electricity-measuring-modules) : TBTS, 20 voies par installation.
13. [Garantie](https://guide.niko.eu/en/hmnhc2/lv/guarantee-provisions) : quatre ans, exclusion de la surtension, grossistes.
14. [Avertissements d'installation](https://guide.niko.eu/en/hmnhc2/lv/warnings-regarding-installation) : installateur enregistré.
15. [Notes de version](https://guide.niko.eu/en/rnnhc/lv) : logiciel 2.28.1.
16. [Paramètres des poussoirs](https://guide.niko.eu/en/smnhc2/lv/general-controls-push-buttons) : appui court, appui long, mode poussoir, double fonction, décalage.
17. [Envoi du projet](https://guide.niko.eu/en/smnhc2/lv/uploading), [composants](https://guide.niko.eu/en/smnhc2/lv/components) et [communication bus](https://guide.niko.eu/en/smnhc2/lv/bus-communication) : mise à jour à l'envoi, diagnostic, journal de 3 à 7 jours.
18. [Enregistrement de l'installation](https://guide.niko.eu/en/smnhc2/lv/register-installation) et [première connexion](https://guide.niko.eu/en/smnhc2/lv/connecting-your-computer-for-the-first-time-to-the) : compte, adresse MAC et numéro de série, bouton TEST.
19. [Logiciel de programmation et application](https://guide.niko.eu/en/smnhc2/lv/programming-software-niko-home-app) : gratuit, Windows et Mac, public visé.
20. [Peak mode](https://guide.niko.eu/en/smnhc2/lv/peak-mode), [Warning mode](https://guide.niko.eu/en/smnhc2/lv/warning-mode), [gestion de l'énergie](https://guide.niko.eu/en/smnhc2/lv/energy-management-with-niko-home-control), [commande d'ambiances](https://guide.niko.eu/en/umnhc2/lv/mood-control) : délestage, dissuasion, mesure, ambiances.
21. [Hobby API](https://guide.niko.eu/en/connhc2/lv/hobby-api) et [plateformes d'intégration](https://guide.niko.eu/en/connhc2/lv/integration-platforms) : prérequis, jeton annuel, absence de support, API intégrateur.
22. [Hobby API, documentation technique v1.4](https://github.com/joleys/niko-home-control-II/blob/master/docs/documentation.pdf) (25/03/2025) : MQTT 8884 en TLS, JWT, DNS-SD, REST, « requires internet connectivity for correct operation ».
23. [Migration de la génération I](https://guide.niko.eu/en/unhc/lv/1-identify-hardware-and-required-replacements) et [mise à niveau](https://guide.niko.eu/en/unhc/lv) : contrôleur non compatible, Nikobus sans équivalent, écrans, raisons de sécurité.
24. [Manuel utilisateur](https://guide.niko.eu/en/umnhc2/lv) : écran 550-20102 arrêté, variation, ambiances.
25. [Binding openHAB Niko Home Control](https://www.openhab.org/addons/bindings/nikohomecontrol/) : pont « bridge2 », jeton d'un an, profil tactile, « strictement en réseau local ».
26. [Intégration Home Assistant officielle](https://www.home-assistant.io/integrations/niko_home_control/), [hass-nhc2](https://github.com/filipvh/hass-nhc2) et [niko-home-control-II](https://github.com/joleys/niko-home-control-II) : génération I seule en officiel, deux intégrations communautaires, Internet pour le jeton seulement.
27. Prix hors TVA, Elektramat : [contrôleur 550-00003](https://www.elektramat.nl/catalogsearch/result/?q=550-00003), [module capteurs 550-00210](https://www.elektramat.nl/niko-sensormodule-3-ingangen-home-control-550-00210/) ; alimentation 550-00010, coupleur 550-00020, modules 550-00103, 550-00106, 550-00130, 550-00340 et interface poussoirs d'après les pages de résultats de la même boutique.

!!! note "À confirmer auprès des fabricants"
    Le comportement des modules quand le contrôleur s'arrête ou que le bus tombe (maintien des relais bistables, boutons manuels sans bus) ; la portée exacte de « requires internet connectivity for correct operation » et ce qui survit à une coupure d'Internet ; l'admissibilité du module capteurs 550-00210 comme entrée poussoir, ses modes d'appui, sa tension de repos et ses points de consommation ; les tensions d'essai, la catégorie de surtension et le type des entrées ; le verrouillage des deux sens sur le module moteurs ; le comportement du bus en court-circuit ; le retour arrière après une mise à jour échouée ; l'existence d'une impulsion périodique pour le relais de garde ; l'alimentation en 24 V d'un module de commutation ; les prix belges et ceux des écrans et modules de mesure ; les dates de la génération I et sa politique de support.
