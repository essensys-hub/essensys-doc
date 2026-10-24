---
title: "Solutions du marché : remplacer l'armoire sans recâblage"
description: "KNX et dix autres solutions domotiques (Loxone, Niko, Domintell, Homematic IP Wired, Eltako Series 14, Siemens LOGO!, Wago, Shelly Pro, ESPHome, modules Modbus) évaluées pour remplacer l'armoire ESSENSYS sans toucher aux fils des poussoirs ni des charges : seules face à l'exigence de résilience, puis en couche domotique sur le filaire V2."
---

# Solutions du marché : remplacer l'armoire sans recâblage

La V2 « [filaire d'abord, domotique en dérivation](../v2/filaire-d-abord.md) » répond à l'[exigence de résilience](../../resilience.md) avec des télérupteurs, des relais et des variateurs à entrée locale, et laisse ouvert le choix de la couche domotique. Avant de s'engager, une question se pose : une solution domotique du marché, KNX en tête, pourrait-elle remplacer les quatre cartes de l'armoire **sans toucher au câblage existant** ? Et comment une dizaine de solutions, ouvertes, payantes ou issues de l'automatisme, se comparent-elles sur les mêmes critères ?

Cette étude répond en onze dossiers écrits au même gabarit, puis dans un tableau comparatif. Elle a été relue par un relecteur indépendant. Ses chiffres sont des estimations d'octobre 2026, à confirmer par un électricien, des devis, les fabricants et des essais.

!!! abstract "En bref"
    - **KNX peut remplacer l'armoire sans toucher un fil** : des modules d'entrées lisent les 63 poussoirs, des actionneurs commandent les charges, le bus reste dans l'armoire. Découpé en une ligne par zone, il ne laisse **aucune défaillance unique priver toute la maison** de ses boutons. Mais chaque bouton passe par le bus : la perte d'une alimentation de zone, panne la plus fréquente, coupe 20 à 22 boutons. **Il ne répond pas à l'exigence**, aucune des onze solutions n'y répond.
    - **Seules**, les plus proches de l'exigence sont celles qui lient l'entrée au relais dans le firmware de chaque module, sans bus ni contrôleur : Shelly Pro et ESPHome. Elles y arrivent avec un isolement non publié, un état gardé par logiciel et, pour Shelly, un relais d'interface par poussoir. KNX est la meilleure des architectures à bus ; Domintell est hors contrainte (10 m d'entrées) ; Wago et Domintell gardent 5 à 6 causes communes.
    - **En dérivation**, la couche domotique la moins chère et la plus simple est un **serveur d'entrées-sorties Modbus piloté par la passerelle** (≈ 430 € HT en modules Waveshare, ≈ 3 000 à 3 900 € HT en modules industriels) ; **KNX** (≈ 3 100 € HT) est l'option normalisée et durable, sans logiciel du projet sur le chemin des contacts. Les deux donnent un corps au désaccord « Revolution Pi ou serveur d'E/S léger » de la V2, sans le trancher ici.
    - Chiffres d'octobre 2026, à confirmer par un électricien, des devis, les fabricants et des essais.

## La question, en deux lectures

Chaque solution est lue deux fois.

**Seule.** Elle remplace les quatre cartes : ses modules d'entrées reçoivent les 63 poussoirs, ses actionneurs commandent les charges. On mesure sa distance à l'exigence : que reste-t-il quand son cerveau, son bus, son alimentation, son logiciel ou sa licence tombe ?

**En dérivation.** Elle n'est que la couche domotique posée sur le filaire de la V2 : télérupteurs, chaînes de volets et variateurs à entrée locale gardent le chemin du bouton ; la solution ferme des contacts secs en parallèle des poussoirs, derrière le relais de garde et la borne sectionnable, et lit l'état par des recopies. On la compare aux deux candidates actuelles de la V2 : la Revolution Pi Connect 5 et un serveur d'entrées-sorties léger piloté par la passerelle.

## Ce qui ne change pas

- **63 poussoirs muraux**, contacts secs à impulsion, ramenés à l'armoire sur trois nappes, une par zone (pièces de vie 20, chambres 21, pièces d'eau 22), par des jonctions IDC données pour 1 A.
- **Les charges** restent câblées sur l'armoire : 25 éclairages, 15 volets dont le store (30 relais, deux sens verrouillés), 8 variateurs, fil pilote, cumulus, prises de sécurité, arrosage, coupure des machines.
- **Le câblage de migration** des V1, gardé par la V2 : répartiteur X1, blocs de phase X3, jonctions des nappes, plan de bornage.
- **La passerelle** (Raspberry Pi CM5, backend Go) continue d'exposer l'application : elle doit pouvoir parler à la solution retenue.

