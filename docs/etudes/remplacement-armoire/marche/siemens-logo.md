---
title: "Siemens LOGO! 8 : remplacer l'armoire sans recâblage"
description: "L'automate compact Siemens LOGO! 8 pour remplacer les quatre cartes de l'armoire ESSENSYS sans toucher aux fils : quatre ou cinq unités reliées en Ethernet pour 63 entrées et 80 à 100 sorties relais, variateurs externes. Seul, c'est un calculateur entre chaque bouton et sa charge, dont les relais retombent à l'arrêt ; en dérivation, c'est un serveur d'entrées-sorties Modbus TCP à relais, bon marché mais aux entrées non isolées. Environ 1 900 € HT par zone, 1 600 € HT en couche domotique."
---

# Siemens LOGO! 8

LOGO! est le module logique compact de Siemens, lancé en 1996 et très répandu en domotique de particulier : une unité de base à 8 entrées et 4 sorties relais, des modules d'extension, un programme en schéma à blocs. Ce dossier du [comparatif](index.md) regarde ce que donne un automate, et non un système domotique, face aux 63 poussoirs et aux charges de l'armoire : il faut plusieurs unités en réseau, il n'y a ni variateur ni bloc de volet natif, et les relais retombent dès que l'unité s'arrête.

!!! abstract "Synthèse"
    - **Seule** : le LOGO! reprend les 63 poussoirs et les charges sans recâblage, mais il n'existe pas de LOGO! à 80 sorties : il en faut quatre ou cinq unités reliées en Ethernet, plus huit variateurs externes. Chaque bouton passe par le programme d'une unité : **règle 1 non tenue**, sauf pour les huit variateurs si l'on retient des EUD12D-UC à entrée locale. Les relais sont monostables : en arrêt ou hors tension, « les contacts sont ouverts en permanence », et l'état revient par logiciel au redémarrage. En version 230 V, les nappes des poussoirs portent le secteur. En configuration par zone (cinq unités autonomes), **aucune des huit défaillances uniques ne prive toute la maison de ses boutons** ; deux privent une zone, les autres une unité. En configuration maître-esclaves, cinq privent toute la maison.
    - **En dérivation** : un serveur d'entrées-sorties à relais isolés, Modbus TCP ouvert, sans Linux et presque sans licence, dont les sorties s'ouvrent d'elles-mêmes à l'arrêt. Ses entrées ne sont pas isolées, ses relais ne sont pas faits pour battre toutes les 200 ms, et la version 24 V, seule compatible avec les îlots TBTS de la V2, n'a pas de prix trouvé.
    - **Coût estimé** : ≈ 1 600 € HT en configuration minimale, ≈ 1 900 € HT par zone, variateurs et licence compris ; ≈ 1 600 € HT en couche domotique seule, version 230 V. Prix d'octobre 2026, vendeurs eBay et boutiques allemandes, TTC à 19 %, convertis en HT ; les distributeurs officiels n'affichent pas leurs prix.
    - **Réserve** : estimations à confirmer par un électricien, des devis, le fabricant et des essais. Le commutateur Ethernet, les modules 24 V et les sorties analogiques n'ont pas de prix trouvé.

## Principe et gamme

Le LOGO! est un **micro-automate** : une unité de base (BM) à 8 entrées et 4 sorties relais 10 A, extensible par des modules DM8 (4 entrées, 4 sorties) et DM16 (8 entrées, 8 sorties relais 5 A) emboîtés sur le côté, jusqu'à 24 entrées et 20 sorties par unité. La logique s'exécute dans l'unité de base, programmée en blocs fonction dans **LOGO! Soft Comfort** ou, pour les cas simples, sur l'afficheur. Il n'y a ni bus de terrain, ni actionneur de volet, ni variateur : les sorties sont des relais ou des transistors.

Plusieurs unités se relient en **Ethernet** : en maître-esclaves, où l'esclave n'est qu'une extension réseau sans programme, ou en client-serveur, où chaque unité exécute son programme et échange par des entrées-sorties réseau (S7 ou Modbus TCP). Une unité tient 16 connexions S7 ou Modbus, dont 8 statiques.

Les générations : LOGO! 8 (0BA8) en 2014, 8.1 avec Modbus TCP, 8.3 avec le cloud, **8.4** fin 2023 avec MQTT vers tout broker. **LOGO! 9** a été annoncé en mars 2026 et livré en avril : 64 entrées et 60 sorties par unité, Soft Comfort V9 sous Windows, macOS et Linux, Secure Boot. Le LOGO! 8 reste « produit actif » au 24 octobre 2026, sans date d'arrêt publiée ; ce dossier chiffre le LOGO! 8, seul à prix connus. Références en 230 V (230RCE, DM 230R) ou en 12/24 V continu (12/24RCE, DM 24R) ; les deux classes de tension ne se mélangent pas sur une même unité.

