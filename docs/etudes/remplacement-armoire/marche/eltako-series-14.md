---
title: "Eltako Series 14 : remplacer l'armoire sans recâblage"
description: "Le bus RS-485 Eltako Series 14 pour remplacer les quatre cartes de l'armoire ESSENSYS sans toucher aux fils : modules FTS14EM pour les 63 poussoirs, actionneurs FSR14, FSB14 et FUD14 alimentés par le bus. Seule, elle met le bus entre le bouton et sa charge et éteint les lumières d'une zone à la perte de son 12 V ; en dérivation, c'est la couche la plus compacte et la moins chère des bus, mais propriétaire. Environ 2 100 € HT par zone, 1 600 € HT en couche domotique."
---

# Eltako Series 14

Eltako fabrique les variateurs EUD12D-UC que la V2 retient. Sa Series 14 est autre chose : des appareils modulaires sur un bus RS-485 propriétaire, alimentés par le bus, conçus pour regrouper dans l'armoire les actionneurs de sa radio de bâtiment EnOcean. Ce dossier du [comparatif](index.md) regarde ce que donne ce bus quand il reçoit les 63 poussoirs classiques, et le compare à la Series 12 à entrée locale de la V2 : la Series 12 est le filaire, la Series 14 est le bus.

!!! abstract "Synthèse"
    - **Seule** : la Series 14 remplace les quatre cartes sans recâblage ni câble de bus dans la maison, en moins d'un mètre de rail. Mais chaque poussoir passe par un module FTS14EM, le bus et un actionneur : **règle 1 non tenue**. Elle fait moins bien que KNX sur la règle 2 : les télérupteurs FSR14-4x sont monostables et alimentés par le 12 V du bus ; la perte d'une alimentation **éteint toutes les lumières de sa zone**. En configuration par zone (trois bus, trois alimentations, trois maîtres), **aucune des huit défaillances uniques ne prive toute la maison de ses boutons** ; trois privent une zone, quatre si le maître de bus est nécessaire à l'exécution des ordres, point qu'Eltako ne documente pas.
    - **En dérivation** : la couche la moins chère et la plus compacte des bus de ce comparatif, sans Linux, sans licence, avec un outil gratuit et le fabricant des variateurs de la V2. Elle est propriétaire, à un seul fabricant, configurée sous Windows, reliée à la passerelle par une liaison série USB, avec une bibliothèque Python mais pas de bibliothèque Go.
    - **Coût estimé** : ≈ 1 800 € HT en configuration minimale, ≈ 2 100 € HT par zone, ≈ 1 600 € HT en couche domotique seule. Prix d'octobre 2026 d'une boutique allemande, TTC à 19 %, convertis en HT ; trois références au prix conseillé Eltako HT, faute de prix boutique.
    - **Réserve** : estimations à confirmer par un électricien, des devis, le fabricant et des essais. L'alimentation 24 V des boucles de poussoirs n'a pas de prix trouvé.

## Principe et gamme

Eltako GmbH, à Fellbach près de Stuttgart, est une entreprise familiale fondée en 1949 avec le premier télérupteur. La **Series 14** (« Baureihe 14 ») est sa gamme d'appareils modulaires sur bus RS-485 pour l'installation centralisée de sa radio de bâtiment : le catalogue 2026 la présente comme un chapitre éprouvé du montage centralisé d'actionneurs radio. L'année de lancement n'a pas été trouvée ; le plus ancien guide de planification retrouvé date de 2014.

Le bus est propriétaire : quatre fils (RSA, RSB, +12 V, GND) et une ligne d'arbitrage HOLD, reliés d'appareil en appareil par des cavaliers enfichables sur le rail. Les télégrammes ont la structure des télégrammes radio EnOcean ; la bibliothèque libre `eltako14bus` décrit le protocole comme une extension du protocole série EnOcean ESP2. Chaque bus accepte 126 adresses d'appareils ; les segments sur plusieurs rails ou coffrets se relient par un câble blindé de 100 m au plus.

Le système est **hybride**. Les liens poussoir → actionneur sont mémorisés dans chaque actionneur, jusqu'à 120 identifiants, sans contrôleur logique. Mais le bus a besoin d'un **maître** : le module antenne radio FAM14, ou l'interface FTS14KS sans radio. Tous les actionneurs sont alimentés par le 12 V du bus, fourni par l'alimentation FSNT14 de 12 W.

**Series 12 et Series 14.** La V2 retient des appareils Eltako à entrée locale : le variateur EUD12D-UC, dont les entrées de commande de 8 à 230 V sont isolées de l'alimentation, l'ES12Z-200-UC au banc deux lumières, l'EGS12Z en option pour les volets. Ces appareils lient eux-mêmes leur entrée à leur sortie, sans bus : un contact sec de la domotique s'y ajoute en parallèle du poussoir. La Series 14 reprend les mêmes fonctions (FSR14 télérupteur, FSB14 volets, FUD14 variateur) mais retire l'entrée locale : l'ordre arrive par le RS-485, depuis un module d'entrées FTS14EM. Les deux gammes ne se mélangent pas sur un rail sans passerelle ; la FGW14 relie encore les anciens composants de bus Series 12. Ce dossier ne modifie pas la V2.