Toute solution doit donc fournir, sur rail DIN : des entrées binaires pour 63 contacts secs, des sorties relais 230 V, des sorties variateur, et des contacts pour le fil pilote, le cumulus et les prises. Les boutons tactiles, écrans ou poussoirs connectés d'une gamme ne comptent pas : ils demanderaient de changer les fils. Une solution qui exige un recâblage est marquée **hors contrainte**.

## La grille

Les onze dossiers partagent les mêmes sections et sont notés sur les mêmes critères.

### Les sept règles

Les [sept règles](../../resilience.md#pour-toutes-les-installations-essensys) de la réponse de résilience, règle par règle : **tenue**, **partielle** ou **non tenue**. La règle 1, « un bouton ne passe jamais par un calculateur pour atteindre sa charge », décide de la lecture « seule ». On reprend la définition de la V2, qui tolère le microcontrôleur du commerce d'un variateur Eltako :

| Niveau | Ce que fait le poussoir | Exemple |
| --- | --- | --- |
| **Tenue** | Il attaque directement un organe qui garde l'état, sans bus ni logiciel du projet | Télérupteur, variateur à entrée locale |
| **Partielle** | Il attaque un module du commerce, à firmware fixé par le fabricant, qui lie lui-même son entrée à sa sortie, sans bus ni contrôleur. Une panne ne prive que les circuits de ce module | Module à entrée locale et relais intégré |
| **Non tenue** | L'ordre passe par un bus ou par un contrôleur programmable. La perte du bus, de son alimentation ou du contrôleur coupe le bouton | Bus de terrain, automate, serveur domotique |

Un bus sans contrôleur central, comme KNX, est donc « non tenue » : le dossier dit alors combien de boutons une panne de ligne prive, et quelles parades le fabricant propose.

### Les causes communes

Pour chaque solution, dans sa configuration résiliente (voir ci-dessous), on passe la même liste fermée de défaillances uniques et on compte celles qui privent **toute la maison** de ses boutons :

1. l'alimentation du système ou du bus ;
2. un court-circuit ou une ligne collée sur un bus ;
3. le contrôleur central ;
4. le logiciel figé (plantage sans redémarrage) ;
5. une mise à jour ratée ;
6. une licence, un compte ou un cloud indisponible ;
7. le commutateur ou le routeur du réseau local ;
8. la foudre sur le chemin du bus.

Le conseil d'autocritique avait compté 13, 5, 4 et 0 modes communs pour les trois V1 et le filaire, avec sa propre méthode, dont le détail n'est pas publié. Ces chiffres sont rappelés dans le tableau **dans une colonne à part**, et ne se comparent pas directement au décompte de cette étude.

### Deux configurations par solution

Chaque dossier décrit une **configuration minimale**, conforme au fabricant (un bus, une alimentation, un contrôleur), et une **configuration résiliente**, alignée sur la V2 : un segment, une alimentation et, s'il existe, un contrôleur **par zone**. Le classement, le décompte des causes communes et le coût « armoire complète » portent sur la configuration résiliente ; la minimale est chiffrée à côté, pour montrer l'écart.

### Les autres critères

| Critère | Ce qu'on regarde |
| --- | --- |
| Foudre et isolement | Le bus traverse-t-il la maison ou reste-t-il dans l'armoire ; isolement annoncé entre entrées, bus et contacts 230 V ; possibilité de tenir les barrières de 4 kV et 8 mm et les deux îlots TBTS ; parafoudres dédiés |
| Coût matériel estimé HT | Armoire complète (lecture « seule ») et couche domotique seule (lecture « en dérivation »), prix relevés en octobre 2026, sources citées. Les prix TTC sont convertis en HT au taux de 20 %. Un prix non public est marqué « indicatif, non public » avec sa source |
| Charge de travail | Jours d'électricien ; semaines-personne de logiciel et de paramétrage avant bascule ; outil de configuration, licence, formation |
| Place | Mètres de rail, nombre de coffrets |
| Ouverture et pérennité | Protocole ouvert ou propriétaire, norme, nombre de fabricants, dépendance au cloud ou à une licence, pièces à dix ans, communauté |
| Passerelle Essensys | Protocole exposé (KNXnet/IP, Modbus, MQTT, REST, API locale) et travail estimé côté passerelle |
| Fonctions | Double appui, appui long, scénarios, délestage, alarme, écran : perdus, gardés ou reportés |

**Périmètre du coût comparé** : le même que les totaux de la V2, soit les poussoirs, les éclairages, les volets, les variateurs, le fil pilote, le cumulus, les prises, l'arrosage et la coupure des machines. L'alarme, la sirène, les détecteurs de fuite, l'écran et le délestage sont des **fonctions à reporter**, notées dans chaque dossier avec un ordre de grandeur de prix, hors du total.

**Lecture « en dérivation »** : le dispositif de la V2 s'impose à toutes les solutions (relais de couplage, relais de garde à chien de garde matériel, fusible F2, durées bornées, recopie d'état, barrières de 4 kV). Son coût est déjà dans la V2 ; le coût « en plus » d'une solution ne compte que ce qu'elle apporte : contrôleur, modules d'entrées-sorties, logiciel, licence. Chaque dossier dit qui réarme le chien de garde.