## Dans l'armoire sans recâblage

Les poussoirs sont des contacts secs : les **entrées tout-ou-rien** des unités les lisent ; les **relais** commandent les charges ; l'Ethernet reste dans l'armoire.

| Fonction | Module | Voies | Largeur | Ce qu'il faut savoir |
| --- | --- | --- | --- | --- |
| 63 poussoirs | LOGO! 230RCE et DM16 230R | 8 entrées par module, 24 par unité | 4 modules chacun | Entrées **non isolées**, référencées à l'alimentation ; état 1 au-dessus de 79 V, état 0 sous 40 V, retard 30 à 75 ms, 4 Hz, 100 m non blindé ; le commun des poussoirs est la phase, et tous les modules doivent être sur **la même phase** que l'unité ; les nappes portent 230 V |
| | LOGO! 12/24RCE et DM16 24R | 8 entrées 12/24 V continu | 4 modules chacun | Non isolées non plus ; alimentation LOGO! Power 24 V ; les boucles restent en TBT. Version compatible avec les volumes des salles d'eau, **sans prix trouvé en euros** pour le DM16 24R |
| 25 éclairages | Relais de l'unité (4 × 10 A) et des DM16 (8 × 5 A) | 20 sorties par unité | | Relais **monostables**, contacts NO seuls, un contact par bornes (« groupes de 1 »), isolés ; incandescence 1 000 W, charge LED **non chiffrée** ; charge minimale recommandée 100 mA ; protection B16 externe ; « en STOP, les contacts sont ouverts en permanence » |
| 15 volets dont le store | Deux relais par moteur | 30 sorties | | **Aucun bloc volet ni verrouillage matériel** : l'interverrouillage des deux sens et le temps de course se programment ; l'exemple Siemens « Set 9 » le fait |
| 8 variateurs | Aucun variateur natif. Soit AM2 AQ (2 sorties 0–10 V, 10 bits) vers des variateurs 0–10 V, soit **Eltako EUD12D-UC** (Series 12, entrée de commande 8 à 230 V isolée, 400 W) piloté par un relais, le poussoir en parallèle | | 2 modules (AM2 AQ) ou 1 module (EUD12D) | La seconde voie est celle de la V2 : le poussoir garde la main sans LOGO! |
| Fil pilote | Relais et diodes externes | | | Non documenté par Siemens |
| Cumulus, prises, arrosage, machines | Relais 10 A ou 5 A, contacteur pour le cumulus | ≈ 8 à 10 sorties | | Contacts secs |
| Réseau | LOGO! CSM230 ou commutateur du commerce | 4 ports | | Nécessaire au-delà de deux unités ; prix non trouvé |
| Afficheur | LOGO! TDE | | | Déporté, Ethernet ; prix non trouvé |
| Passerelle KNX | LOGO! CMK2000 | | | ≈ 304 € HT, « non disponible » chez le revendeur consulté ; non retenue |

### Configuration minimale

Il n'existe pas de LOGO! à 85 sorties : la configuration minimale est déjà un réseau. **Quatre unités** « 230RCE + 2 DM16 230R », soit 96 entrées et 80 sorties relais, en **maître-esclaves** : une unité porte le programme et lit les entrées des trois autres par Ethernet ; un commutateur ; huit EUD12D-UC pour les variateurs. 230 V sur les nappes de poussoirs. **≈ 60 modules, soit ≈ 1,1 m de rail** (12 modules par unité, 8 pour les variateurs, 4 pour le commutateur).

### Configuration résiliente

**Une ou deux unités autonomes par zone**, chacune avec son programme, reliées en Ethernet seulement pour les commandes centrales et la passerelle. Les besoins en sorties par zone (éclairages, deux relais par volet, variateurs) dépassent les 20 d'une unité pour deux zones sur trois :

| Zone | Sorties nécessaires | Unités | Entrées disponibles |
| --- | --- | --- | --- |
| Pièces de vie (20 poussoirs, 5 éclairages, 6 volets, 3 variateurs) | 20 | 1 | 24 |
| Chambres (21, 7, 5, 4) | 21 | 2 | 48 |
| Pièces d'eau (22, 13, 4 dont le store, 1) | 22 | 2 | 48 |

Le fil pilote, le cumulus, les prises, l'arrosage et les machines prennent les sorties restantes des unités doubles. **Cinq unités**, 120 entrées et 100 sorties, cinq adresses IP, cinq serveurs Modbus TCP. **≈ 72 modules, soit ≈ 1,3 m de rail**, variateurs et commutateur compris. En version 230 V, chaque unité est alimentée par le disjoncteur de sa zone ; en version 24 V, une LOGO! Power par zone.