## Dans l'armoire sans recâblage

Les poussoirs restent des contacts secs : des modules **FTS14EM** les lisent, et le bus reste dans l'armoire. Seules les nappes des poussoirs parcourent la maison, comme aujourd'hui.

| Fonction | Module | Voies | Largeur | Ce qu'il faut savoir |
| --- | --- | --- | --- | --- |
| 63 poussoirs | FTS14EM | 10 entrées, commun -E | 2 modules | Tension de boucle universelle 8 à 230 V, « isolée de l'alimentation » ; Eltako recommande **24 V continu** par une alimentation séparée et impose ≥ 24 V dès que plusieurs entrées servent à des interrupteurs ; 5 à 9 mA à 24 V, compatible avec les jonctions IDC de 1 A ; longueur de ligne publiée à 230 V seulement (0,9 µF ≈ 3 000 m), **non trouvée à 24 V** ; 50 modules et 500 contacts par bus ; pas d'adresse bus, invisible dans PCT14 |
| 25 éclairages | FSR14-4x | 4 contacts NO 4 A | 1 module | Télérupteur ou relais par voie, LED 230 V jusqu'à 200 W, commutation au zéro de tension ; relais **monostables** : « à la perte de l'alimentation, l'appareil s'éteint en mode défini » ; 1 000 manœuvres par heure au plus |
| | FSR14-2x | 1 + 1 contacts NO 16 A | 1 module | Relais **bistable** : état conservé pendant la coupure, mais **extinction au retour** du 12 V ; pour le cumulus, les prises et les machines |
| 15 volets dont le store | FSB14 | 2 moteurs (2 + 2 contacts NO 4 A) | 1 module | Séquence montée-arrêt-descente-arrêt par poussoir, temps de course réglé sur le module, retour du temps écoulé pour la position ; **commande manuelle en face avant prioritaire** ; verrouillage des deux sens par la logique interne, sans temps mort chiffré |
| 8 variateurs | FUD14 | 1 voie, 400 W MOSFET | 1 module, entretoise DS14 au-delà de 200 W | Détection de lampe automatique, aucune charge minimale, mémoire du niveau à la coupure ; **aucune entrée de commande locale** : ordres par le bus ou la radio seulement. FUD14/800W en 2 modules |
| Fil pilote | F4HK14 | 4 contacts NO 4 A | 1 module | Relais de chauffage à modulation ou tout-ou-rien ; le fil pilote par demi-ondes n'est pas une fonction de la gamme : relais et diodes externes |
| Cumulus, prises, arrosage, machines | FSR14-2x, FMZ14 | 16 A ; inverseur 10 A temporisé | 1 module | Contacts secs |
| Maître de bus | FAM14 (radio) ou FTS14KS (sans radio) | | 1 module | Livré avec une FSNT14, deux terminaisons, les cavaliers et la prise mini-USB pour PCT14 ; le FAM14 scrute le bus et interroge les actionneurs pour les retours d'état |
| Alimentation | FSNT14-12V/12W | 12 W | 1 module | Protégée contre les courts-circuits, redémarrage automatique ; une de plus par tranche de 12 W, séparée par un pont TB14 ; **peut se monter en redondance** |
| Passerelle série | FGW14-USB | USB, 9 600 ou 58 000 bauds | 1 module | Vers la passerelle Essensys ; peut aussi coupler deux bus Series 14 |

Les boutons radio, les écrans et les poussoirs EnOcean de la gamme ne sont pas retenus : ils supposent de la radio ou un recâblage.

### Configuration minimale

Un bus, un maître, tout dans l'armoire : FAM14 et sa FSNT14, sept FTS14EM (70 entrées), sept FSR14-4x (28 voies), huit FSB14 (16 volets), huit FUD14, un F4HK14, un FSR14-2x, une FGW14-USB. Le bilan de puissance, ≈ 12,6 W, dépasse les 10 W d'une alimentation : une seconde FSNT14 et un pont TB14. 58 adresses sur 126. **44 à 48 modules, soit ≈ 0,8 à 0,9 m de rail**, entretoises DS14 comprises si les variateurs dépassent 200 W. Une alimentation 24 V pour les boucles de poussoirs s'ajoute.

### Configuration résiliente

**Un bus par zone**, chacun avec son maître FTS14KS et sa FSNT14, sa FGW14-USB vers la passerelle, ses entrées et ses actionneurs. Les trois bus ne communiquent pas entre eux : les commandes centrales inter-zones passent par la passerelle, qui tient trois liaisons USB.

| Bus | FTS14EM | FSR14 | FSB14 | FUD14 | Puissance | Largeur |
| --- | --- | --- | --- | --- | --- | --- |
| Pièces de vie (20 poussoirs, 5 éclairages, 6 volets, 3 variateurs) | 2 | 1 × 4x + 1 × 2x | 3 | 3 | ≈ 3,6 W | 15 |
| Chambres (21, 7, 5, 4) | 3 | 2 × 4x | 3 | 4 | ≈ 4,7 W | 18 |
| Pièces d'eau (22, 13, 4 dont le store, 1) | 3 | 4 × 4x | 2 | 1 | ≈ 4,9 W | 16 |