## Les onze solutions

| Dossier | Famille | Pourquoi elle est là |
| --- | --- | --- |
| [KNX TP](knx.md) | Bus normalisé, multi-fabricants | La question de départ ; dossier le plus détaillé |
| [Loxone](loxone.md) | Propriétaire, centralisé | Très répandu en rénovation ; entrées pour poussoirs classiques |
| [Niko Home Control II](niko-home-control.md) | Propriétaire, bus | Modules rail DIN, interface pour contacts secs |
| [Domintell](domintell.md) | Propriétaire, bus | Modules d'entrées dédiés aux poussoirs classiques |
| [Homematic IP Wired](homematic-ip-wired.md) | Propriétaire, bus filaire, firmware alternatif libre | Bus bon marché pour poussoirs classiques ; communauté open source |
| [Eltako Series 14](eltako-series-14.md) | Propriétaire, bus RS-485 | Même fabricant que les variateurs de la V2 |
| [Siemens LOGO! 8](siemens-logo.md) | Automate | Automate d'entrée de gamme très répandu en domotique |
| [Wago PFC200](wago-pfc200.md) | Automate, ouvert | Automate industriel ouvert ; des Wago déjà dans la V2 |
| [Shelly Pro](shelly-pro.md) | Modules LAN et Wi-Fi sur rail DIN, API ouverte | Entrées locales par module, fonctionne sans contrôleur |
| [ESPHome sur rail DIN](esphome-rail-din.md) | Open source, matériel et logiciel | La voie « maison » la moins chère, à comparer à la refonte Raspberry Pi des V1 |
| [Modbus et passerelle](modbus-es.md) | Modules d'E/S Modbus (RTU ou TCP) pilotés par la passerelle, protocole ouvert | La forme concrète du « serveur d'E/S léger » cité par la V2 |

Écartés : Revolution Pi, Arduino Opta et Raspberry Pi et Ethernet, déjà étudiés en V1 et rappelés comme repères ; Zigbee et Z-Wave sur rail DIN, sans fil, notés comme variante de Shelly ; Legrand MyHome et Hager coviva, gammes en transition ; Beckhoff, proche de Wago et plus cher.

## Tableau comparatif

Lecture « seule », configuration résiliente, puis coût de la couche en dérivation. Les coûts sont HT, matériel et licence compris, hors électricien ; « hors… » signale un poste sans prix trouvé. Le détail, les sources et les réserves sont dans chaque dossier.