## Seule face à l'exigence

### Les sept règles

| Règle | Tenue | Pourquoi |
| --- | --- | --- |
| 1. Pas de calculateur entre le bouton et sa charge | **Non tenue** | Le poussoir est lu par le programme de l'unité, qui commande le relais ; en STOP, les entrées ne sont plus lues et les relais sont ouverts. Aucun mode manuel ni liaison entrée → sortie câblée ; un esclave n'a aucune logique propre. Exception : les 8 variateurs EUD12D-UC à entrée locale, dont le poussoir reste câblé en parallèle |
| 2. L'état vit dans un organe bistable | Non tenue | Relais monostables : toute coupure ou tout arrêt éteint tout. Au redémarrage, l'unité reprend en RUN en ≈ 1,6 s et réapplique les valeurs des blocs déclarés rémanents : l'état vit dans le logiciel |
| 3. La domotique ajoute, ne retire jamais | Non tenue | L'automate **est** la domotique : une erreur de programme ou une écriture Modbus par le réseau commute n'importe quelle sortie ; Siemens avertit que les ports 102 et 502 à 510 non sécurisés permettent des changements de mode et des écritures |
| 4. Une source et un fusible par zone, un fusible pour la domotique | Partielle | Une ou deux unités par zone, chacune sous son disjoncteur ou sa LOGO! Power ; mais boutons et logique partagent la même alimentation, sans fusible qui sépare les deux ; en 230 V, le commun des poussoirs est la phase |
| 5. Barrière 4 kV et 8 mm, 0 V jamais au PE, parafoudres hors coffrets | Non tenue en 230 V, partielle en 24 V | Entrées **non isolées** ; relais isolés, catégorie de surtension III ; tenue aux chocs 1 kV entre lignes et 2 kV ligne-terre (230 V), 0,5 et 1 kV pour les modules 24 V sans parafoudre ; rigidité « IEC 61131-2 satisfaite » **sans valeur en kV**. En 230 V, les boucles de poussoirs portent le secteur dans toute la maison, jusqu'aux salles d'eau : hors des îlots TBTS de la V2 |
| 6. Replis choisis au câblage, essayés à la recette | Partielle | Le repli est fixé par construction : relais ouverts ; la rémanence se règle bloc par bloc dans le programme ; le verrouillage des volets est logiciel, un relais soudé n'est pas rattrapé |
| 7. Isolement mesuré chaque année | Tenue | Rien ne l'empêche |

### Les causes communes

Dans la configuration résiliente, la liste fermée du comparatif donne :

| Défaillance unique | Prive de ses boutons… | Pourquoi |
| --- | --- | --- |
| 1. Alimentation du système | une zone | Les unités d'une zone sont sous le disjoncteur ou la LOGO! Power de la zone ; leurs relais s'ouvrent, leurs boutons se taisent |
| 2. Court-circuit ou ligne collée | un module | Pas de bus : une liaison Ethernet coupée ne touche que les commandes centrales et l'application ; un module d'extension qui ne communique plus passe en STOP et prive ses 8 sorties ; une entrée collée est lue à 1 en permanence, sans diagnostic |
| 3. Contrôleur central | un module | Aucun : chaque unité porte son programme ; une unité morte prive ses 20 à 24 boutons, soit une demi-zone au plus |
| 4. Logiciel figé | un module | Un utilisateur rapporte des passages spontanés en STOP ; **aucun chien de garde matériel documenté** ; l'unité touchée seule |
| 5. Mise à jour ratée | un module | Le firmware se charge unité par unité par Soft Comfort ; procédure de récupération non trouvée |
| 6. Licence, compte ou cloud | rien | Soft Comfort ne sert qu'à programmer ; le cloud est optionnel |
| 7. Commutateur ou routeur | rien | Hors du chemin du bouton, qui reste dans son unité |
| 8. Foudre sur le chemin du bus | une zone | Pas de bus ; l'onde entre par les boucles de poussoirs, à 230 V dans toute la maison en version 230 V, dans des entrées non isolées référencées à l'alimentation de l'unité ; tenue annoncée 2 kV ligne-terre |

**Total : 0 défaillance unique prive toute la maison**, 2 privent une zone, 4 privent une unité. En configuration minimale maître-esclaves, les esclaves n'ont aucune logique : l'alimentation du maître, le maître, son logiciel figé, sa mise à jour ratée et le commutateur par lequel passent les boutons des esclaves privent toute la maison : **5** ; une liaison Ethernet coupée prive les trois esclaves.

Le passage de 5 à 0 ne coûte qu'une unité de plus. Il tient à une décision de programmation, pas de matériel : cinq programmes au lieu d'un.

