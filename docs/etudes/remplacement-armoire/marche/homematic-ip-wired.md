---
title: "Homematic IP Wired : remplacer l'armoire sans recâblage"
description: "Homematic IP Wired, bus RS-485 propriétaire d'eQ-3, pour remplacer les quatre cartes de l'armoire ESSENSYS sans toucher aux fils : modules d'entrées DRI32 pour les 63 poussoirs, actionneurs DRS8, DRBL4 et DRD3, un point d'accès DRAP par zone. Seul, le bus et son point d'accès restent entre le bouton et sa charge, et les entrées sortent le 24 V du bus vers les poussoirs ; en dérivation, c'est la couche domotique la moins chère des bus du comparatif, avec une centrale locale libre. Environ 3 510 € HT en configuration par zone."
---

# Homematic IP Wired

Homematic IP Wired est la déclinaison filaire du système radio Homematic IP d'eQ-3, lancée en 2018 : un bus RS-485 bon marché, des modules d'entrées pour poussoirs classiques, une centrale locale dont le logiciel passe à la communauté sous le nom OpenCCU. Il est dans ce [comparatif](index.md) pour son prix et pour cette ouverture. Deux faits le cadrent : le point d'accès DRAP alimente tout le bus, à lui seul ; et les entrées DRI32 ne sont pas isolées, elles sortent le 24 V du bus vers les poussoirs.

!!! abstract "Synthèse"
    - **Seule** : Homematic IP Wired reprend les 63 poussoirs et toutes les charges sur rail DIN, et le câble de bus ne sort pas de l'armoire. Mais chaque appui passe par le bus et son point d'accès : **règle 1 non tenue**. Les liaisons directes entrée → actionneur « sans centrale » sont documentées pour la radio et contredites sur le terrain pour le filaire. En configuration par zone (un DRAP, une alimentation et un bus par zone, une centrale CCU3), **4 des huit défaillances uniques privent toute la maison de ses boutons** si la centrale reste sur le chemin, 0 si les liaisons directes tiennent sans elle ; **7** (ou 3) en configuration minimale. Les relais d'éclairage sont bistables ; les actionneurs se commandent en face avant.
    - **En dérivation** : une couche domotique à centrale locale, sans cloud, pilotée par XML-RPC, avec un système de centrale libre (OpenCCU, Apache 2.0) et une intégration Home Assistant locale. Le relais de garde se tient par une minuterie d'actionneur relancée par la passerelle à travers la centrale et le réseau local. Elle vaut la moitié de KNX et compte quatre fois moins de modules.
    - **Coût estimé** : ≈ 2 630 € HT en configuration minimale, ≈ 3 510 € HT par zone, ≈ 2 480 € HT en couche domotique seule. Prix d'octobre 2026, boutiques allemandes, TTC à 19 % convertis en HT.
    - **Réserve** : estimations à confirmer par un électricien, des devis, le fabricant et des essais. Le fonctionnement des liaisons directes filaires sans centrale, l'isolement bus / 230 V et l'état des relais à la coupure n'ont pas été trouvés dans la documentation.

## Principe et gamme

eQ-3 AG (Leer, Allemagne) est née en 2006 de la scission d'ELV, fondée en 1978 ; le groupe familial emploie plus de 1 000 personnes et annonce plus de 50 millions d'appareils livrés. Homematic IP existe depuis 2015 ; la gamme filaire a été présentée en 2018. ELV reste le distributeur historique, héberge les manuels et donne des webinaires techniques gratuits.

Le bus est un **RS-485 propriétaire à 19,2 kbit/s**, chiffré et authentifié, sur quatre fils : 24 V continu TBTS et une paire de données. Le **point d'accès HmIPW-DRAP** est le maître du bus et sa source d'alimentation : il porte les terminaisons et deux sorties de bus de 3 A chacune, qui se câblent en deux lignes, en étoile ou en anneau. En anneau, une coupure du câble scinde le bus en deux segments qui continuent à fonctionner. Limites : 64 appareils par bus, 120 par installation, 300 m de câble.

L'architecture est **hybride**. Les programmes vivent dans une centrale : CCU3 (locale, interface web), Home Control Unit HCU1 (locale avec mode hors ligne) ou le cloud Homematic IP si l'on exploite le DRAP seul. Les **liaisons directes** entre un canal d'entrée et un canal d'actionneur sont mémorisées dans les appareils et présentées par eQ-3 comme fonctionnant sans centrale ; pour le filaire, les retours de terrain sont contradictoires (voir plus bas). La génération actuelle date de 2023 à 2025 pour les manuels consultés.

## Dans l'armoire sans recâblage

Les poussoirs sont des contacts secs : des **modules d'entrées DRI32** les lisent, dans l'armoire. Le câble de bus reste dans le coffret ; les nappes, elles, portent le 24 V du bus.