| Solution | Règle 1 | Causes communes (résiliente / minimale) | Pire panne simple | Armoire complète (résiliente / minimale) | Couche en dérivation | Rail | Ouverture |
| --- | --- | --- | --- | --- | --- | --- | --- |
| [KNX TP](knx.md) | Non tenue | **0** / 3 | Une zone ; éclairages gardent leur état | ≈ 5 200 / 2 950 € | ≈ 3 100 € | 2,2 m | Norme ouverte, 500 fabricants, ETS payant |
| [Loxone](loxone.md) | Non tenue | **0** / 6 | Une zone ; état des relais non documenté | ≈ 6 700 / 3 900 € | ≈ 3 950 € | ≈ 2 m | Propriétaire, logiciel gratuit, vente « Partner » |
| [Niko Home Control II](niko-home-control.md) | Non tenue | **0 ou 1** / 6 ou 7 | Une zone ; Internet « requis » selon la doc | ≈ 9 200 / 7 600 € | ≈ 8 100 € | ≈ 2,4 m | Propriétaire, API MQTT locale à jeton annuel |
| [Domintell](domintell.md) | Non tenue, **hors contrainte** (entrées à 10 m) | **6** / 6 | Toute la maison | ≈ 7 530 / 6 190 € | ≈ 5 570 € | ≈ 2,3 m | Propriétaire, Light Protocol documenté |
| [Homematic IP Wired](homematic-ip-wired.md) | Non tenue | **4** (0 si liaisons directes sans centrale) / 7 | Toute la maison ou une zone, selon ce point | ≈ 3 510 / 2 630 € | ≈ 2 480 € | 1,65 m | Propriétaire, centrale libre OpenCCU |
| [Eltako Series 14](eltako-series-14.md) | Non tenue | **0** / 3 | Une zone ; ses éclairages s'éteignent | ≈ 2 100 / 1 800 € | ≈ 1 600 € | ≈ 1 m | Propriétaire, un fabricant, outil gratuit |
| [Siemens LOGO! 8](siemens-logo.md) | Non tenue | **0** / 5 | Une zone ; relais retombent | ≈ 1 900 / 1 600 € | ≈ 1 600 € | 1,3 m | Propriétaire, Modbus TCP |
| [Wago PFC200](wago-pfc200.md) | Non tenue | **5** / 6 | Toute la maison ; repli à zéro en 50 ms | ≈ 6 500 / 6 250 €, hors alim et relais | ≈ 6 350 € | ≈ 0,7 m | Ouvert (Modbus, MQTT, CODESYS) |
| [Shelly Pro](shelly-pro.md) | **Partielle**, à confirmer ; 63 relais d'interface | **0** / 0 | Un module : 4 circuits | ≈ 2 270 € les deux, hors relais d'interface | ≈ 1 940 € | 1,1 m | API locale ouverte, cloud facultatif |
| [ESPHome sur rail DIN](esphome-rail-din.md) | **Partielle**, par carte | **0** (2 sans réglages) / 2 | Une zone ; relais à zéro au redémarrage | ≈ 1 100 € les deux, hors alim | ≈ 360 € | 3 × 320 mm, hors rail | Open source, CE radio seulement |
| [Modbus et passerelle](modbus-es.md) | Non tenue | **3** en RTU, 4 en TCP / 6 | Toute la maison (passerelle) | ≈ 1 190 / 1 073 € | **≈ 430 €** (Waveshare) ; ≈ 3 000 à 3 900 € en industriel | 1,9 m | Protocole ouvert, libre de droits |

Repères, avec les chiffres du conseil d'autocritique dans leur colonne, **non comparables** au décompte ci-dessus :