### Ce qui reste, panne par panne

| Panne | Ce qui reste |
| --- | --- |
| Unité d'une zone hors tension ou en STOP | Les autres unités. Dans l'unité touchée : **lumières éteintes**, volets arrêtés, aucun bouton ; variateurs EUD12D-UC au bouton. Au retour, RUN en ≈ 1,6 s, blocs rémanents réappliqués, horloge sauvegardée 20 jours |
| Maître en configuration minimale | Les 24 entrées et 20 sorties du maître ; les esclaves ne lisent plus rien ; l'état de leurs relais à la perte de liaison n'est **pas documenté** |
| Réseau ou commutateur | En résiliente : le local de chaque unité ; perdues : les commandes centrales et l'application |
| Passerelle Essensys | Tout le local ; perdue : l'application |
| Coupure du secteur | Tout retombe ; au retour, le programme réapplique les états rémanents : des lumières se rallument par logiciel |
| Un relais soudé | Les autres voies ; pour un volet, le programme ne peut pas ouvrir un contact collé : **les deux sens peuvent être alimentés ensemble**, faute de verrouillage câblé |
| Coupure pendant la programmation | « Le programme est absent au retour de la tension » ; recharger depuis Soft Comfort ou la carte |
| Foudre par une ligne de poussoirs | L'unité touchée au moins, par ses entrées non isolées ; les autres unités |

Les utilisateurs de Home Assistant notent que les relais LOGO! n'ont que deux contacts (C et NO), sans commande manuelle, et montent des relais séparés pour que l'éclairage survive aux contrôleurs.

## En dérivation sur le filaire V2

Dans cette lecture, les télérupteurs, les chaînes de volets et les variateurs à entrée locale gardent le chemin du bouton. Le LOGO! fournit la couche domotique :

- **Sorties** : cinq unités « 230RCE + 2 DM16 230R » donnent 100 relais isolés, en groupes de 1, qui commandent les bobines 24 V des relais de couplage 38.51 de la V2. La charge minimale recommandée de 100 mA est à comparer au courant d'une bobine de 38.51.
- **Entrées** : 120 entrées pour les 70 contacts de recopie. En version 230 V, le contact sec du relais de recopie ferme la phase de l'unité sur l'entrée : la barrière de 6 kV du 38.51 sépare le circuit filaire de l'automate, mais l'entrée elle-même n'est pas isolée de l'alimentation. En version 24 V, les boucles de recopie restent en TBT ; cette version n'a pas de prix trouvé.
- **Logique** : deux partages possibles. Soit la passerelle écrit les sorties par Modbus TCP et le LOGO! n'est qu'un serveur d'entrées-sorties : les utilisateurs de Home Assistant notent qu'une sortie écrite par le réseau ne peut pas aussi être pilotée par le programme. Soit les cinq programmes portent les horaires et les scènes et la passerelle les lit.
- **Battement de cœur** : si la passerelle porte la logique, c'est elle qui réarme le chien de garde matériel de la V2. Si le LOGO! la porte, son bloc « générateur d'impulsions asynchrone » peut réarmer le relais de garde, mais une sortie relais n'est pas faite pour battre toutes les 200 ms (10 Hz mécaniques au plus, 0,5 Hz en charge inductive) : il faudrait une sortie transistor, en version 24 V. Si le réarmeur se tait, le relais de garde retombe en moins d'une seconde ; si l'unité s'arrête ou perd sa tension, ses relais s'ouvrent d'eux-mêmes : la couche se retire. Un relais soudé ou un programme figé sorties tenues sont les cas que le chien de garde et le câblage de la V2 couvrent.
- **Interface** : la passerelle, par Modbus TCP ; la table d'adresses n'est pas dans le manuel système et deux sources en donnent des bases différentes.

Ce que la couche apporte : ≈ 1 600 € HT pour 100 relais et 120 entrées, un protocole ouvert, aucun Linux dans l'armoire, une licence à ≈ 50 € HT, un automate dont les sorties s'ouvrent à l'arrêt, un fabricant qui vend depuis trente ans. Ce qu'elle coûte : ≈ 60 modules (≈ 1,1 m de rail, à ajouter aux 1,6 à 2,1 m de la couche filaire), des entrées non isolées, un commutateur Ethernet, cinq adresses IP et une scrutation Modbus d'une seconde environ. Face à la Revolution Pi Connect 5 (≈ 581 € HT nue, plus ses modules d'entrées-sorties), le LOGO! est du même ordre de prix pour plus de voies, sans Linux à maintenir, mais sans entrées isolées. Face à KNX (≈ 3 100 € HT), il coûte moitié moins. Face au serveur d'entrées-sorties léger ([dossier Modbus](modbus-es.md)), il est dans la même gamme de prix, avec ses relais intégrés et un programme local possible.