Un FSR14-4x pour les prises, l'arrosage et les machines, un FSR14-2x pour le cumulus et un F4HK14 s'ajoutent sur l'un des bus. Chaque bus reste sous 10 W, donc une seule FSNT14 par zone, qu'une seconde peut doubler en redondance. **≈ 52 modules, soit ≈ 0,95 m de rail**, jusqu'à ≈ 60 modules (1,1 m) avec les entretoises DS14.

## Seule face à l'exigence

### Les sept règles

| Règle | Tenue | Pourquoi |
| --- | --- | --- |
| 1. Pas de calculateur entre le bouton et sa charge | **Non tenue** | Le poussoir attaque un FTS14EM qui émet un télégramme sur le bus ; l'actionneur, alimenté par le bus, l'exécute. Aucun FSR14-4x, FSB14 ni FUD14 n'a d'entrée de commande locale ; le tableau technique du catalogue ne donne une entrée locale 230 V qu'aux FSR14-2x, FMZ14, F2L14 et FTN14 |
| 2. L'état vit dans un organe bistable | Non tenue | FSR14-4x monostable : perte du 12 V, extinction. FSR14-2x bistable, mais extinction au retour de l'alimentation. FUD14 : mémoire du niveau, lumière éteinte pendant la coupure |
| 3. La domotique ajoute, ne retire jamais | Non tenue | Le bus **est** la domotique : un télégramme faux commute n'importe quelle voie. Pendant une session PCT14, les ordres radio ne sont pas exécutés ; les ordres des FTS14EM, non précisé. Parades : commande manuelle prioritaire du FSB14, position TEST du FSR14, toutes deux électroniques et alimentées par le bus |
| 4. Une source et un fusible par zone, un fusible pour la domotique | Partielle | Une FSNT14 par bus de zone, redondance possible ; les boucles de poussoirs ont leur propre 24 V ; mais entrées et actionneurs partagent le 12 V du bus, sans fusible qui sépare le bouton de la domotique |
| 5. Barrière 4 kV et 8 mm, 0 V jamais au PE, parafoudres hors coffrets | Partielle | Les îlots existent : la FSNT14 « découple l'électronique du 230 V », les entrées FTS14EM sont « isolées de l'alimentation », les contacts « libres de potentiel ». Aucune valeur n'est publiée pour ces barrières ; la seule tension d'essai du catalogue, **2 000 V** entre commande locale et contact des FSR14-2x, FMZ14 et F2L14, est sous les 4 kV. Ni SELV, ni catégorie de surtension, ni parafoudre dans les documents |
| 6. Replis choisis au câblage, essayés à la recette | Partielle | Le repli est fixé par le fabricant, « extinction en mode défini », pas réglable par voie ni au câblage ; seule la commande manuelle du FSB14 est un repli d'exploitation |
| 7. Isolement mesuré chaque année | Tenue | Rien ne l'empêche ; le manuel décrit le dépannage du bus au multimètre (120 à 140 Ω entre RSA et RSB, 11 à 12 V, 3 à 5 V sur HOLD) |

### Les causes communes

Dans la configuration résiliente, la liste fermée du comparatif donne :

| Défaillance unique | Prive de ses boutons… | Pourquoi |
| --- | --- | --- |
| 1. Alimentation du bus | une zone | Une FSNT14 par bus ; tous les actionneurs de la zone s'éteignent, et ses boutons se taisent, jusqu'au remplacement. Une seconde FSNT14 en redondance écarte la panne d'un seul convertisseur |
| 2. Court-circuit ou ligne collée | une zone | Les trois bus sont séparés, sans liaison native ; la FSNT14 tient le court-circuit et redémarre seule ; une entrée collée fait ré-émettre E10 toutes les 5 min, sans diagnostic |
| 3. Contrôleur central | une zone, à confirmer | Pas de contrôleur logique ; mais un maître par bus. Le manuel évoque un bus « fonctionnant sans FAM14 » et la bibliothèque libre fonctionne « avec ou sans FAM14 » ; **aucun document Eltako ne dit si les actionneurs exécutent encore les ordres des FTS14EM quand le maître est en panne et le 12 V présent** |
| 4. Logiciel figé | un module | Pas de logiciel central ; un actionneur figé prive ses voies ; la passerelle n'est pas dans la boucle |
| 5. Mise à jour ratée | un module | Aucune mise à jour de firmware des actionneurs trouvée ; PCT14 écrit la mémoire d'un appareil à la fois |
| 6. Licence, compte ou cloud | rien | PCT14 est gratuit, aucun cloud dans la gamme |
| 7. Commutateur ou routeur | rien | Liaison USB vers la passerelle, hors du chemin du bouton |
| 8. Foudre sur le chemin du bus | une zone | Le bus reste dans l'armoire ; l'onde entre par les boucles de poussoirs et frappe le FTS14EM de la zone, isolé du bus sans valeur chiffrée ; GND commun à tout le bus de la zone |