| Repère | Règle 1 | Modes communs (méthode du conseil) | Matériel HT |
| --- | --- | --- | --- |
| [V2 filaire d'abord](../v2/filaire-d-abord.md) | **Tenue** | 0 | ≈ 3 450 à 3 950 € (filaire seul), 6 450 à 7 850 € (avec domotique complète) |
| [Revolution Pi](../revolution-pi.md) (V1) | Non tenue | 13 | ≈ 5 450 € |
| [Arduino Opta](../arduino-opta.md) (V1) | Non tenue | 5 | ≈ 5 600 € |
| [Raspberry Pi et Ethernet](../raspberry-pi-ethernet.md) (V1) | Non tenue | 4 | ≈ 3 160 € |

## Classement : seule face à l'exigence

Aucune des onze solutions ne tient la règle 1 : le bouton qui commande seul sa charge. Le classement mesure la distance qui reste, par ce qu'il faut pour priver la maison de ses boutons et par ce que garde un circuit quand sa commande meurt.

1. **Shelly Pro** : la liaison entrée → relais vit dans le firmware de chaque module ; aucune défaillance unique ne touche toute la maison, un module mort prive quatre circuits. Mais l'état et le verrouillage des volets sont logiciels, l'isolement n'est pas publié, et il faut un relais d'interface par poussoir pour garder les nappes en TBTS. « Partielle, à confirmer ».
2. **ESPHome sur rail DIN** : même logique locale, une carte par zone, le prix le plus bas ; mais un micrologiciel du projet dans l'armoire, des relais à zéro au redémarrage, un marquage CE qui ne couvre que la radio et aucun isolement publié. C'est la refonte Raspberry Pi des V1 en moins cher et moins propre.
3. **KNX TP** : la meilleure architecture à bus. Zéro cause commune par zone, des relais bistables qui gardent l'état, des manettes mécaniques sur certains actionneurs, une norme à 500 fabricants. Une zone tombe avec son alimentation.
4. **Eltako Series 14** : zéro cause commune par zone, compact et bon marché, mais la perte du 12 V d'une zone éteint ses lumières ; fabricant unique.
5. **Siemens LOGO! 8** : zéro cause commune avec cinq unités autonomes, mais les relais retombent à l'arrêt, les entrées 230 V ne sont pas isolées, et il n'y a ni variateur ni verrouillage natif.
6. **Loxone** : zéro cause commune avec un Miniserver par zone, au prix fort ; l'état des relais à la perte du Link n'est pas documenté et rien n'est manœuvrable à la main.
7. **Niko Home Control II** : à contre-emploi (trois entrées par module, un contrôleur par installation) et une dépendance à Internet que sa documentation affirme.
8. **Homematic IP Wired** : zéro ou quatre causes communes selon que les liaisons directes filaires tiennent sans centrale, ce que le terrain contredit ; entrées non isolées qui portent le 24 V du bus sur les nappes.
9. **Modbus et passerelle** : la passerelle, son Linux et son logiciel sont sur le chemin de chaque appui : 3 à 4 causes communes.
10. **Wago PFC200** : contrôleur unique, coupleurs sans logique, repli à zéro en 50 ms : 5 causes communes, au prix le plus élevé avec Niko.
11. **Domintell** : hors contrainte (entrées limitées à 10 m), maître unique, 6 causes communes.

Ce que dit ce classement : les solutions qui s'approchent de l'exigence le font en mettant **un microcontrôleur par poussoir ou par zone**, pas en le supprimant. La V2 reste la seule réponse qui tient la règle 1.

## Recommandation : en dérivation sur le filaire V2

En dérivation, la couche domotique n'a plus qu'à fermer des contacts secs en parallèle des poussoirs, lire des recopies, battre le cœur du relais de garde et parler à la passerelle. Les critères qui comptent changent : prix pour ≈ 85 sorties et ≈ 70 entrées, ouverture du protocole, place, et rien du projet qui tourne dans l'armoire.

| Rang | Solution | Couche HT | Pour | Contre |
| --- | --- | --- | --- | --- |
| 1 | **Modbus et passerelle** (serveur d'E/S léger) | ≈ 430 € en Waveshare ; ≈ 3 000 à 3 900 € en Advantech ou Seneca | Aucune logique dans l'armoire, protocole ouvert et libre, chien de garde de communication sur les modules industriels, la passerelle fait tout | Isolement et CE des modules bon marché non trouvés ; Waveshare sans chien de garde ; un maître unique, acceptable pour une couche sacrifiable |
| 2 | **KNX TP** | ≈ 3 100 € | Norme, 500 fabricants, pièces à dix ans, aucun Linux ni logiciel du projet sur le chemin des contacts, minuterie d'actionneur en battement de cœur | ETS à acheter et apprendre ; 88 modules ; relais 16 A surdimensionnés |
| 3 | **Eltako Series 14** | ≈ 1 600 € | Compact (0,75 m), sans licence, fabricant des variateurs de la V2 | Propriétaire, un seul fabricant, liaison série, pas de bibliothèque Go |
| 4 | **Homematic IP Wired** | ≈ 2 480 € | Peu de modules, centrale libre, sans cloud | Entrées non isolées, battement de cœur à travers centrale et réseau |
| 5 | **Siemens LOGO! 8** | ≈ 1 600 € | Relais isolés qui s'ouvrent à l'arrêt, Modbus TCP | Entrées non isolées en 230 V, version 24 V sans prix, génération n−1 |
| 6 | **Shelly Pro** | ≈ 1 940 € | Bon marché, API locale | Relais qui commutent la phase, 22 micrologiciels, isolement non publié |
| 7 | **ESPHome sur rail DIN** | ≈ 360 € | Le moins cher | Micrologiciel du projet, CE radio seulement, hors rail DIN |
| — | Loxone, Niko, Domintell, Wago | ≈ 3 950 à 8 100 € | | Trop chers pour le service rendu, ou contrôleur propriétaire sur le chemin des contacts |

**Recommandation** : pour la couche domotique de la V2, chiffrer en premier le **serveur d'entrées-sorties Modbus** piloté par la passerelle, avec des modules à chien de garde de communication et un isolement attesté, en demandant un devis en modules industriels ; garder **KNX** comme option si l'on préfère une norme reprise par n'importe quel intégrateur à un logiciel maison, au prix d'ETS et de 1,6 m de rail. La Revolution Pi Connect 5 (≈ 581 € HT nue, plus ses modules) reste la troisième voie, celle de la V1. Le choix revient à l'exploitant ; cette étude ne modifie pas la V2.

## Réserves

- Les chiffres viennent de fiches techniques, de boutiques en ligne et de retours d'utilisateurs consultés en octobre 2026. Ce sont des estimations, à confirmer par un électricien, des devis, les fabricants et des essais.
- Les comportements en panne sont ceux que la documentation des fabricants décrit ou que des utilisateurs rapportent ; aucun n'a été essayé sur un banc dans cette étude.
- Les études V1 et la V2 ne sont pas modifiées par cette étude. Un point qui les toucherait est signalé ici, pas appliqué.