## Foudre et isolement

- **Pas de bus** : seules les boucles de poussoirs et l'Ethernet entre unités sortent du rail. En version 230 V, les 63 boucles portent le secteur dans toute la maison ; en version 24 V, du 24 V continu.
- **Isolement** : entrées « sans isolement électrique » sur toutes les unités et modules relais, 230 V comme 24 V ; sorties relais isolées, groupes de 1 ; modules analogiques et de communication isolés sur leur connecteur latéral. Rigidité diélectrique « IEC 61131-2 satisfaite », distances d'isolement UL 61010 satisfaites, **aucune valeur en kV**. La barrière de 4 kV et 8 mm de la V2 ne peut pas être tenue par les entrées : elle revient aux relais 38.51 de recopie, en amont.
- **Chocs** : 1 kV entre lignes et 2 kV ligne-terre pour le 230RCE et les DM 230R ; 0,5 et 1 kV pour les modules 24 V, 1 et 2 kV avec un parafoudre tel que le BVT AD 24. Salves 2 kV sur l'alimentation ; catégorie de surtension III pour les unités et modules relais.
- **Recommandations Siemens** : câbles en paires, séparation des circuits alternatifs, à haute fréquence et à basse tension, parafoudre « tel que DCO RK E 24 » sur les câbles exposés.
- **Retours de terrain** : aucun cas de LOGO! détruit par la foudre en domotique n'a été trouvé.

## Logiciel, paramétrage et passerelle Essensys

| Point | Ce qu'on a trouvé |
| --- | --- |
| Outil | **LOGO! Soft Comfort V8.4** (Windows 11, macOS 12.1, Java), licence mono-poste ≈ 46 à 59 € HT selon le vendeur eBay, prix masqué chez Siemens ; indispensable pour le réseau et le Modbus ; programmation sur l'afficheur possible pour une unité isolée. V9 pour LOGO! 9, aussi sous Linux |
| Outils gratuits | Access Tool (traces), Web Editor V1.2 (pages web), Integrity Tool, serveur web intégré avec « module virtuel » |
| Formation | « Personnel qualifié » pour l'installation ; exemple Siemens « Set 9 » d'une maison en maître-esclave avec volets, tout éteindre et fonction panique ; livres grand public |
| Mise à jour | Firmware par Soft Comfort via Ethernet, ports non sécurisés ouverts ; récupération après échec non trouvée |
| Sécurité | Ports 102 (S7), 135 (TDE), 502 à 510 (Modbus) : Siemens recommande de ne les ouvrir que derrière un pare-feu ; le mode esclave ouvre 102 et 502 à 510 ; S7 et Modbus désactivés par défaut depuis la V8.3 ; HTTPS recommandé avec certificat racine LOGO! |
| API pour la passerelle | **Modbus TCP** serveur et client (16 connexions partagées avec S7, 8 statiques), **S7**, **MQTT** vers tout broker (8.4, TLS), HTTP/HTTPS. Table Modbus non publiée dans le manuel : base 0 selon un blog, 8192 + n selon des utilisateurs, « retrancher 1 aux adresses affichées » ; à vérifier dans l'aide de Soft Comfort |
| Bibliothèques libres | Home Assistant : intégration `modbus` du cœur, unité en RUN obligatoire, scrutation ≈ 1 s ; Node-RED `node-red-contrib-s7`, python-snap7 ; openHAB Modbus générique. Pas d'intégration LOGO! dédiée |
| Cloud | Optionnel (AWS, Azure, Alibaba, broker MQTT) ; sur la 8.3, le cloud activé coupe l'Access Tool et le navigateur |

Côté passerelle, le backend Go parle Modbus TCP, protocole ouvert sans bibliothèque propriétaire, ou MQTT. L'estimation de cette étude est de **deux à quatre semaines-personne** pour l'intégration, plus une à trois semaines pour les cinq programmes LOGO! : ≈ 3 à 7 semaines avant la bascule, contre 11 à 28 pour les V1.

## Nomenclature et coût estimé

Prix relevés le 24 octobre 2026, TTC à 19 %, convertis ici en HT. Siemens Industry Mall, Automation24, Conrad et RS n'affichent pas leurs prix sans compte ou refusent la lecture automatique : les prix viennent de **fiches produit eBay (neuf)**, d'osd-schenck, d'elektromax24 et de zaehlerschrank24. Un revendeur allemand affiche le DM16 230R à 144,81 € TTC, soit ≈ 27 % de plus que l'offre eBay retenue.

### Configuration minimale