| Fonction | Module | Voies | Largeur | Ce qu'il faut savoir |
| --- | --- | --- | --- | --- |
| 63 poussoirs | HmIPW-DRI32 | 32 entrées, poussoir, interrupteur ou contact | 4 modules | **« Les entrées ne sont pas libres de potentiel, elles présentent la tension du bus »** : 24 V TBTS, 3,2 mA, commun GND du bus ; organes de commande à spécifier pour 26 V au moins ; 200 m par ligne ; au-delà de 3 m, **câble blindé** exigé et séparation mécanique des conducteurs 230 V, prescription que les nappes existantes ne respectent pas : à discuter avec eQ-3 |
| | HmIPW-DRI16 | 16 | non vérifiée | Même famille ; ne couvre pas une zone de 20 poussoirs |
| 25 éclairages | HmIPW-DRS8 | 8 relais NO unipolaires, **bistables** | 4 modules | 10 A par relais (16 A sur deux relais en mode 2), 80 A par appareil, chaque canal sur sa propre phase ; LED 200 W par canal ; surcharge : arrêt automatique et reprise après ≈ 30 min ; touches Channel et Select en face avant |
| | HmIPW-DRS4 | 4 relais bistables 16 A | 4 modules | Même famille |
| 15 volets dont le store | HmIPW-DRBL4 | 4 canaux, inverseur + NO par canal | 4 modules | 2,2 A / 500 W par moteur, fins de course obligatoires ; une seule direction alimentée par construction, verrouillage et pause à l'inversion non formulés ; « commande directe par poussoirs conventionnels raccordés via le système » ; relais non qualifiés de bistables |
| 8 variateurs | HmIPW-DRD3 | 3 canaux, chacun sur sa phase | 4 modules | Coupure de phase descendante ; 200 VA par canal, **100 W en LED**, 3 VA au minimum ; charges inductives absentes de la liste ; pas de variateur à un canal dans la gamme |
| Fil pilote | aucune offre trouvée | | | Un canal DRS8 commute 8 A de chauffage ; la génération du signal fil pilote n'est pas documentée |
| Cumulus, prises, arrosage, machines | HmIPW-DRS8 | 8 | 4 modules | 16 A possibles sur les relais 4 et 6 |
| Point d'accès et alimentation du bus | HmIPW-DRAP | 2 sorties de bus 24 V, 3 A | 4 modules | Maître du bus, terminaisons, Ethernet, afficheur ; **alimente tout le bus** ; câble entre alimentation et DRAP de 3 m au plus ; classe III |
| Alimentation | HmIPW-DRPS4 | 24 V, 4 A, 96 W | 4 modules | Deux en parallèle avec une diode « pour la redondance » ; alimentation tierce admise si TBTS, isolement 3 750 V, catégorie III, tenue aux coupures 80 ms |
| Centrale | HmIP-CCU3 ou HmIP-HCU1 | | hors rail, murale | CCU3 : locale, sans compte ni cloud en exploitation, Internet pour la mise en service et les mises à jour ; HCU1 : mode hors ligne, plugins Modbus et MQTT |

Le DRAP et les actionneurs ont un afficheur et des touches Channel et Select : chaque canal se commute en face avant, ce qui sert à vérifier le câblage « sur le chantier sans programmation ». Un verrou de commande peut les désactiver. Les afficheurs en verre WGD et les modules FIO6 décentralisés ne sont pas retenus : ils demanderaient de tirer le bus jusqu'aux murs.

### Configuration minimale

Un bus, une alimentation, un DRAP, une centrale : DRAP, DRPS4, deux DRI32 (64 entrées), cinq DRS8 (25 éclairages et les fonctions communes), quatre DRBL4 (16 volets), trois DRD3 (9 variateurs), une CCU3 au mur. **16 modules sur rail, soit 64 unités ≈ 1,12 m de rail**, 15 appareils sur le bus ; consommation au pire cas ≈ 2,4 A, sous les 3 A d'une sortie de bus et répartissable sur les deux.

### Configuration résiliente

