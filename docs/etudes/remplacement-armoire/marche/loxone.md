---
title: "Loxone : remplacer l'armoire sans recâblage"
description: "Loxone Miniserver, DI Extensions, Relay Extensions et Dimmer Extensions sur le bus Link pour remplacer les quatre cartes de l'armoire ESSENSYS sans toucher aux fils. Seul, chaque bouton passe par le Miniserver, sans logique locale ni commande manuelle sur les cartes ; en dérivation, un contrôleur sans licence mais cher en entrées-sorties. Environ 6 700 € HT en configuration par zone."
---

# Loxone

Loxone est un système domotique propriétaire autrichien, très répandu en rénovation, construit autour d'un contrôleur unique, le Miniserver, et de cartes d'entrées-sorties déportées sur un bus d'armoire, le Link. Ce dossier du [comparatif](index.md) regarde s'il peut reprendre les 63 poussoirs et toutes les charges sans changer un fil, et ce qu'il reste quand le Miniserver se tait.

!!! abstract "Synthèse"
    - **Seule** : Loxone remplace les quatre cartes sans recâblage et le Link ne sort pas de l'armoire. Mais le système est centralisé : les Extensions n'ont ni logique locale ni commande manuelle, et chaque poussoir passe par le Miniserver : **règle 1 non tenue**. En configuration par zone (un Miniserver Compact, un Link, une alimentation par zone), **aucune des huit défaillances uniques ne prive toute la maison de ses boutons**, mais six d'entre elles privent une zone de 20 à 22 boutons. L'état des relais à la perte du Link ou du Miniserver n'est pas documenté par Loxone.
    - **En dérivation** : un contrôleur sans licence ni cloud obligatoire, une API locale documentée, mais des cartes d'entrées-sorties chères pour 85 sorties et 70 entrées, un système propriétaire sur carte microSD dans l'armoire, et un battement de cœur dont le comportement au gel du Miniserver n'est pas documenté. Plusieurs fois le prix de la Revolution Pi Connect 5 nue.
    - **Coût estimé** : ≈ 3 900 € HT en configuration minimale, ≈ 6 700 € HT par zone, logiciel gratuit ; ≈ 3 950 € HT en couche domotique seule. Prix hors TVA de la boutique officielle, octobre 2026.
    - **Réserve** : estimations à confirmer par un électricien, des devis, le fabricant et des essais. La vente aux particuliers n'est pas confirmée (compte « Partner » avec licence professionnelle) ; la fiche et la largeur des alimentations n'ont pas été lues.

## Principe et gamme

Loxone Electronics GmbH (Kollerschlag, Autriche) existe depuis 2009 ; le premier Miniserver est sorti en 2010, la deuxième génération (réf. 100335) en décembre 2020. Le fabricant annonce plus de 1 200 salariés.

Le système est **centralisé** : le Miniserver « sert d'unité de commande centrale » et exécute toute la logique, en blocs fonctions (plus de 150) dessinés dans Loxone Config. Les Extensions ne sont que des cartes d'entrées-sorties : le Miniserver voit une Relay Extension comme 14 actionneurs 0/1 et un état « en ligne ». Le système d'exploitation et le programme vivent sur une carte microSD dans le Miniserver.

Trois supports :

- **Link** : bus propriétaire d'armoire, en chaîne stricte depuis le Miniserver, 30 Extensions au plus, 500 m, terminaison 120 Ω sur la dernière carte. La couche physique n'est pas nommée par Loxone ; un utilisateur parle d'émetteurs-récepteurs CAN.
- **Tree** : bus propriétaire pour les périphériques décentralisés (boutons tactiles, Nano DI Tree, Nano 2 Relay Tree), 50 appareils et 500 m par branche, topologie libre. Il sortirait de l'armoire : les produits Tree ne sont pas retenus.
- **Air** : radio 868 MHz, hors périmètre.

Le Miniserver a aussi un port LAN (HTTPS, WebSocket, Modbus TCP en client). L'Extension d'origine (12 entrées, 8 relais, analogique) a été arrêtée en 2020 et remplacée par des cartes spécialisées : DI Extension, Relay Extension, Dimmer Extension, AI et AO Extension.

## Dans l'armoire sans recâblage

Les poussoirs sont des contacts secs : ils commutent le **+24 V** de l'alimentation Loxone vers des entrées à seuil de tension. Le Link reste dans l'armoire ; seules les nappes des poussoirs parcourent la maison, comme aujourd'hui, mais sous 24 V au lieu de 5 V.