| Poste | Référence | Qté | Prix unitaire HT | Total HT | Source |
| --- | --- | --- | --- | --- | --- |
| Unités de base | LOGO! 230RCE 6ED1052-1FB08-0BA2 | 4 | 113,90 € (135,54 € TTC) | 456 € | eBay.de, neuf |
| Extensions | LOGO! DM16 230R 6ED1055-1FB10-0BA2 | 8 | 95,99 € (114,23 € TTC) | 768 € | eBay.de, neuf |
| Variateurs | Eltako EUD12D-UC | 8 | 43,45 € (51,70 € TTC) | 348 € | zaehlerschrank24 |
| Commutateur Ethernet | LOGO! CSM230 ou du commerce | 1 | non trouvé | — | — |
| **Matériel** | | | | **≈ 1 570 € HT** | |
| Logiciel | LOGO! Soft Comfort V8.4 | 1 | 46,18 € (54,95 € TTC) | 46 € | eBay.de |
| **Total** | | | | **≈ 1 620 € HT** | |

Variante 0–10 V : quatre AM2 AQ (prix non trouvé) et huit variateurs 0–10 V (non chiffrés) à la place des EUD12D-UC.

### Configuration résiliente

| Poste | Référence | Qté | Prix unitaire HT | Total HT |
| --- | --- | --- | --- | --- |
| Unités de base | LOGO! 230RCE | 5 | 113,90 € | 570 € |
| Extensions | LOGO! DM16 230R | 10 | 95,99 € | 960 € |
| Variateurs | Eltako EUD12D-UC | 8 | 43,45 € | 348 € |
| Commutateur Ethernet | LOGO! CSM230 ou du commerce | 1 | non trouvé | — |
| **Matériel** | | | | **≈ 1 880 € HT** |
| Logiciel | LOGO! Soft Comfort V8.4 | 1 | 46,18 € | 46 € |
| **Total** | | | | **≈ 1 925 € HT** |

Soit ≈ 300 € HT de plus que la configuration minimale, pour passer de 5 à 0 défaillance unique touchant toute la maison. La version 24 V, seule compatible avec les îlots TBTS de la V2, remplace les 230RCE par des 12/24RCE (≈ 125 € HT, 148,76 € TTC) et les DM16 230R par des DM16 24R, sans prix trouvé en euros, plus une LOGO! Power 24 V par zone (≈ 27 € HT, 31,85 € TTC) : **non chiffrable** avec les prix relevés.

### Couche domotique en dérivation

| Poste | Référence | Qté | Total HT |
| --- | --- | --- | --- |
| Unités de base | LOGO! 230RCE | 5 | 570 € |
| Extensions | LOGO! DM16 230R | 10 | 960 € |
| Commutateur Ethernet | LOGO! CSM230 ou du commerce | 1 | non trouvé |
| **Matériel** | | | **≈ 1 530 € HT** |
| Logiciel | LOGO! Soft Comfort V8.4 | 1 | 46 € |
| **Total** | | | **≈ 1 575 € HT**, ≈ 60 modules, 100 relais et 120 entrées |

### Ce qui n'est pas dans les totaux

- **Fonctions à reporter** : pas de centrale d'alarme ; messages texte, e-mail (8.4) et MQTT. Écran : afficheur six lignes sur chaque unité, TDE déporté (prix non trouvé), serveur web. Délestage : aucun bloc dédié ; logique à programmer avec un AM2 ou des compteurs Modbus. Mesure d'énergie : aucune intégrée.
- **Fil pilote** : relais et diodes externes, non documentés par Siemens.
- **Commutateur Ethernet**, rail, bornes, LOGO! Power et modules 24 V : non chiffrés.
- **Électricien** : de l'ordre de 4 à 6 jours (estimation sans devis ; en 230 V, le câblage des entrées et la mise sur une même phase demandent du soin).
- **Logiciel** : ≈ 3 à 7 semaines-personne (estimation de cette étude).
- **Place** : ≈ 1,1 m (minimale), ≈ 1,3 m (par zone), ≈ 1,1 m (dérivation, en plus de la couche filaire).

## Ouverture et pérennité