Un **DRAP, une alimentation et un bus par zone**, chacun avec ses entrées et ses actionneurs ; une seule centrale CCU3, reliée aux trois DRAP par le réseau local. Il n'y a pas de coupleur de ligne : chaque DRAP est un point d'accès à part entière. Le nombre de DRAP qu'une CCU3 prend en charge aujourd'hui est **à confirmer** (deux en 2021 selon ELV ; « trois points d'accès supplémentaires » selon le comparatif de 2026), de même qu'une liaison directe entre appareils de deux DRAP différents.

| Zone | Modules | Largeur |
| --- | --- | --- |
| Pièces de vie (20 poussoirs, 5 éclairages, 6 volets, 3 variateurs) | DRAP, DRPS4, DRI32, DRS8, 2 × DRBL4, DRD3 | 28 |
| Chambres (21, 7, 5, 4) | DRAP, DRPS4, DRI32, DRS8, 2 × DRBL4, 2 × DRD3 | 32 |
| Pièces d'eau (22, 13, 4 dont le store, 1) | DRAP, DRPS4, DRI32, 2 × DRS8, DRBL4, DRD3 | 28 |
| Communs | DRS8 (cumulus, prises, arrosage, machines), sur l'un des bus | 4 |

**23 modules, soit 92 unités ≈ 1,61 m de rail**, trois alimentations, trois DRAP, une CCU3 au mur.

## Seule face à l'exigence

### Les sept règles

| Règle | Tenue | Pourquoi |
| --- | --- | --- |
| 1. Pas de calculateur entre le bouton et sa charge | **Non tenue** | Le poussoir attaque un DRI32 ; l'ordre traverse le bus et son maître, le DRAP, jusqu'à l'actionneur. Aucun actionneur n'a d'entrée poussoir locale ; tous sont alimentés par le bus. Les liaisons directes sans centrale sont documentées pour la radio ; pour le filaire, des utilisateurs rapportent un appui qui passe puis un blocage dès que le réseau tombe, sans réponse d'eQ-3 |
| 2. L'état vit dans un organe bistable | Tenue pour les éclairages | Relais DRS8 et DRS4 bistables, qui « ne consomment qu'à la commutation ». Les inverseurs du DRBL4 ne sont pas qualifiés ; aucun paramètre « état au retour de tension » trouvé |
| 3. La domotique ajoute, ne retire jamais | Non tenue | Le bus **est** la domotique : un programme faux ou une centrale piratée commute n'importe quelle voie. Parades : bus chiffré et authentifié, CCU3 hors cloud |
| 4. Une source et un fusible par zone, un fusible pour la domotique | Partielle | Une alimentation et un DRAP par zone, oui ; mais boutons et domotique partagent le bus, et le DRAP est le point unique d'alimentation de sa zone. Deux alimentations en parallèle avec diode sont possibles |
| 5. Barrière 4 kV et 8 mm, 0 V jamais au PE, parafoudres hors coffrets | **Non tenue, sauf attestation** | Le bus est TBTS et l'alimentation doit tenir 3 750 V en catégorie III ; mais les entrées DRI32 **sortent le 24 V du bus vers les 63 nappes** : l'îlot des boutons est l'îlot du bus. Aucune tension d'essai bus / 230 V des actionneurs, aucun parafoudre recommandé |
| 6. Replis choisis au câblage, essayés à la recette | Partielle | Commande en face avant de chaque canal et remise en service automatique après surcharge ; mais les liaisons directes et leur comportement se règlent en logiciel, et l'état à la coupure n'est pas documenté |
| 7. Isolement mesuré chaque année | Tenue | Rien ne l'empêche ; le DRAP signale court-circuit (E16), sous-tension (E11) et topologie non conforme (E15), et chaque module affiche la tension du bus |

### Les causes communes

Dans la configuration par zone, la liste fermée du comparatif donne. Chaque fois que les liaisons directes sont en jeu, la première valeur suppose qu'elles exigent la centrale, comme le terrain le rapporte ; la seconde, qu'elles tiennent sans elle, comme eQ-3 le dit pour la radio.

| Défaillance unique | Prive de ses boutons… | Pourquoi |
| --- | --- | --- |
| 1. Alimentation du bus | une zone | Une DRPS4 et un DRAP par zone ; le DRAP alimente tout son bus. Parade : deux DRPS4 en parallèle avec diode (≈ 50 € HT de plus par zone) |
| 2. Court-circuit ou ligne collée | une zone | Un bus par DRAP. Le court-circuit déclenche E16 et doit être **acquitté à la main** après réparation : le segment ne redémarre pas seul. En anneau, une coupure de câble ne prive personne |
| 3. Contrôleur central | toute la maison, ou rien | Une seule CCU3 pour les trois zones. ELV : « liaisons directes fonctionnelles aussi sans CCU » ; terrain filaire : un appui puis blocage sans réseau, liaison tenue seulement si aucun programme ne touche le même canal |
| 4. Logiciel figé | toute la maison, ou rien | Même dépendance à la centrale ; un DRAP figé prive sa zone ; chien de garde non documenté |
| 5. Mise à jour ratée | toute la maison, ou rien | Mise à jour de la CCU3 ou de ses appareils, Internet requis ; un DRAP en échec clignote rouge, l'effet d'une interruption n'est pas documenté |
| 6. Licence, compte ou cloud | rien | Aucune licence ; la CCU3 fonctionne « sans enregistrement », sans cloud ni Internet en exploitation. Exploiter le DRAP seul exigerait un Internet permanent, et n'est pas retenu |
| 7. Commutateur ou routeur | toute la maison, ou rien | Les trois DRAP parlent à la CCU3 par le réseau local. Le test de terrain est précisément « câble LAN débranché » : un appui passe, puis plus rien |
| 8. Foudre sur le chemin du bus | une zone | Le câble de bus reste dans l'armoire, mais le 24 V du bus est sur les 20 à 22 nappes de la zone ; l'onde entre par une nappe dans le bus de la zone, isolé des autres bus et de la centrale par les DRAP et l'Ethernet (tenue en kV non chiffrée) |

**Total : 4 défaillances uniques privent toute la maison** si les liaisons directes exigent la centrale, 0 si elles tiennent sans elle ; faute de déclaration écrite d'eQ-3 pour le filaire et devant les retours de terrain, on retient **4**, à trancher par un essai. 3 privent une zone. En configuration minimale, l'alimentation, le court-circuit et la foudre sur le bus unique s'ajoutent : **7** (ou 3).

Ce décompte dit l'essentiel : la gamme découpe bien les zones (un DRAP par zone, vraiment indépendants en alimentation et en bus), mais une centrale unique et le commutateur réseau restent sur le chemin du bouton tant que les liaisons directes filaires n'ont pas prouvé qu'elles s'en passent. Un essai sur banc, CCU3 éteinte et câble réseau débranché, départage ELV et le terrain en une heure.

### Ce qui reste, panne par panne

| Panne | Ce qui reste |
| --- | --- |
| Alimentation ou DRAP d'une zone | Les deux autres zones. Dans la zone touchée : éclairages dans leur état (bistables), volets arrêtés (état des inverseurs non documenté), variateurs à vérifier ; aucun bouton, et les touches de face avant sont hors tension aussi |
| Court-circuit sur un bus | Sa zone, jusqu'à la réparation et l'acquittement E16 sur le DRAP |
| Centrale CCU3 arrêtée, figée ou en mise à jour | Si les liaisons directes tiennent : tous les boutons, perdus les programmes, l'application et les horaires. Sinon : aucun bouton ; touches Channel et Select en face avant de chaque actionneur |
| Réseau local | Même alternative : les trois DRAP sont coupés de la centrale |
| Coupure du secteur | Tout s'arrête ; au retour, relais d'éclairage dans leur état, comportement des autres non documenté ; eQ-3 recommande une ASI pour les usages de sécurité |
| Un actionneur | Ses voies ; échange, et un appareil appairé « récupère sa configuration automatiquement » depuis la centrale. Surcharge : reprise seule après ≈ 30 min |
| Foudre par une nappe | Le DRI32 de la zone au mieux, le bus de la zone au pire ; les autres zones et la centrale derrière l'Ethernet |

## En dérivation sur le filaire V2

Dans cette lecture, les télérupteurs, les chaînes de volets et les variateurs à entrée locale gardent le chemin du bouton. Homematic IP Wired fournit la couche domotique :

- **Sorties** : onze DRS8 (88 contacts NO libres de potentiel) commandent les bobines 24 V des relais de couplage 38.51 de la V2. Chaque canal reçoit sa propre « phase », qui peut être la tension de commande ; eQ-3 interdit de mélanger 230 V et TBTS sur un même actionneur : des DRS8 dédiés à la TBTS.
- **Entrées** : trois DRI32 (96 entrées) lisent les contacts des relais de recopie. Elles sortent le 24 V du bus vers ces contacts : la barrière de 6 kV est le 38.51 de recopie, le DRI32 n'en apporte aucune.
- **Bus** : ≈ 3,2 A au pire cas, au-dessus des 3 A d'une sortie : répartir les actionneurs sur BUS1 et BUS2 du DRAP.
- **Battement de cœur** : la **durée d'enclenchement** d'une liaison directe (minuterie d'escalier, 10 s par exemple) sur un canal DRS8, relancée périodiquement par la passerelle, tient la bobine du relais de garde ; si la passerelle se tait, le canal retombe au bout de la durée. L'ordre de relance traverse la CCU3, le réseau local, le DRAP et le bus : une panne de l'un d'eux fait aussi retomber le relais, ce qui est le comportement voulu. Le chien de garde matériel de la V2 reste en place. Aucune sortie cyclique autonome n'a été trouvée dans les actionneurs.
- **Logique et interface utilisateur** : la passerelle, par XML-RPC vers la CCU3 ou OpenCCU, ou Home Assistant par l'intégration locale. La CCU3 porte des programmes, des horaires et des scènes ; la HCU1, des automatisations locales et des plugins Modbus et MQTT.
- **Durées bornées** : la durée d'enclenchement des liaisons directes limite aussi une impulsion ; le câblage de la V2 les borne de toute façon.

Ce que la couche apporte : une centrale locale sans cloud, un système de centrale libre (OpenCCU, Apache 2.0) qui tourne aussi sur Raspberry Pi ou en conteneur, une API publique et une communauté allemande nombreuse. Ce qu'elle coûte : ≈ 2 480 € HT, 16 modules (≈ 1,12 m de rail, à ajouter aux 1,6 à 2,1 m de la couche filaire) et une CCU3 au mur, un fabricant unique, des entrées non isolées. Face à la Revolution Pi Connect 5 (≈ 581 € HT nue, plus ses modules d'entrées-sorties), c'est un ordre de prix voisin une fois les modules comptés, avec un Linux (la CCU3) à maintenir aussi, mais sur une base que la communauté entretient. Face à KNX en dérivation (≈ 3 100 € HT, 88 modules), moins cher et quatre fois moins large, sans la norme. Face au serveur d'entrées-sorties léger ([dossier Modbus](modbus-es.md)), plus cher et plus lourd en logiciel.

## Foudre et isolement

- **Le câble de bus reste dans l'armoire** avec des DRI32 et des poussoirs classiques. Mais les entrées **ne sont pas optocouplées** : elles sortent la tension du bus, 24 V, commun GND, vers les poussoirs. Les 63 nappes sont donc au potentiel du bus TBTS de leur zone : l'îlot des boutons et l'îlot du bus sont le même, et seul le découpage par DRAP sépare les zones entre elles.
- **Tensions d'essai** : le bus est déclaré TBTS ; les actionneurs et le DRI32 sont de classe II, le DRAP de classe III ; l'alimentation doit tenir 3 750 V entre entrée et sortie en catégorie de surtension III. Aucune fiche ne donne la tension d'essai entre le bus et les contacts 230 V. La barrière de 4 kV et 8 mm de la V2 est donc **à faire attester** ; sans attestation, un relais 38.51 (6 kV) devant chaque voie, comme la V2 le prévoit en dérivation.
- **Câblage** : 230 V et bus cheminés séparément, jamais dans la même boîte de dérivation, cloisons dans le tableau ; au-delà de 3 m, câbles blindés (Cat 5e, J-Y(ST)Y) qui « n'ont pas la tenue en tension requise » pour voisiner le 230 V sans cloisonnement.
- **Parafoudres** : aucune recommandation d'eQ-3 trouvée, dans le manuel du DRAP, le manuel système ni ceux des actionneurs. Les parafoudres de la V2 restent hors des coffrets.
- **Court-circuit** : détecté par le DRAP, acquittement manuel ; l'alimentation doit être protégée et limitée en courant.
- **Retours de terrain** : aucun retour de foudre trouvé pour le filaire.

## Logiciel, paramétrage et passerelle Essensys

| Point | Ce qu'on a trouvé |
| --- | --- |
| Outil | **CCU3** : interface web locale, aucun compte, « sans enregistrement » ; l'installateur peut configurer puis remettre le mot de passe au client. **HCU1** : application et interface web, mode hors ligne, plugins. **Application Homematic IP** : par le cloud, non retenue |
| Formation | Webinaires ELV gratuits ; aucune licence ni certification ; eQ-3 recommande un professionnel |
| Mise à jour | Appareils mis à jour par la centrale, Internet requis ; firmware du DRAP par un outil réseau ; aucun cas de module rendu inutilisable trouvé, effet d'une interruption non documenté |
| Sécurité | Bus chiffré et authentifié, sécurité certifiée VDE ; CCU3 hors cloud ; télémaintenance par VPN |
| API pour la passerelle | **XML-RPC** (spécification publique eQ-3) : `init`, `listDevices`, `event`, paramètres MASTER, VALUES et LINK (les liaisons directes) ; sur la CCU3, port 2010 (42010 en TLS) pour le filaire ; **JSON-RPC** sur 80 et 443 pour les noms et les pièces. MQTT et Modbus par plugins sur la HCU1 |
| Bibliothèques libres | **OpenCCU** (ex-RaspberryMatic, Apache 2.0) : système de centrale pour CCU3, Raspberry Pi, x86, Docker, module Home Assistant ; intégration Home Assistant « Homematic(IP) Local » (MIT, XML-RPC, CCU3 3.61 ou plus) ; adaptateurs ioBroker et openHAB non vérifiés. Bibliothèque Go : aucune trouvée |
| Cloud | Aucun avec la CCU3 en exploitation ; compte pour l'application avec la HCU1 ; permanent avec le DRAP seul |

Côté passerelle, le backend Go doit parler XML-RPC à la CCU3 ou à OpenCCU, et tenir un serveur de rappel pour recevoir les événements. L'estimation est de **trois à six semaines-personne** pour l'intégration, plus une à deux semaines de paramétrage de la centrale : ≈ 4 à 8 semaines avant la bascule. Un Linux, celui de la centrale, tourne dans la maison, mais hors de l'armoire et hors du chemin des contacts si les liaisons directes tiennent.

## Nomenclature et coût estimé

Prix relevés le 24 octobre 2026 sur un comparateur allemand, prix « à partir de » TTC à **19 %**, ELV parmi les vendeurs, convertis ici en HT. Aucun tarif HT public ni distributeur français trouvé. Câbles, borniers et port exclus.

### Configuration minimale

| Poste | Référence | Qté | Prix unitaire HT | Total HT | Source |
| --- | --- | --- | --- | --- | --- |
| Point d'accès | HmIPW-DRAP | 1 | 125,70 € (149,58 € TTC) | 126 € | billiger.de |
| Alimentation | HmIPW-DRPS4 | 1 | 50,26 € (59,81 € TTC) | 50 € | billiger.de |
| Entrées | HmIPW-DRI32 | 2 | 169,95 € (202,24 € TTC) | 340 € | billiger.de, ELV |
| Éclairages et divers | HmIPW-DRS8 | 5 | 149,58 € (178,00 € TTC) | 748 € | billiger.de |
| Volets | HmIPW-DRBL4 | 4 | 139,60 € (166,12 € TTC) | 558 € | billiger.de |
| Variateurs | HmIPW-DRD3 | 3 | 219,39 € (261,08 € TTC) | 658 € | billiger.de |
| Centrale | HmIP-CCU3 | 1 | 151,22 € (179,95 € TTC) | 151 € | billiger.de |
| **Matériel** | | | | **≈ 2 630 € HT** | |
| Logiciel | CCU3 WebUI, OpenCCU | 1 | 0 € | 0 € | eQ-3, GitHub |
| **Total** | | | | **≈ 2 630 € HT** | |

### Configuration résiliente

| Poste | Référence | Qté | Prix unitaire HT | Total HT |
| --- | --- | --- | --- | --- |
| Points d'accès | HmIPW-DRAP | 3 | 125,70 € | 377 € |
| Alimentations | HmIPW-DRPS4 | 3 | 50,26 € | 151 € |
| Entrées | HmIPW-DRI32 | 3 | 169,95 € | 510 € |
| Éclairages et divers | HmIPW-DRS8 | 5 | 149,58 € | 748 € |
| Volets | HmIPW-DRBL4 | 5 | 139,60 € | 698 € |
| Variateurs | HmIPW-DRD3 | 4 | 219,39 € | 878 € |
| Centrale | HmIP-CCU3 | 1 | 151,22 € | 151 € |
| **Matériel** | | | | **≈ 3 510 € HT** |
| Logiciel | CCU3 WebUI, OpenCCU | 1 | 0 € | 0 € |
| **Total** | | | | **≈ 3 510 € HT** |

Soit ≈ 880 € HT de plus que la configuration minimale, pour passer de 7 à 4 défaillances uniques touchant toute la maison (ou de 3 à 0 si les liaisons directes tiennent). Une HCU1 à la place de la CCU3 ajoute ≈ 100 € HT (299,95 € TTC) ; une seconde DRPS4 par zone, en parallèle avec diode, ≈ 50 € HT par zone.

### Couche domotique en dérivation

| Poste | Référence | Qté | Total HT |
| --- | --- | --- | --- |
| Sorties vers les relais de couplage | HmIPW-DRS8 (88 contacts NO) | 11 | 1 645 € |
| Entrées de recopie | HmIPW-DRI32 (96 entrées) | 3 | 510 € |
| Point d'accès, alimentation, centrale | DRAP, DRPS4, CCU3 | 3 | 327 € |
| **Matériel** | | | **≈ 2 480 € HT** |
| Logiciel | CCU3 WebUI, OpenCCU | 1 | 0 € |
| **Total** | | | **≈ 2 480 € HT**, 16 modules et une CCU3 au mur |

### Ce qui n'est pas dans les totaux

- **Fonctions à reporter** : alarme par les fonctions de la centrale et de l'application, avec ASI exigée par eQ-3 pour un usage de sécurité ; pas de centrale d'alarme certifiée trouvée. Écran : afficheur en verre WGD sur bus, prix non relevé. Délestage : aucun dans les actionneurs filaires ; la HCU1 est « préparée pour la gestion d'énergie » ; aucune mesure d'énergie sur les actionneurs filaires.
- **Fil pilote** : aucune offre ; prévoir des relais externes.
- **ASI** pour le DRAP et la centrale, recommandée par eQ-3 : non chiffrée.
- **Électricien** : de l'ordre de 4 à 6 jours (estimation sans devis, moins de câblage que la V2), hors remplacement des nappes par du câble blindé si eQ-3 l'exige.
- **Logiciel** : ≈ 4 à 8 semaines-personne (centrale et passerelle).
- **Place** : ≈ 1,12 m (minimale), ≈ 1,61 m (par zone), ≈ 1,12 m (dérivation, en plus de la couche filaire), plus la centrale au mur.

## Ouverture et pérennité

- **Protocole propriétaire**, un seul fabricant d'appareils de bus. Ouverture par les API publiques de la centrale (XML-RPC, JSON-RPC) et par OpenCCU, système de centrale libre sous Apache 2.0.
- **Ancienneté** : Homematic IP depuis 2015, filaire depuis 2018 ; des appareils Homematic de dix à quatorze ans toujours en service selon des utilisateurs. Tous les modules filaires retenus étaient en stock chez ELV en octobre 2026, aucune fin de vie annoncée.
- **Transition de la centrale** : eQ-3 ne fixe pas de fin de support à la CCU3, mais la transmet à la communauté sous le nom OpenCCU ; eQ-3 y intègre encore ses nouveaux produits **jusqu'à fin 2026**, puis la communauté poursuit ; la CCU3 reste vendue par ELV ; eQ-3 se concentre sur la HCU1, dont la migration depuis une CCU3 efface la programmation antérieure. Que la HCU1 et OpenCCU couvrent toute la gamme filaire après 2026 reste à vérifier.
- **Cloud** : trois modes coexistent ; la CCU3 et le mode hors ligne de la HCU1 permettent une exploitation locale.
- **Communauté** : forums allemands actifs (homematic-forum, ioBroker, simon42), projet OpenCCU sur GitHub, intégration Home Assistant maintenue.
- **Fiabilité rapportée** : essentiellement radio ; appareils durables, mais un utilisateur a abandonné après des années de problèmes de CCU3, et des commandes manquées sont rapportées en radio (sans objet en filaire).

## Verdict

- **Seule** : Homematic IP Wired remplace l'armoire sans toucher un fil, pour moins cher que tout autre bus de ce comparatif, et se découpe vraiment en une zone par point d'accès. Il ne tient pas la règle 1 : chaque bouton passe par le bus et son maître, et une centrale unique reste sur le chemin tant que les liaisons directes filaires n'ont pas prouvé qu'elles s'en passent, ce que le terrain conteste. Ses entrées non isolées mettent le 24 V du bus sur les nappes, et le point d'accès est le point unique d'alimentation de sa zone. Un essai de banc, centrale coupée, dirait si le compte est 4 ou 0.
- **En dérivation** : la couche domotique à bus la moins chère et la moins encombrante, avec une centrale locale libre et une API publique ; moins durable que KNX (un fabricant, une centrale en transition), plus riche que le serveur d'entrées-sorties Modbus.
- **À qui elle convient** : à qui veut une couche domotique locale, bon marché, soutenue par une communauté allemande et un système de centrale libre, et accepte un fabricant unique et une centrale au mur.

## Sources

Toutes consultées le 24 octobre 2026.

1. [Manuel HmIPW-DRAP V1.7 (12/2023)](https://media.elv.com/file/152465_hmipwdrap_um.pdf) : TBTS, topologies, anneau, exigences d'alimentation, codes E15 et E16, acquittement, 6 A et 2 × 3 A, 300 m, 64 et 120 appareils, ASI, remise à zéro.
2. [Fiche HmIPW-DRAP (01/2026)](https://media.elv.com/file/152465_data.pdf) : classe III, commande en face avant.
3. [Page produit DRAP](https://homematic-ip.com/en/product/wired-access-point) : modes d'exploitation, anneau scindé automatiquement.
4. [Manuel HmIPW-DRI32 V1.6 (03/2025)](https://media.elv.com/file/152263_um.pdf) : entrées non libres de potentiel, tension du bus, 26 V, 3,2 mA, 200 m, câble blindé au-delà de 3 m, classe II.
5. [Fiche HmIPW-DRI32](https://media.elv.com/file/152263_data_neu.pdf) : 24 V TBTS, 135 mA, 4 unités.
6. [Manuel HmIPW-DRS8 (2025)](https://media.elv.com/file/151677_um.pdf) : relais bistables, courants, charges, surcharge et reprise à 30 min, classe II, touches Channel et Select, TBTS et 230 V non mélangés.
7. [Manuel HmIPW-DRBL4 V1.7 (03/2025)](https://media.elv.com/file/152431_um.pdf) : fins de course, inverseurs, 2,2 A, surcharge, codes E10 et E11, verrou de commande, commande par poussoirs conventionnels.
8. [Fiche HmIPW-DRD3 (11/2025)](https://media.elv.com/file/152626_data.pdf) : coupure de phase descendante, 200 VA, 3 VA, classe II.
9. [Fiches techniques officielles DRS8, DRBL4, DRI32, DRD3](https://homematic-ip.com/en/product/wired-switching-actuator-8-channels/technical-data) : 80 A, bistable, inverseur + NO, 100 W LED.
10. [Fiche HmIPW-DRPS4 V1.3](https://media.elv.com/file/158080_data.pdf) et [page produit](https://homematic-ip.com/en/product/wired-power-supply-unit) : 24 V, 4 A, parallèle avec diode pour la redondance.
11. [Manuel système Homematic IP Wired V5.4 (04/2024)](https://media.elv.com/file/hmipw_systemhandbuch.pdf) : 120 appareils, 72 W par bus, longueurs, consommations, CCU3 sans cloud ni Internet en exploitation, cloud permanent avec le point d'accès seul.
12. [Fiche HmIP-CCU3 V2.3](https://media.elv.com/file/151965_data_.pdf) : logique locale, « sans enregistrement », alimentation 5 V, dimensions, filaire via DRAP.
13. [Page produit HCU1](https://homematic-ip.com/en/product/home-control-unit) : 350 appareils, trois points d'accès, mode hors ligne, plugins Modbus et MQTT.
14. [Comparatif des centrales ELV V1.0 (02/2026)](https://downloads.elv.com/downloads/downloads/HmIP-Zentralenvergleich-ELV.pdf) : prix publics, stockage local ou cloud, points d'accès supplémentaires.
15. [Webinaire ELV 2021, présentation](https://downloads.elv.com/downloads/Fachseminare/PDFs/2021_04_29_elv_online-fachseminar_vorstellung_hmip-wired.pdf) et [mise en service](https://downloads.elv.com/downloads/Fachseminare/PDFs/2021_05_06_elv_online-fachseminar_inbetriebnahme_hmip-wired.pdf) : 19,2 kbit/s, consommations, commande locale des canaux, liaisons directes, durée d'enclenchement.
16. [Webinaire ELV CCU3 2024](https://downloads.elv.com/downloads/Fachseminare/PDFs/Fachseminar_21_02_2024_Webinar_ELV_Basics_CCU_24.pdf) : « liaisons directes fonctionnelles aussi sans CCU », CCU mémoire centrale des liaisons et programmes.
17. [Spécification XML-RPC HomeMatic V2.16](https://www.eq-3.de/Downloads/eq3/download%20bereich/hm_web_ui_doku/HM_XmlRpc_API.pdf) : méthodes, paramètres MASTER, VALUES, LINK.
18. [OpenCCU (ex-RaspberryMatic)](https://github.com/jens-maus/RaspberryMatic) : Apache 2.0, plateformes, sans cloud.
19. [Intégration Home Assistant « Homematic(IP) Local »](https://github.com/SukramJ/custom_homematic) : MIT, ports, versions requises.
20. [eQ-3, entreprise](https://www.eq-3.de/unternehmen.html) et [annonce Light+Building 2018](https://www.asmag.com/showpost/26511.aspx) : historique, effectifs, lancement du filaire.
21. [ifun.de, 8 juillet 2025](https://www.ifun.de/homematic-ip-schaltzentrale-ccu3-soll-community-projekt-werden-258360/) : CCU3 vers OpenCCU, intégration des nouveautés jusqu'à fin 2026, vente par ELV.
22. [Guide de migration CCU3 vers HCU1](https://media.elv.com/file/hcu1_ccu3-plugin_guideline.pdf) : programmation antérieure supprimée.
23. Prix : [billiger.de, DRS8, DRBL4, DRD3, DRAP, DRPS4, CCU3](https://www.billiger.de/search?searchstring=HmIPW-DRS8), [billiger.de DRI32](https://www.billiger.de/pricelist/3666300609-homematic-ip-wired-smart-home-eingangsmodul-32-fach-hmipw-dri32), [billiger.de DRS4](https://www.billiger.de/pricelist/1887543891-homematic-ip-wired-schaltaktor-4-fach-hmipw-drs4).
24. Forum HomeMatic (allemand) : [liaison directe filaire sans CCU, page 1](https://homematic-forum.de/forum/viewtopic.php?f=71&t=58947) et [page 2](https://homematic-forum.de/forum/viewtopic.php?t=58947&start=10) ; [question générale sur le filaire](https://homematic-forum.de/forum/viewtopic.php?t=57367) ; [construction neuve en filaire (2018)](https://homematic-forum.de/forum/viewtopic.php?f=71&t=43019).
25. [Fil ioBroker sur le filaire (2020)](https://forum.iobroker.net/topic/28504/erfahrungen-mit-homematic-ip-wired/30) : événements non retransmis en présence d'une liaison directe, programme factice.
26. [Fil simon42 (juillet 2026)](https://community.simon42.com/t/homematic-ip-noch-zukunftstauglich/88903?page=2) et [retour d'expérience simon42](https://www.simon42.com/homematic-erfahrungsbericht/) : liaisons directes maintenues serveur arrêté, fiabilité, point d'accès sans Internet.
27. [Liaisons directes, documentation communautaire](https://homematic.simdorn.net/direkte-verknuepfungen/) et [article technikkram (2017)](https://technikkram.net/blog/2017/12/12/homematic-direktverknuepfungen-verknuepfungen-ueber-die-zentrale/) : liaisons stockées dans les appareils, fonctions limitées (Homematic classique).

!!! note "À confirmer auprès des fabricants"
    Où est stockée une liaison directe filaire et la garantie écrite qu'une liaison DRI32 → DRS8, DRBL4 ou DRD3 fonctionne sans centrale, sans HCU1 et sans Internet, le DRAP seul alimenté ; le comportement des actionneurs à la coupure du 24 V et au retour de tension ; la tension d'essai entre le bus et les contacts 230 V, et les parafoudres recommandés ; le verrouillage des deux sens et la pause à l'inversion du DRBL4 ; le nombre de DRAP par CCU3 et une liaison directe entre deux DRAP ; la prescription de câble blindé face aux nappes existantes et la spécification à 26 V des poussoirs ; largeur et prix du DRI16, prix HT chez un distributeur français ; chien de garde du DRAP et effet d'une mise à jour interrompue ; une sortie cyclique autonome pour le relais de garde ; la génération d'un signal fil pilote par relais ; la couverture de la gamme filaire par la HCU1 et OpenCCU après 2026.