| Fonction | Module | Voies | Largeur | Ce qu'il faut savoir |
| --- | --- | --- | --- | --- |
| Contrôleur | Miniserver 100335 | 8 entrées, 8 relais 10 A, 4 entrées 0-10 V, Link, Tree, LAN | 9 modules | Alimentation 19,2 à 30 V, 1,85 W ; relais de couplage recommandés au-delà de 5 A ; horloge avec 64 h de réserve ; programme sur microSD |
| Contrôleur de zone | Miniserver Compact 100512 | 4 entrées, 2 relais 16 A, Link ou Tree, Air, LAN | 6 modules | Même logiciel ; retenu pour la configuration par zone |
| 63 poussoirs | DI Extension 100283 | 20 entrées pour contacts secs | 2 modules | Niveau 1 de 9,7 à 28 V, 67 kΩ (≈ 0,36 mA à 24 V, calcul d'après la fiche) ; impulsion de 2 ms au moins ; bornes 0,14 à 0,5 mm² ; longueur de ligne admise et type d'entrée (optocouplée ou non) **non publiés** |
| 25 éclairages, divers | Relay Extension 100038 | 14 relais 16 A, contacts secs | 9 modules | 48 A au total par carte (limite thermique), 24 A d'appel ; -40 à 40 °C ; coupure thermique de toutes les sorties ; **aucun bouton de commande manuelle** ; état à la perte du Link **non documenté** |
| 15 volets dont le store | Relay Extension 100038 | 2 relais par volet | | **Aucun verrouillage matériel** des deux sens : le verrouillage est logiciel, dans le bloc « Automatic Blinds » du Miniserver |
| 8 variateurs | Dimmer Extension 100029 | 4 voies, découpage de phase | 9 modules | Voie 1 : 400 W, voies 2 à 4 : 210 W ; LED 200 et 105 VA ; 8 entrées en plus ; aucune protection contre le court-circuit **documentée**, seule une coupure thermique |
| Fil pilote, cumulus, prises, arrosage, machines | Relay Extension 100038 | contacts 16 A | | Aucun module fil pilote ; relais externes à prévoir |
| Alimentation 24 V | Power Supply 4,2 A 100617 ou 10 A 200035 | | **non lue** | Fiches non consultées ; Loxone recommande des alimentations séparées pour la commande, les périphériques et l'éclairage LED ; les 0 V de toutes les alimentations doivent être reliés |
| Pontets Link et 24 V | Shunting Wire 200300 et 200301 | | | Pontets entre le Miniserver et les Extensions |

Le courant d'entrée (≈ 0,36 mA) convient aux jonctions IDC données pour 1 A. La longueur admise des lignes d'entrée n'est pas publiée : seul le Link est spécifié à 500 m. Les boutons tactiles Tree, les Nano DI Tree et les écrans ne sont pas retenus : ils demanderaient de tirer le bus Tree jusqu'aux murs.

### Configuration minimale

Un Miniserver, un Link, une alimentation, tout dans l'armoire : Miniserver 100335, trois DI Extension (60 entrées plus les 8 du Miniserver : 68), quatre Relay Extension (56 relais plus 8 : 64, pour 25 éclairages, 30 relais de volets et six contacts divers), deux Dimmer Extension (8 voies, 16 entrées de réserve), une alimentation 24 V. **≈ 73 à 75 modules, soit ≈ 1,3 m de rail**, dont 4 à 6 modules estimés pour l'alimentation, sans bornes, disjoncteurs ni parafoudres. Bilan 24 V : ≈ 20 W, moins de 1 A.

### Configuration résiliente

Un Miniserver **ne segmente pas son Link** : une chaîne, une terminaison. Trois segments indépendants demandent **trois Miniservers**, un par zone, chacun avec son Link, ses Extensions et son alimentation, reliés par le réseau local en mode « Client-Gateway » de Loxone Config, dont la page de documentation n'a pas pu être lue. La gamme n'a ni coupleur ni répéteur Link.

| Zone | Modules | Largeur |
| --- | --- | --- |
| Pièces de vie (20 poussoirs, 5 éclairages, 6 volets, 3 variateurs) | Miniserver Compact, 1 DI Extension, 2 Relay Extension, 1 Dimmer Extension, alimentation | ≈ 35 + alimentation |
| Chambres (21, 7, 5, 4) | Miniserver Compact, 2 DI Extension, 2 Relay Extension, 1 Dimmer Extension, alimentation | ≈ 37 + alimentation |
| Pièces d'eau (22, 13, 4 dont le store, 1) | Identique aux chambres | ≈ 37 + alimentation |

Les contacts divers (fil pilote, cumulus, prises, arrosage, machines) prennent les relais libres de la zone des pièces de vie, qui en a treize. **≈ 110 modules, soit ≈ 2 m de rail** sans les trois alimentations ; trois Miniservers, trois Links. Un bouton d'une zone qui commanderait une charge d'une autre zone passerait par le réseau local ; le découpage retenu l'évite.

## Seule face à l'exigence

### Les sept règles

| Règle | Tenue | Pourquoi |
| --- | --- | --- |
| 1. Pas de calculateur entre le bouton et sa charge | **Non tenue** | Le poussoir attaque une entrée d'Extension, qui remonte l'état par le Link ; le programme du Miniserver commande le relais d'une autre Extension. Aucune logique locale dans les Extensions, aucune commande manuelle en face avant : sans Miniserver, aucun bouton n'agit |
| 2. L'état vit dans un organe bistable | Non tenue | L'état vit dans le programme du Miniserver. La consommation de la Relay Extension passe de 0,7 W relais ouverts à 3,8 W : ses relais sont monostables (déduction d'après la fiche, non confirmée). Leur état à la perte du Link ou du Miniserver n'est pas documenté |
| 3. La domotique ajoute, ne retire jamais | Non tenue | Le Miniserver **est** la domotique : un bloc faux, un programme corrompu ou un accès pirate commute n'importe quelle voie |
| 4. Une source et un fusible par zone, un fusible pour la domotique | Partielle | Une alimentation 24 V et un disjoncteur par zone, oui ; mais les poussoirs sont alimentés par le 24 V du système, et rien ne sépare leur fusible de celui des cartes |
| 5. Barrière 4 kV et 8 mm, 0 V jamais au PE, parafoudres hors coffrets | Partielle | TBTS 24 V possible ; **seule tension publiée : 2,5 kV d'impulsion sur les sorties relais** ; isolement entre entrées, Link et 230 V non publié ; 0 V de toutes les alimentations reliés par consigne ; aucun parafoudre spécifié |
| 6. Replis choisis au câblage, essayés à la recette | Non tenue | Aucun repli documenté à la perte du Link ; le seul comportement décrit d'un Miniserver en panne est la boucle de redémarrage sur carte microSD illisible |
| 7. Isolement mesuré chaque année | Tenue | Rien ne l'empêche ; le diagnostic Link signale les pertes de paquets et les différences de potentiel |

### Les causes communes

Dans la configuration résiliente, trois Miniservers Compact, un par zone :

| Défaillance unique | Prive de ses boutons… | Pourquoi |
| --- | --- | --- |
| 1. Alimentation du système | une zone | Une alimentation 24 V par zone ; elle alimente le Miniserver, les Extensions et les boucles des poussoirs de la zone |
| 2. Court-circuit ou ligne collée sur le Link | une zone | Un Link par zone ; comportement non documenté par Loxone, seul le diagnostic de perte de paquets est décrit |
| 3. Contrôleur central | une zone | Un Miniserver par zone exécute le programme de sa zone ; le rôle du Miniserver passerelle en mode Client-Gateway n'a pas pu être lu |
| 4. Logiciel figé | une zone | Le programme de chaque zone tourne dans son Miniserver ; aucun chien de garde externe documenté |
| 5. Mise à jour ratée | une zone | Si l'on met à jour un Miniserver à la fois ; les Extensions sont mises à jour en arrière-plan et « restent en général opérationnelles » ; la conséquence d'un échec n'est pas documentée |
| 6. Licence, compte ou cloud | rien | Loxone Config est gratuit, sans licence ; le fonctionnement local n'exige ni compte ni cloud ; Remote Connect est optionnel |
| 7. Commutateur ou routeur | rien | Le chemin du bouton passe par le Link de sa zone, pas par le réseau local |
| 8. Foudre sur le chemin du bus | une zone | Le Link reste dans l'armoire ; l'onde entre par les lignes de poussoirs, qui portent le 24 V de la zone jusqu'aux entrées (isolement non publié). Un utilisateur a perdu un Miniserver et cinq Extensions sur un même Link |

**Total : 0 défaillance unique prive toute la maison**, 6 privent une zone. En configuration minimale, l'alimentation, le Link, le Miniserver, le logiciel figé, la mise à jour et la foudre privent toute la maison : **6**.

Le découpage par zone divise la panne par trois, il ne la supprime pas : dans la zone touchée, aucun bouton ne répond, aucune manette ne permet d'allumer, et Loxone ne dit pas si les lumières restent dans leur état. Les pannes de Miniserver les plus citées par les utilisateurs sont la carte microSD et l'alimentation ; le forum le qualifie de point unique de défaillance.

### Ce qui reste, panne par panne

| Panne | Ce qui reste |
| --- | --- |
| Miniserver d'une zone (carte microSD, alimentation interne) | Les deux autres zones. Dans la zone : aucun bouton, aucune commande manuelle ; état des relais et des variateurs non documenté. Remplacement : nouveau Miniserver, restauration du programme, carte microSD Loxone ; redémarrage jusqu'à une minute |
| Alimentation 24 V d'une zone | Les deux autres zones. Dans la zone : Miniserver, Extensions et boucles des poussoirs sans tension ; relais ouverts s'ils sont monostables (déduction), donc lumières éteintes |
| Link d'une zone coupé | Les Extensions clignotent en rouge ; le Miniserver signale la carte hors ligne (délai non chiffré) ; état des relais non documenté |
| Réseau local ou passerelle | Tout le local de chaque zone ; perdus : l'application, la liaison entre zones, Remote Connect |
| Coupure du secteur | Tout s'arrête ; au retour, chaque Miniserver redémarre (jusqu'à une minute, plus en Client-Gateway) ; état de reprise des relais non documenté. Option : Power Supply & Backup à batterie 36 V, 625 € HT, coffret de 100 l recommandé |
| Une Extension | Ses voies ; au-delà de 40 °C ambiants, la coupure thermique ouvre toutes les sorties de la carte |
| Foudre par une ligne de poussoirs | Au pire la zone entière ; les autres zones |

## En dérivation sur le filaire V2

Les télérupteurs, les chaînes de volets et les variateurs à entrée locale gardent le chemin du bouton. Loxone fournit la couche domotique :

- **Sorties** : six Relay Extension (84 relais) et les 8 relais du Miniserver, soit 92 contacts secs 16 A, commandent les bobines 24 V des relais de couplage 38.51 de la V2. Les contacts 16 A sont très surdimensionnés pour une bobine ; la gamme n'a pas de carte de sorties plus fine sur rail DIN.
- **Entrées** : quatre DI Extension (80 entrées) et les 8 du Miniserver lisent les contacts des relais de recopie. Le 38.51 de recopie fournit la barrière de 6 kV que l'isolement non publié des entrées ne garantit pas.
- **Battement de cœur** : un bloc fonction du Miniserver, relancé par une commande périodique de la passerelle, tient un relais dont le contact alimente le relais de garde ; si la passerelle se tait, la minuterie expire et le relais retombe. C'est donc le **Miniserver** qui réarme. S'il se fige ou perd le Link, l'état de ce relais n'est pas documenté : le chien de garde matériel de la V2 reste indispensable, et il attend un signal alterné qu'un relais mécanique à 200 ms ne fournira pas longtemps. La cadence et le support du signal se fixent au banc ; aucune fonction « chien de garde » nommée n'a été trouvée dans la documentation.
- **Logique et interface** : la passerelle, par l'API WebSocket locale du Miniserver, ou le Miniserver lui-même, dont les blocs (éclairage, volets, délestage, alarme) sont riches.
- **Durées bornées** : les blocs du Miniserver limitent la durée d'une impulsion ; le câblage de la V2 la borne de toute façon.

Ce que la couche apporte : un contrôleur sans licence, mis à jour gratuitement depuis 2010 jusque sur la première génération, une API locale documentée, une communauté active (loxforum, LoxBerry, PyLoxone). Ce qu'elle coûte : ≈ 3 950 € HT, ≈ 71 modules plus l'alimentation (≈ 1,3 m de rail, en plus des 1,6 à 2,1 m de la couche filaire), un système propriétaire sur carte microSD dans l'armoire, Windows pour Loxone Config. Face à la Revolution Pi Connect 5 (≈ 581 € HT nue, plus ses modules d'entrées-sorties), Loxone coûte le prix d'une armoire pour la même fonction ; face au serveur d'entrées-sorties léger ([dossier Modbus](modbus-es.md)), il est plusieurs fois plus cher et plus large.