- **Protocoles ouverts** côté réseau : Modbus TCP, MQTT, HTTP ; S7 propriétaire mais porté par de nombreuses bibliothèques. **Programmation propriétaire** : Soft Comfort sous licence payante, extensions Siemens uniquement, compatibles seulement au sein de la série 0BA8.
- **Ancienneté** : 1996 ; LOGO! 8 depuis 2014 ; 8.4 fin 2023 ; **LOGO! 9 depuis avril 2026**. Le LOGO! 8 est donc la génération précédente, encore « produit actif », sans date d'arrêt publiée. Précédent : les 0BA6 ont été arrêtés le 30 septembre 2021, sept ans après leur successeur, et leurs modules d'extension n'étaient pas compatibles avec la génération suivante. La compatibilité des modules 0BA2 avec LOGO! 9 n'est pas documentée dans les sources consultées ; Soft Comfort V9 reprend les projets des générations antérieures.
- **Vente libre** chez les distributeurs d'automatisme et sur les places de marché, prix masqués chez Siemens sans compte.
- **Cloud** : optionnel, fonctionnement local ; sécurité de type industriel (ports, HTTPS, pare-feu).
- **Communauté** : forum Siemens Industry Online Support, forums Home Assistant et allemands, exemples d'application Siemens, livres grand public ; aucun retour chiffré de fiabilité pluriannuelle en habitat trouvé.

## Verdict

- **Seule** : le LOGO! remplace l'armoire sans toucher un fil pour ≈ 1 900 € HT, le prix le plus bas de ce comparatif, et, découpé en cinq unités autonomes, ne laisse aucune défaillance unique priver toute la maison. Mais c'est un automate : chaque bouton passe par un programme, les relais s'ouvrent dès que l'unité s'arrête et l'état revient par logiciel ; il n'a ni variateur ni volet natif, et sa version 230 V met le secteur sur les nappes de poussoirs. C'est la reprise des défauts des études V1, en moins cher et en plus robuste industriellement, pas une réponse à l'exigence.
- **En dérivation** : un serveur d'entrées-sorties à relais, ouvert par Modbus TCP, sans Linux, dont les sorties s'ouvrent d'elles-mêmes à l'arrêt ; au prix du serveur léger, avec moins d'isolement sur les entrées, plus de rail et une génération derrière LOGO! 9.
- **À qui elle convient** : à qui sait programmer un automate, veut des relais isolés et un protocole ouvert dans un boîtier de marque, et accepte des entrées non isolées protégées par les relais de recopie, ou attend le prix de la version 24 V.

## Sources

Toutes consultées le 24 octobre 2026.