**Total : 0 défaillance unique prive toute la maison**, 3 privent une zone, 4 si le maître de bus est nécessaire à l'exécution. En configuration minimale, l'alimentation (ou le groupe d'appareils derrière le pont TB14), le court-circuit du bus unique, la foudre et, sous la même réserve, le maître privent toute la maison : **3**, ou 4.

Le découpage par zone retrouve donc, comme KNX, trois boîtiers indépendants sans boîtier principal. La différence est dans la zone touchée : KNX laisse les lumières dans leur état, la Series 14 les éteint.

### Ce qui reste, panne par panne

| Panne | Ce qui reste |
| --- | --- |
| Alimentation 12 V d'une zone | Les deux autres zones. Dans la zone touchée : **toutes les lumières éteintes**, volets arrêtés, variateurs éteints avec mémoire du niveau ; aucun bouton ; les commandes manuelles des modules, électroniques, sont mortes aussi |
| Maître de bus d'une zone, 12 V présent | À confirmer auprès d'Eltako : soit les actionneurs exécutent encore les ordres des FTS14EM, soit la zone perd ses boutons. Perdus dans tous les cas : les retours d'état et la liaison PCT14 |
| Passerelle Essensys ou FGW14-USB | Tout le local, bus par bus ; perdues : l'application et les commandes inter-zones |
| Coupure du secteur | Tout s'éteint ; au retour, FSR14 éteints « en mode défini », FUD14 avec leur niveau mémorisé, FMZ14 contact 1 fermé |
| Un actionneur | Ses voies ; échange, puis réapprentissage des identifiants par les commutateurs ou restauration par PCT14 |
| Foudre par une ligne de poussoirs | Le FTS14EM de la zone au pire ; les autres zones. Eltako avance le découplage du 230 V par la FSNT14, sans valeur ; aucun retour public de FAM14 détruit par la foudre |
| Session PCT14 ouverte | Les ordres radio ne sont pas exécutés ; les ordres des FTS14EM, non précisé |

Les retours d'utilisateurs parlent surtout du bus : poussoirs qui demandent un second appui après le raccordement d'openHAB, « perturbations occasionnelles du bus », alimentations usées avec le temps.

## En dérivation sur le filaire V2

Dans cette lecture, les télérupteurs, les chaînes de volets et les variateurs EUD12D-UC à entrée locale gardent le chemin du bouton. La Series 14 fournit la couche domotique :

- **Sorties** : 22 FSR14-4x, soit 88 contacts NO de 4 A, commandent les bobines 24 V des relais de couplage 38.51 de la V2, qui ferment les contacts secs en parallèle des poussoirs. Le courant d'une bobine de 38.51 face à la charge admise par un contact FSR14 reste à vérifier.
- **Entrées** : sept FTS14EM lisent les 70 contacts des relais de recopie, sous un 24 V de l'îlot domotique.
- **Infrastructure** : un FTS14KS sans radio et sa FSNT14, une seconde FSNT14 (≈ 17 W au total), une FGW14-USB vers la passerelle. 88 adresses sur 126.
- **Battement de cœur** : la gamme n'a pas de relais de garde. Le réarmement du chien de garde matériel de la V2 revient à la **passerelle**, qui porte la logique ; un contact FSR14, limité à 1 000 manœuvres par heure, ne peut pas battre toutes les 200 ms. Une voie FSR14 en télérupteur à retombée temporisée peut ajouter une garde lente, de l'ordre de la minute, qui retombe si la passerelle cesse de l'écrire. Si la passerelle se tait, le relais de garde retombe en moins d'une seconde ; si le 12 V du bus tombe, tous les FSR14-4x s'ouvrent : la couche se retire d'elle-même. Un contact FSR14 soudé reste borné par le câblage de la V2.
- **Logique et interface** : la passerelle, par la liaison série ESP2 de la FGW14-USB. Les actionneurs ne portent que des scènes et des temporisations par voie.

Ce que la couche apporte : ≈ 1 600 € HT, **≈ 40 modules (≈ 0,75 m de rail)**, aucun Linux ni logiciel du projet sur le bus, aucune licence, un outil gratuit, et le fabricant des variateurs déjà retenus. Ce qu'elle coûte : un bus propriétaire à un seul fabricant, un outil Windows, une liaison série USB au lieu d'un réseau, une bibliothèque Python LGPL et des intégrations communautaires, pas de bibliothèque Go. Face à la Revolution Pi Connect 5 (≈ 581 € HT nue, plus ses modules d'entrées-sorties), la Series 14 est moins chère et plus compacte, sans le Linux de la Connect 5 dans l'armoire. Face à KNX (≈ 3 100 € HT, 88 modules), elle coûte moitié moins et tient sur moitié moins de rail. Face au serveur d'entrées-sorties léger ([dossier Modbus](modbus-es.md)), elle est dans la même gamme de prix, avec des relais intégrés et sans protocole ouvert.

## Foudre et isolement

- **Le bus reste dans l'armoire** : les cavaliers relient les modules sur le rail ; seules les boucles de poussoirs sortent, sous 24 V continu recommandé par Eltako. Les segments sur plusieurs coffrets se relient par un câble blindé, GND commun à tout le bus.
- **Tensions d'essai** : aucune fiche FTS14EM, FSR14-4x, FSB14 ou FUD14 consultée ne chiffre l'isolement entre les entrées et le bus, ni entre le bus et les contacts 230 V. Le tableau du catalogue donne 2 000 V entre commande locale et contact pour les actionneurs à entrée 230 V, 4 000 V pour le FSR14SSR à opto-triac, « – » pour les autres. Ni SELV, ni PELV, ni catégorie de surtension. La barrière de 4 kV et 8 mm de la V2 est donc **à faire attester** ; sans attestation, un relais de couplage 38.51 (6 kV) devant chaque voie, ce que la lecture en dérivation prévoit déjà.
- **Découplage** : Eltako présente la FSNT14 comme ce qui « découple l'électronique de tous les appareils du réseau 230 V » et les protège des pointes de tension, argument de durée de vie plus que de foudre.
- **Parafoudres** : aucune recommandation dans les documents Series 14 consultés. Les entrées 230 V du FTS14EM admettent 100 mA pendant moins de 5 s.
- **Retours de terrain** : aucun cas public de FAM14 ou d'actionneur détruit par la foudre n'a été trouvé.

## Logiciel, paramétrage et passerelle Essensys

| Point | Ce qu'on a trouvé |
| --- | --- |
| Outil | **PCT14**, Windows, **gratuit**, mise à jour automatique depuis la version 8.1 ; connexion par la prise mini-USB du FAM14 ou du FTS14KS, avec un code de légalisation fourni dans l'emballage ; liste des appareils, lecture et écriture de la mémoire, sauvegarde et restauration du projet. Sous Mac ou Linux, les utilisateurs passent par une machine virtuelle |
| Sans PC | Apprentissage par les commutateurs rotatifs de chaque actionneur (LRN, CLR), suffisant pour une installation simple |
| Formation | « Installation réservée aux électriciens » sur chaque notice ; aucune certification pour PCT14 ; manuel PCT14 en allemand |
| Mise à jour | Aucune mise à jour de firmware des actionneurs ni du maître trouvée ; PCT14 affiche la version logicielle de chaque appareil |
| Sécurité | Code de légalisation PCT14 ; le FAM14 porte une radio EnOcean 868 MHz, le FTS14KS n'en a pas |
| API pour la passerelle | Liaison série **ESP2-Eltako** par la FGW14-USB (9 600 ou 58 000 bauds) ou la prise mini-USB du maître (57 600 bauds selon l'intégration Home Assistant). Pas de KNXnet/IP, de Modbus ni de REST pour les actionneurs ; MQTT et REST seulement pour les compteurs, par la FGW14WL-IP |
| Bibliothèques libres | `eltako14bus` (Python, LGPL) et son outil `eltakotool` ; intégration Home Assistant **communautaire** `grimmpp/home-assistant-eltako` (MIT, ≈ 1 900 commits, FSR14, FSB14, FUD14 et FTS14EM pris en charge) : l'intégration officielle Eltako de Home Assistant ne couvre que les Series 62 et 64 Matter ; binding openHAB EnOcean officiel en mode RS-485. Bibliothèque Go : non trouvée |
| Cloud | Aucun ; aucun compte |

Côté passerelle, le backend Go doit parler ESP2 sur un port série, protocole documenté par la bibliothèque Python et les deux intégrations, sans bibliothèque Go. Un utilisateur rapporte qu'Eltako reconnaît une déviation de la spécification EnOcean dans ses télégrammes de retour. L'estimation de cette étude est de **trois à six semaines-personne** pour l'intégration, plus quelques jours de PCT14.

## Nomenclature et coût estimé

Prix relevés le 24 octobre 2026 chez elektro-wandelt (Allemagne), TTC à 19 %, convertis ici en HT. Trois références sans prix boutique (FSR14-2x, F4HK14, FMZ14 non retenu) sont comptées au **prix de vente conseillé Eltako HT** imprimé sur leur fiche technique. Au tarif conseillé pour toutes les références, la configuration minimale monterait à ≈ 2 525 € HT.

### Configuration minimale

| Poste | Référence | Qté | Prix unitaire HT | Total HT | Source |
| --- | --- | --- | --- | --- | --- |
| Maître et alimentation | FAM14 avec FSNT14-12V/12W | 1 | 88,05 € (104,78 € TTC) | 88 € | elektro-wandelt |
| Alimentation supplémentaire | FSNT14-12V/12W et pont TB14 | 1 | 30,07 € (35,78 € TTC) | 30 € | elektro-wandelt |
| Entrées | FTS14EM | 7 | 54,02 € (64,28 € TTC) | 378 € | elektro-wandelt |
| Éclairages | FSR14-4x | 7 | 47,46 € (56,48 € TTC) | 332 € | elektro-wandelt |
| Volets | FSB14 | 8 | 46,03 € (54,78 € TTC) | 368 € | elektro-wandelt |
| Variateurs | FUD14 | 8 | 52,08 € (61,98 € TTC) | 417 € | elektro-wandelt |
| Fil pilote | F4HK14 | 1 | 66,67 € (prix conseillé HT) | 67 € | fiche Eltako |
| Cumulus, prises, arrosage, machines | FSR14-2x | 1 | 69,32 € (prix conseillé HT) | 69 € | fiche Eltako |
| Passerelle série | FGW14-USB | 1 | 48,72 € (57,98 € TTC) | 49 € | elektro-wandelt |
| Alimentation 24 V des boucles de poussoirs | SNT12/24V ou équivalent | 1 | non trouvé | — | — |
| **Matériel** | | | | **≈ 1 800 € HT** | |
| Logiciel | PCT14 | 1 | 0 € (gratuit) | 0 € | eltako.com |
| **Total** | | | | **≈ 1 800 € HT** | |

### Configuration résiliente

| Poste | Référence | Qté | Prix unitaire HT | Total HT |
| --- | --- | --- | --- | --- |
| Maîtres et alimentations | FTS14KS avec FSNT14-12V/12W | 3 | 75,61 € (89,98 € TTC) | 227 € |
| Passerelles série | FGW14-USB | 3 | 48,72 € | 146 € |
| Entrées | FTS14EM | 8 | 54,02 € | 432 € |
| Éclairages et divers | FSR14-4x | 8 | 47,46 € | 380 € |
| Cumulus | FSR14-2x | 1 | 69,32 € (prix conseillé HT) | 69 € |
| Volets | FSB14 | 8 | 46,03 € | 368 € |
| Variateurs | FUD14 | 8 | 52,08 € | 417 € |
| Fil pilote | F4HK14 | 1 | 66,67 € (prix conseillé HT) | 67 € |
| Alimentation 24 V des boucles de poussoirs | SNT12/24V ou équivalent | 3 | non trouvé | — |
| **Matériel** | | | | **≈ 2 100 € HT** |
| Logiciel | PCT14 | 1 | 0 € | 0 € |
| **Total** | | | | **≈ 2 100 € HT** |

Soit ≈ 300 € HT de plus que la configuration minimale, pour passer de 3 à 0 défaillance unique touchant toute la maison. Avec trois FAM14 à la place des FTS14KS, ≈ 2 140 € HT. Une FSNT14 redondante par zone ajouterait ≈ 90 € HT.

### Couche domotique en dérivation

| Poste | Référence | Qté | Total HT |
| --- | --- | --- | --- |
| Maître et alimentation | FTS14KS avec FSNT14-12V/12W | 1 | 76 € |
| Alimentation supplémentaire | FSNT14-12V/12W et pont TB14 | 1 | 30 € |
| Passerelle série | FGW14-USB | 1 | 49 € |
| Sorties vers les relais de couplage | FSR14-4x | 22 | 1 044 € |
| Entrées de recopie | FTS14EM | 7 | 378 € |
| **Matériel** | | | **≈ 1 580 € HT** |
| Logiciel | PCT14 | 1 | 0 € |
| **Total** | | | **≈ 1 580 € HT**, ≈ 40 modules |

### Ce qui n'est pas dans les totaux

- **Fonctions à reporter** : pas de centrale d'alarme ; les FSR14 ont des modes pour détecteurs de fumée et d'eau, le FTS14EM un mode contact de fenêtre. Écran : l'horloge FSU14 a un afficheur, mais la visualisation passe par un logiciel tiers. Délestage : aucune fonction trouvée ; le FSR14M-2x mesure la puissance par voie (prix conseillé 101,23 € HT), la logique revient à la passerelle.
- **Fil pilote** : contacts du F4HK14 et diodes externes, montage non documenté par Eltako.
- **Alimentation 24 V** des boucles de poussoirs, entretoises DS14, ponts TB14, rail et bornes : non chiffrés.
- **Électricien** : de l'ordre de 4 à 6 jours (estimation sans devis, moins de câblage que la V2 : les modules remplacent les télérupteurs et les relais de volets).
- **Logiciel** : ≈ 3 à 6 semaines-personne (estimation de cette étude).
- **Place** : ≈ 0,8 à 0,9 m (minimale), ≈ 0,95 à 1,1 m (par zone), ≈ 0,75 m (dérivation, en plus des 1,6 à 2,1 m de la couche filaire).

## Ouverture et pérennité

- **Propriétaire** : bus RS-485 Eltako, télégrammes au format EnOcean, protocole série proche d'ESP2. Un seul fabricant d'actionneurs de bus ; l'écosystème EnOcean Alliance n'existe que côté radio.
- **Ancienneté** : au moins douze ans (guide de planification de 2014), fabricant de 1949. Notices révisées régulièrement (FAM14 en 2022, FTS14EM en 2023, FSB14 et FSR14-4x en 2024), catalogue 2026 complet, 23 revendeurs en ligne pour le FAM14. Aucune déclaration de fin de vie trouvée ; aucune disponibilité des pièces à dix ans publiée.
- **Succession** : les nouvelles gammes Eltako, Series 62-IP (Wi-Fi) et Series 64 (Matter), sont des appareils d'encastrement, pas des modules rail DIN sur RS-485. La FGW14 relie encore les anciens composants de bus Series 12 : Eltako a déjà remplacé une gamme de bus en gardant une passerelle.
- **Vente libre** en ligne, prix conseillés publics sur les fiches, aucune licence, aucun cloud.
- **Communauté** : intégration Home Assistant communautaire active, binding openHAB officiel, bibliothèque Python LGPL, projets documentés sur GitHub, forums allemands et français. Le support Eltako a reconnu une déviation de la spécification EnOcean ; openHAB note que « tous les télégrammes radio ne sont pas publiés sur le bus ».

## Verdict

- **Seule** : la Series 14 remplace l'armoire sans toucher un fil, dans moins d'un mètre de rail et pour ≈ 2 100 € HT par zone, et son découpage en trois bus ne laisse aucune défaillance unique priver toute la maison. Elle ne tient pas la règle 1 et fait moins bien que KNX sur la règle 2 : la perte d'une alimentation de zone éteint toutes ses lumières au lieu de les laisser dans leur état, et le rôle du maître de bus dans l'exécution des ordres n'est pas documenté. C'est le bus de la famille dont la V2 a retenu le filaire ; il n'en a pas la résilience.
- **En dérivation** : la couche la plus compacte et la moins chère des bus, sans Linux ni licence, chez le fabricant des variateurs déjà choisis ; mais propriétaire, à un seul fabricant, outillée sous Windows et reliée à la passerelle par une liaison série sans bibliothèque Go.
- **À qui elle convient** : à qui a déjà de la radio EnOcean ou veut un bus bon marché et compact, accepte un seul fournisseur et une intégration communautaire.

## Sources

Toutes consultées le 24 octobre 2026.

1. [Fiche FTS14EM](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_FTS14EM.pdf) et [notice FTS14EM](https://www.eltako.com/fileadmin/downloads/en/_bedienung/FTS14EM_30014060-3_gb.pdf) : 10 entrées 8 à 230 V isolées, courants de commande, 0,9 µF à 230 V, ≥ 24 V, E10 cyclique, prix conseillé 73,03 € HT.
2. [Notice FAM14](https://www.eltako.com/fileadmin/downloads/en/_bedienung/FAM14_30014000-6_gb.pdf) et [fiche FAM14](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_FAM14.pdf) : 126 adresses, scan du bus, 12 V, ordres radio suspendus pendant PCT14, prix conseillé 130,80 € HT.
3. [Fiche FSNT14-12V/12W](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_FSNT14-12V_12W.pdf) : court-circuit, redémarrage automatique, redondance, TB14.
4. [Fiche FBA14](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_FBA14.pdf) : liaison entre coffrets, 100 m.
5. [Manuel Series 14 RS485 bus](https://www.eltako.com/fileadmin/downloads/en/_bedienung/Series_14_RS485_Bus_DIN_Rail_Mounted_DevicesSeries_gb.pdf) et [Planungshilfe Baureihe 14](https://www.eltako.com/fileadmin/downloads/de/_bedienung/RS485-Bus-Reiheneinbaugeraete_Baureihe_14_Planungshilfe_und_Betriebsanleitung_dt.pdf) : table de puissance, HOLD et Enable, 120 identifiants par actionneur, dépannage du bus, 24 V recommandé, bus « sans FAM14 », découplage du 230 V.
6. [Fiche FSR14-4x](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_FSR14-4x.pdf) et [notice FSR14-4x](https://www.eltako.com/fileadmin/downloads/de/_bedienung/FSR14-4x_30014001-6_dt.pdf) : 4 × 4 A, LED 200 W, extinction définie, position TEST.
7. [Fiche FSR14-2x](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_FSR14-2x.pdf) : 16 A, état conservé à la coupure, extinction au retour.
8. [Fiche FSB14](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_FSB14.pdf) et [notice FSB14](https://eltako.com/fileadmin/downloads/en/_bedienung/FSB14_30014004-6_gb.pdf) : 2 moteurs, commande manuelle prioritaire, temps de course, retour de position.
9. [Fiche FUD14](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_FUD14.pdf) et [fiche FUD14/800W](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_FUD14_800W.pdf) : 400 W, mémoire à la coupure, DS14 au-delà de 200 W.
10. [Fiche FHK14](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_FHK14.pdf) et [fiche F4HK14](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_F4HK14.pdf) : relais de chauffage, prix conseillés.
11. [Fiche FGW14-USB](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_FGW14-USB.pdf) : USB, couplage de deux bus, Series 12.
12. [Fiches FSR14M-2x, FMZ14, FTD14, FGW14WL-IP](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_FGW14WL-IP.pdf) : mesure, temporisation, duplicateur radio, MQTT pour les compteurs.
13. [Catalogue général Eltako, chapitre 1](https://www.eltako.com/fileadmin/downloads/de/Gesamtkatalog/Eltako_Gesamtkatalog_Kap1_low_res.pdf) : gamme, tableau technique (tensions d'essai 2 000 et 4 000 V, AgSnO2, IP50/IP20).
14. [Fiche EUD12D-UC](https://www.eltako.com/fileadmin/downloads/en/_datasheets/Datasheet_EUD12D-UC.pdf) : entrées de commande isolées, 400 W, Series 12.
15. [Manuel PCT14](https://www.eltako.com/fileadmin/downloads/de/Software/PCT14_Handbuch.pdf) et [page PCT14](https://eltako.com/en/?p=72293) : gratuit, Windows, mise à jour automatique.
16. [Home Assistant, intégration Eltako](https://www.home-assistant.io/integrations/eltako/) : Series 62 et 64 seulement.
17. [grimmpp/home-assistant-eltako](https://github.com/grimmpp/home-assistant-eltako) et [sa documentation des passerelles](https://github.com/grimmpp/home-assistant-eltako/blob/main/docs/gateways/readme.md) : FAM14 et FGW14-USB, ESP2 57 600 bauds.
18. [cvanlabe/Eltako-home-automation](https://github.com/cvanlabe/Eltako-home-automation) : câblage FTS14EM, PCT14 en machine virtuelle.
19. [eltako14bus sur PyPI](https://pypi.org/project/eltako14bus) : LGPL, extension d'ESP2, « avec ou sans FAM14 ».
20. [Planungshilfe Baureihe 14, édition 2014](https://www.mikrocontroller.net/attachment/226432/RS485-Bus-Reiheneinbaugeraete_Baureihe_14_Planungshilfe_und_) : plus ancien document daté.
21. [Eltako, prospectus nouveautés](https://www.eltako.com/fileadmin/downloads/de/Prospekte/Neuheiten_Prospekt_dt.pdf) : Series 62-IP et 64, encastrées.
22. [openHAB, binding EnOcean](https://www.openhab.org/addons/bindings/enocean/) et [guide communautaire FSR14/FSB14/FUD14 via FGW14](https://community.openhab.org/t/beginners-guide-for-implementing-eltako-fsr14-fsb14-fud14-via-fgw14/136872) : RS-485, ESP2, télégrammes non publiés, second appui.
23. [openHAB, retour FAM14](https://community.openhab.org/t/getting-feedback-from-eltaco-fam14/151172) et [forum HACF, enoceanmqtt et Eltako](https://forum.hacf.fr/t/enoceanmqtt-et-eltako-appareillage-de-modules-lumiere-fsr14-4x-et-volet-fsb14-avec-une-cle-usb300/35090) : retours d'utilisateurs.
24. [KNX-User-Forum, retour FSR14/FAM14 par passerelle Weinzierl](https://knx-user-forum.de/forum/öffentlicher-bereich/knx-eib-forum/1916692-rückmeldung-von-eltako-fsr14-fam14-über-weinzierl-enocean-gateway) : déviation de la spécification EnOcean.
25. [Eltako, 75 ans](https://www.eltako.com/en/75-years/) : 1949, Fellbach.
26. Prix : [elektro-wandelt, recherche par référence](https://www.elektro-wandelt.de/index.php?cl=search&searchparam=30014001), [elektro-wandelt FTS14EM](https://www.elektro-wandelt.de/Eltako-FTS14EM-Taster-Eingabemodul-fuer-RS485-Bus-30014060.html), [elektro-wandelt FBA14](https://www.elektro-wandelt.de/Eltako-FBA14-Busankoppler-RS485-30014018.html), [elektromax24 FUD14](https://www.elektromax24.de/eltako-rs485-bus-universal-dimmaktor-fud14-bis-400w), [voelkner FMZ14](https://www.voelkner.de/products/6670452/Eltako-FMZ14-RS485-Aktor-Rack-Schaltleistung-max.-2000W.html), [zaehlerschrank24 EUD12D-UC](https://www.zaehlerschrank24.de/multi-dimmschalter-eud12d-uc.html), [comparateur heise, FAM14](https://preisvergleich.heise.de/eltako-fam14-funk-antennenmodul-fuer-rs485-bus-30014000-a2836762.html).
27. [EnOcean Alliance, FSR14-4x](https://www.enocean-alliance.org/product/eltako_actuator-fsr14-4x/) : « le fonctionnement exige le FAM14 », 868 MHz.

!!! note "À confirmer auprès des fabricants"
    Le comportement des actionneurs quand le maître de bus (FAM14 ou FTS14KS) est en panne et le 12 V présent ; les tensions d'essai entre les entrées FTS14EM et le bus, et entre le bus et les contacts 230 V des FSR14-4x, FSB14 et FUD14, avec la classe SELV ou PELV ; la longueur de ligne admise à 24 V continu sur les FTS14EM ; l'existence d'une mise à jour de firmware et son échec ; la commande manuelle du FUD14 ; le verrouillage et le temps mort du FSB14 ; l'exécution des ordres FTS14EM pendant une session PCT14 ; la version actuelle du FAM14 (1 module 12 V ou 2 modules 230 V) ; les recommandations foudre d'Eltako ; la charge minimale des contacts FSR14 face à une bobine de 38.51 ; les prix boutique des FSR14-2x, F4HK14 et de l'alimentation 24 V des boucles ; la disponibilité des pièces à dix ans.