## Foudre et isolement

- **Le Link reste dans l'armoire** avec des poussoirs classiques sur DI Extension : il ne relie que le Miniserver et ses Extensions. Les nappes des poussoirs portent le **24 V de l'alimentation Loxone**, pas une tension séparée : l'îlot des boutons et l'îlot du contrôleur sont le même îlot, à la différence de la V2.
- **Tensions d'essai** : les fiches du Miniserver, de la Relay Extension et de la Dimmer Extension donnent 2,5 kV d'impulsion sur les sorties relais (UL 60730-1, degré de pollution 2) ; la DI Extension est certifiée UL 62368-1 sans valeur. **Aucune tension d'isolement entre Link, entrées et contacts 230 V n'est publiée.** La barrière de 4 kV et 8 mm de la V2 est donc à faire attester ; sans attestation, un 38.51 devant chaque voie, comme la V2 le prévoit en dérivation.
- **TBTS ou PELV** : Loxone écrit qu'une « vraie installation Loxone » n'utilise que des alimentations à très basse tension, mais que dans beaucoup d'installations le 0 V finit relié au PE par des appareils tiers ; la Power Supply & Backup demande même ce raccordement pour une installation PELV. Le 0 V de toutes les alimentations doit être commun.
- **Parafoudres** : Loxone n'en vend pas et n'en spécifie pas ; un billet du fabricant recommande d'en prévoir. Les utilisateurs citent des parafoudres pour bus CAN (Blitzart) sur le Link et le Tree.
- **Retour de terrain** : après une foudre dans la maison (installation en PELV), un utilisateur a perdu un Miniserver, une Relay Extension, deux Multi Extensions, une 1-Wire et une RS-485 sur le même Link ; un intervenant évoque des transils et des émetteurs-récepteurs CAN à remplacer.