1. [Siemens, LOGO! System Manual, 06/2023](https://cache.industry.siemens.com/dl/files/499/109826499/att_1161914/v1/logo_system_manual_en-US_en-US.pdf) : limites 24 entrées et 20 sorties, compatibilité des modules, maître-esclaves, 16 connexions, STOP et relais ouverts, rémanence, redémarrage, CEM et catégories de surtension, isolement, sécurité des ports, même phase, parafoudre.
2. [Siemens, Product Information LOGO! 05/2024](https://docs.rs-online.com/b8b3/A700000014360789.pdf) : numéros de commande 0BA2.
3. [Drives & Controls, histoire du LOGO!](https://m.drivesncontrols.com/news/fullstory.php/aid/4309/.html) et [reichelt, LOGO! 8.4](https://www.reichelt.com/magazin/en/?p=95451) : 1996, compatibilité 8.3 et 8.4, nouveautés 8.4.
4. [computer-automation.de, Hannover Messe 2014](https://www.computer-automation.de/bilder/5/neues-von-siemens-auf-der-hannover-messe-2014.htm) : LOGO! 8 remplace les séries 6 et 7.
5. [Forum Siemens, numérotation et fin des 0BA6](https://support.industry.siemens.com/forum/ww/en/posts/logo-product-numbering/228685) : arrêt au 30 septembre 2021.
6. [DigiKey, LOGO! 8.4](https://www.digikey.com/en/product-highlight/s/siemens/logo-8-3-logic-modules) : cloud, MQTT, e-mail, outils gratuits.
7. [devicebase, nouveautés LOGO! 8.4](https://devicebase.net/en/siemens-logo/updates/new-enhancements/4pf) et [forum Siemens, mise en vente 8.4](https://support.industry.siemens.com/forum/WW/en/posts/sales-release-for-logo-8-4-basic-devices/309682) : décembre 2023.
8. [IT Brief, Siemens dévoile LOGO! 9](https://itbrief.com.au/story/siemens-unveils-logo-9-compact-controller-upgrade) et [communiqué Siemens](https://news.siemens.com/es-es/introducing-the-new-generation-of-logic-controllers/) : mars 2026, 64 entrées et 60 sorties, Soft Comfort V9, compatibilité des projets.
9. [Siemens Industry Mall, 230RCE](https://mall.industry.siemens.com/mall/en/WW/Catalog/Product/6ED1052-1FB08-0BA2) et [CMK2000](https://mall.industry.siemens.com/mall/en/WW/Catalog/Product/6BK1700-0BA20-0AA0) : « produit actif », prix masqués ; [smartkram, CMK2000](https://smartkram.de/en/?p=278150).
10. [Fiche distributeur DM16 230R](https://www.onninen.fi/en/siemens-expansionmodul-logo-dm16-230r-0ba8/p/GCR521) et [fiche RS 230RCE](https://docs.rs-online.com/38c2/A700000015110570.pdf) : relais 5 A, protection externe.
11. [Siemens, « Haussteuerung mit Master-Slave – LOGO! Set 9 »](https://asset.conrad.com/media10/add/160267/c1/-/de/64143308_LOGO8_Set9_Master_Slave_DOKU_v22_de_(2)) : maison en maître-esclave, volets, tout éteindre, panique.
12. [dacpol, AM2 AQ](https://www.dacpol.eu/en/drivers-422/product/logo-8-am2-aq-extension-module-power-supply-24v-dc-2-analog-outputs-04-20ma-or-0-10v), [mikrocontroller.net, LED 1–10 V](https://www.mikrocontroller.net/topic/481052), [BricoZone, variateur et LOGO!](https://www.bricozone.be/t/siemens-logo-8-dimmer-avec-un-bouton-poussoir.109846/) : variation par 0–10 V.
13. [Eltako, fiche EUD12D-UC](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_EUD12D-UC.pdf) et [zaehlerschrank24, EUD12D-UC](https://www.zaehlerschrank24.de/multi-dimmschalter-eud12d-uc.html) : entrées isolées, 400 W, 51,70 € TTC.
14. [Forum Siemens, LOGO! en STOP spontané](https://support.industry.siemens.com/forum/tw/en/post/1233301) : retour d'utilisateur.
15. [Home Assistant Community, « Siemens logo 8 »](https://community.home-assistant.io/t/siemens-logo-8/129281) : Modbus TCP, adresses 8192, RUN obligatoire, latence, relais sans commande manuelle.
16. [industrialmonitordirect, table Modbus TCP](https://industrialmonitordirect.com/blogs/knowledgebase/configuring-logo-8-modbus-tcpip-server-discrete-io-mapping), [sorties NC](https://industrialmonitordirect.com/blogs/knowledgebase/logo-8-nc-output-workarounds-for-safety-circuit-design), [maître-esclave et client-serveur](https://industrialmonitordirect.com/blogs/knowledgebase/logo-masterslave-vs-clientserver-s7-communication) : sources tierces.
17. [forum heimnetz.de, position de volet](https://forum.heimnetz.de/threads/position-rollo-mit-externen-opening-closing-signal.8463/) et [LOGO! et Home Assistant](https://forum.heimnetz.de/threads/siemens-logo-an-ha-anbinden.601/) : volets, adresses Modbus.
18. [Extrait du livre « Steuern und Regeln für Heim und Industrie mit LOGO! 8 »](https://blafusel.de/book_stuff/steuern_und_regeln_fuer_heim_und_industrie_mit_lgo_8_isbn_9783754348796_leseprobe.pdf).
19. Prix : [eBay.de, 230RCE](https://www.ebay.de/p/8014451492), [eBay.de, 12/24RCE](https://www.ebay.de/p/10066549381), [eBay.de, DM16 230R](https://www.ebay.de/p/2254347573), [osd-schenck, DM16 230R](https://shop.osd-schenck.de/6ED1055-1FB10-0BA2), [elektromax24, DM8 230R](https://www.elektromax24.de/siemens-logo-8-erweiterungsmodul-6ed1055-1fb00-0ba2-dm8-230r), [osd-schenck, DM8 230R](https://shop.osd-schenck.de/6ED1055-1FB00-0BA2), [alltron, DM16 24R](https://alltron.ch/de/product/828368), [sparepartsnow, DM16 24](https://www.sparepartsnow.de/produkte/siemens-6ed1055-1cb10-0ba2-cbfpb8), [eBay.de, Soft Comfort V8.4](https://www.ebay.de/itm/165688430098), [eBay.de, LOGO! Power](https://www.ebay.de/itm/205388487551).

!!! note "À confirmer auprès des fabricants"
    L'état des relais d'un esclave à la perte du maître ou du réseau ; l'existence d'un chien de garde matériel et la cause des passages spontanés en STOP ; la procédure de récupération après une mise à jour de firmware échouée ; la table d'adresses Modbus TCP officielle ; la tension d'essai en kV entre entrées, relais et alimentation ; la charge LED admissible et la durée de vie des relais à cadence rapide ; la date d'arrêt du LOGO! 8 et la compatibilité des modules 0BA2 avec LOGO! 9 ; les prix des distributeurs officiels pour le 230RCE, le DM16 230R, le DM16 24R, l'AM2 AQ, le TDE et Soft Comfort ; la consommation 24 V des 12/24RCE et DM16 24R ; une solution de fil pilote.