## Logiciel, paramétrage et passerelle Essensys

| Point | Ce qu'on a trouvé |
| --- | --- |
| Outil | **Loxone Config** 17.2 (Windows 10 64 bits, carte graphique OpenGL 4.5) : « gratuit pour toujours, sans licence, mises à jour gratuites », téléchargement libre ; double authentification introduite en 17.2 |
| Achat | Boutique officielle réservée aux comptes « Partner » avec licence professionnelle ; vente directe aux particuliers **non confirmée** |
| Mise à jour | Micrologiciel du Miniserver par Loxone Config ; Extensions mises à jour en arrière-plan par le Miniserver ; conséquence d'un échec non documentée |
| Sécurité | Jetons (HMAC-SHA1, échange de clé RSA-2048) sur l'API ; HTTPS ; authentification Basic encore disponible |
| API pour la passerelle | **WebSocket RFC 6455 et requêtes HTTP** documentées par Loxone ; structure dans `/data/LoxAPP3.json`, commandes `jdev/sps/io/{uuid}/{commande}`, états poussés ; Modbus TCP **en client seulement** (le Miniserver interroge, il n'expose rien) |
| MQTT | Pas natif ; passerelles communautaires LoxBerry (Raspberry Pi) et Lox2MQTT |
| Bibliothèques libres | PyLoxone pour Home Assistant (micrologiciel ≥ 2024.1), binding openHAB officiel, node-red-contrib-loxone. Bibliothèque Go : non vérifiée |
| Cloud | Aucun en exploitation ; Remote Connect et Cloud DNS optionnels, actifs d'usine sur un Miniserver neuf, refusés à la génération 1 ; tarif non trouvé |

Côté passerelle, le backend Go doit parler le WebSocket du Miniserver, avec son authentification par jeton. L'estimation est de **trois à six semaines-personne** pour l'intégration (estimation de cette étude, sans essai), plus une à deux semaines de programmation dans Loxone Config : ≈ 4 à 8 semaines avant la bascule. Le Miniserver fait tourner un système propriétaire dans l'armoire ; aucun code du projet n'y tourne.

## Nomenclature et coût estimé

Prix relevés le 24 octobre 2026 sur la boutique officielle, région « International (€) », affichés **hors TVA** et repris tels quels, sans conversion. La fiche et la largeur des alimentations n'ont pas été lues.

### Configuration minimale

| Poste | Référence | Qté | Prix unitaire HT | Total HT | Source |
| --- | --- | --- | --- | --- | --- |
| Contrôleur | Miniserver 100335 | 1 | 655,61 € | 656 € | shop.loxone.com |
| Entrées | DI Extension 100283 | 3 | 284,60 € | 854 € | shop.loxone.com |
| Éclairages, volets, divers | Relay Extension 100038 | 4 | 337,57 € | 1 350 € | shop.loxone.com |
| Variateurs | Dimmer Extension 100029 | 2 | 461,02 € | 922 € | shop.loxone.com |
| Alimentation | Power Supply 4,2 A 100617 | 1 | 69,00 € | 69 € | shop.loxone.com |
| Pontets | Shunting Wire 200300 et 200301 | 2 | 30,50 € | 61 € | shop.loxone.com |
| **Matériel** | | | | **3 912 € HT** | |
| Logiciel | Loxone Config | 1 | 0 € | 0 € | loxone.com |
| **Total** | | | | **≈ 3 900 € HT** | |

### Configuration résiliente

| Poste | Référence | Qté | Prix unitaire HT | Total HT |
| --- | --- | --- | --- | --- |
| Contrôleurs de zone | Miniserver Compact 100512 | 3 | 495,00 € | 1 485 € |
| Entrées | DI Extension 100283 | 5 | 284,60 € | 1 423 € |
| Éclairages, volets, divers | Relay Extension 100038 | 6 | 337,57 € | 2 025 € |
| Variateurs | Dimmer Extension 100029 | 3 | 461,02 € | 1 383 € |
| Alimentations | Power Supply 4,2 A 100617 | 3 | 69,00 € | 207 € |
| Pontets | Shunting Wire 200300 et 200301 | 6 | 30,50 € | 183 € |
| **Matériel** | | | | **6 706 € HT** |
| Logiciel | Loxone Config | 1 | 0 € | 0 € |
| **Total** | | | | **≈ 6 700 € HT** |

Soit ≈ 2 800 € HT de plus que la configuration minimale, pour passer de 6 à 0 défaillance unique touchant toute la maison. Le mode Client-Gateway n'a pas de coût de licence connu : Loxone Config étant gratuit, probablement aucun, à confirmer.

### Couche domotique en dérivation

| Poste | Référence | Qté | Total HT |
| --- | --- | --- | --- |
| Contrôleur | Miniserver 100335 | 1 | 656 € |
| Sorties vers les relais de couplage | Relay Extension 100038 | 6 | 2 025 € |
| Entrées de recopie | DI Extension 100283 | 4 | 1 138 € |
| Alimentation et pontets | Power Supply 4,2 A 100617, Shunting Wire × 2 | 3 | 130 € |
| **Matériel** | | | **3 949 € HT** |
| Logiciel | Loxone Config | 1 | 0 € |
| **Total** | | | **≈ 3 950 € HT**, ≈ 71 modules plus l'alimentation |

### Ce qui n'est pas dans les totaux

- **Fonctions à reporter** : alarme par le bloc « Alarm System » de Loxone Config, gratuit, mais sans centrale certifiée ; les détecteurs et la sirène se raccordent à des entrées et des relais. Écran : Touch Pure Display Tree ≈ 350 € HT ou Wall Display 10" ≈ 825 € HT, tous deux sur bus Tree, donc hors contrainte ; l'application mobile et web est incluse. Délestage : bloc « Load Manager » (12 charges, par priorité) gratuit, mais la mesure demande un Energy Meter Tree (≈ 149 à 169 € HT, bus Tree) ou un compteur Modbus TCP.
- **Fil pilote** : aucune offre Loxone ; relais externes.
- **Verrouillage des volets** : logiciel seulement ; un verrouillage câblé externe n'est pas chiffré.
- **Alimentation secourue** : Power Supply & Backup ≈ 625 € HT, encombrante.
- **Électricien** : de l'ordre de 4 à 6 jours (estimation sans devis, moins de câblage que la V2).
- **Logiciel** : ≈ 4 à 8 semaines-personne (Loxone Config et passerelle).
- **Place** : ≈ 1,3 m (minimale), ≈ 2 m (par zone), ≈ 1,3 m (dérivation, en plus de la couche filaire) ; alimentations non comptées.

## Ouverture et pérennité

- **Protocoles propriétaires** : Link et Tree n'ont qu'un fabricant. L'ouverture passe par l'API HTTP et WebSocket, documentée publiquement, par le client Modbus TCP, et par des Extensions KNX (≈ 574 € HT), DALI (≈ 554 € HT), RS-485 et Modbus.
- **Suivi des générations** : le Miniserver de 2010 reçoit toujours les mises à jour « jusqu'à nouvel ordre », et les Extensions Link marchent sur les deux générations ; mais Remote Connect lui est refusé, et l'Extension d'origine a été arrêtée après dix ans, remplacée par des cartes équivalentes. Date de fin de vente de la génération 1 : non confirmée.
- **Vente** : boutique réservée aux partenaires professionnels, prix publics hors TVA ; vente aux particuliers non confirmée ; marché de l'occasion actif (Miniserver génération 1 ≈ 199 €, Relay Extension ≈ 299 €, annonces non vérifiées).
- **Cloud** : position « Cloudfree » affichée ; services cloud optionnels (Remote Connect, Cloud DNS, Mailer).
- **Dépendance matérielle** : la carte microSD porte le système et le programme ; Loxone n'admet que ses propres cartes.
- **Communauté** : loxforum (indépendant, très actif), LoxBerry, PyLoxone, openHAB, Node-RED.

## Verdict

- **Seule** : Loxone remplace l'armoire sans toucher un fil, et un Miniserver par zone évite qu'une panne unique prive toute la maison. Mais c'est l'architecture d'aujourd'hui avec un calculateur par zone : aucune logique locale, aucune manette, un état des relais que le fabricant ne documente pas à la perte du Link, et six pannes uniques qui coupent 20 à 22 boutons. C'est une réponse à la question « sans recâblage », pas à l'exigence.
- **En dérivation** : un contrôleur gratuit en logiciel et bien outillé, qui facture ses entrées-sorties au prix d'une armoire : près de 4 000 € HT là où la Revolution Pi ou un serveur Modbus font la même chose pour 600 à 1 900 € HT, avec un système propriétaire et une carte microSD dans l'armoire.
- **À qui elle convient** : à qui veut une domotique riche, programmée en blocs, suivie par un intégrateur Loxone, et accepte un contrôleur unique par zone sans commande de secours.

## Sources

Toutes consultées le 24 octobre 2026.

1. [Fiche Miniserver 100335](https://loxone.com/wp-content/uploads/datasheets/Datasheet_Miniserver_100335.pdf) (14.02.2024) : entrées-sorties, Link 30 Extensions, Tree 50, LAN et Modbus TCP, 2,5 kV, 9 modules.
2. [Fiche Relay Extension 100038](https://www.loxone.com/wp-content/uploads/datasheets/Datasheet_RelayExtension.pdf?v=1) (08.07.2020) : 14 relais 16 A, 48 A au total, 0,7 à 3,8 W, 2,5 kV, -40 à 40 °C.
3. [Fiche DI Extension 100283](https://loxone.com/wp-content/uploads/datasheets/Datasheet_DIExtension_100283.pdf) (20.09.2024) : 20 entrées, seuils 7,1 et 9,7 V, 67 kΩ, 2 modules, UL 62368-1.
4. [Fiche Dimmer Extension 100029](https://www.loxone.com/wp-content/uploads/datasheets/Datasheet_DimmerExtension.pdf?v=1) (16.04.2020) : 4 sorties 400 et 210 W, 8 entrées, 2,5 kV.
5. [Fiche Miniserver Compact 100512](https://pim.loxone.com//01%20Product%20Data/01%20Products/Basics%20%26%20Accessories/100512%20-%20Miniserver%20Compact/Specifications/Datasheet_MiniserverCompact_100512.pdf) (01.03.2024) : 4 entrées, 2 relais 16 A, Link commutable en Tree.
6. [Documentation Link](https://www.loxone.com/enen/kb/link/) : 30 Extensions, chaîne stricte, 500 m, 120 Ω, 0 V commun, LED, mise à jour en arrière-plan.
7. [Documentation Relay Extension](https://www.loxone.com/enen/kb/relay-extension/) : 14 actionneurs 0/1, état en ligne, coupure thermique, surveillance ; aucune commande manuelle.
8. [Documentation Dimmer Extension](https://www.loxone.com/enen/kb/dimmer-extension/) : charges admises, LED, condensateurs d'antiparasitage ; aucune protection contre le court-circuit mentionnée.
9. [Documentation DI Extension](https://www.loxone.com/enen/kb/di-extension/) : poussoirs, S0, 0 V interconnectés.
10. [Diagnostic des appareils hors ligne](https://www.loxone.com/enen/kb/device-offline-diagnostics/) : délai selon le type d'appareil, Link en bus strict, Miniservers client et passerelle.
11. [Documentation Tree](https://www.loxone.com/enen/kb/tree-branch/) : 50 appareils et 500 m par branche, topologie libre.
12. [Loxone Config](https://www.loxone.com/enen/products/loxone-config/) : « Free forever », 150 blocs fonctions.
13. [Téléchargements](https://www.loxone.com/enen/support/downloads/) : Loxone Config 17.2.10.21, Windows 10 64 bits, double authentification.
14. [Liste de contrôle « Miniserver ne démarre pas »](https://www.loxone.com/enen/kb/miniserver-not-starting-checklist/) : démarrage jusqu'à une minute, boucle de redémarrage, cartes microSD Loxone uniquement.
15. [Miniserver génération 1](https://www.loxone.com/dede/kb/miniserver-gen-1/) : microSD avec système et programme, 30 Extensions.
16. [Power Supply & Backup](https://www.loxone.com/enen/kb/power-supply-backup/) : 7 sorties 24 V fusiblées, batterie 36 V, PELV, coffret de 100 l.
17. [Billet « Creating a reliable installation », partie 4](https://www.loxone.com/enen/blog/part-4-creating-a-reliable-installation-in-a-real-smart-home/) (22 mars 2018) : très basse tension, alimentations séparées, 0 V au PE, parafoudres recommandés.
18. [Remote Connect](https://www.loxone.com/enen/kb/remote-connect/) : enregistrement, Cloud DNS, génération 1 non compatible.
19. [Communicating with the Miniserver](https://www.loxone.com/enen/wp-content/uploads/sites/3/2016/10/1000_Communicating-with-the-Miniserver.pdf) : WebSocket RFC 6455, jetons, échange de clé.
20. [Documentation communautaire de l'API](https://github.com/mr-manuel/Loxone_api_documentation) et [node-red-contrib-loxone](https://github.com/codmpm/node-red-contrib-loxone) : `LoxAPP3.json`, commandes, états poussés.
21. [Modbus TCP](https://www.loxone.com/cscz/kb/komunikace-pres-modbus-tcp/) : le Miniserver en client Modbus TCP.
22. [LoxBerry MQTT Gateway](https://wiki.loxberry.de/plugins/mqtt_gateway/start), [PyLoxone](https://github.com/JoDehli/PyLoxone), [binding openHAB](https://v31.openhab.org/addons/bindings/loxone/) : passerelles et intégrations libres.
23. [Lighting Controller](https://www.loxone.com/enen/kb/lighting-controller/) et [Load Manager](https://www.loxone.com/enen/kb/load-manager/) : double et triple clic, appui long, ambiances, délestage par priorité.
24. [Le Miniserver a dix ans](https://www.loxone.com/enen/blog/the-loxone-miniserver-turns-10/), [FAQ génération 2](https://www.loxone.com/enen/the-next-generation-miniserver/) et [groupe Loxone](https://www.loxone.com/enen/about-us/loxone-group/) : 2009, 2010, 2020, mises à jour de la génération 1, effectifs.
25. [Arrêt de l'Extension](https://www.loxone.com/dede/blog/produktabkuendigung-extension/) (11 mai 2020) : fin de vente en juillet 2020, produits de remplacement.
26. [Devenir Partner](https://www.loxone.com/int/blog/top-reasons-loxone-partner/) : inscription avec licence professionnelle, accès à la boutique.
27. Prix, boutique officielle hors TVA : [Miniserver](https://shop.loxone.com/enen/product/100335-miniserver), [Relay Extension](https://shop.loxone.com/enen/product/100038-relay-extension), [DI Extension](https://shop.loxone.com/enen/product/100283-di-extension), [Dimmer Extension](https://shop.loxone.com/enen/product/100029-dimmer-extension), [Tree Extension](https://shop.loxone.com/enen/product/100218-tree-extension) ; Miniserver Compact, alimentations, pontets, écrans et compteurs d'après les pages de résultats de la même boutique.
28. Forum loxforum (allemand), fils consultés : [foudre, toutes les Extensions clignotent en jaune](https://www.loxforum.com/forum/hardware-zubeh%C3%B6r-sensorik/316290-blitzeinschlag-seit-dem-alle-extensions-blinken-gelb) (29.08.2021) ; [entrée numérique du Miniserver génération 2](https://www.loxforum.com/forum/hardware-zubehör-sensorik/355486-digital-eingang-am-miniserver-gen-2) ; [panne de Miniserver](https://www.loxforum.com/forum/hardware-zubehör-sensorik/351901-miniserver-ausfall) (lu par résumé) ; [fin de vente de la génération 1](https://www.loxforum.com/forum/hardware-zubehör-sensorik/327207-miniserver-gen-1-abkündigung) ; [plugin Lox2MQTT](https://loxforum.com/forum/projektforen/loxberry/plugins/389693-plugin-lox2mqtt).
29. [Forum KNX-User-Forum, « KNX ne marche plus »](https://knx-user-forum.de/forum/öffentlicher-bereich/knx-eib-forum/knx-einsteiger/881001-hilfe-knx-funktioniert-nicht-mehr) : avec Loxone, « quand le cœur central tombe, rien ne marche » (avis d'utilisateur).

!!! note "À confirmer auprès des fabricants"
    L'état des relais des Relay et Dimmer Extensions à la perte du Link ou du Miniserver ; la couche physique du Link et les tensions d'isolement entre Link, entrées et contacts 230 V ; le type d'entrée des DI Extension (optocouplée ou non), la longueur de ligne admise et l'immunité aux parasites ; le comportement après une mise à jour échouée ; la protection contre le court-circuit de la Dimmer Extension ; les limites et le coût éventuel du mode Client-Gateway ; la fiche et la largeur des alimentations 24 V ; les conditions de vente aux particuliers et le tarif de Remote Connect ; la date de fin de vente de la génération 1.
