---
title: "Solutions du marché : remplacer l'armoire sans recâblage"
description: "KNX et dix autres solutions domotiques (Loxone, Niko, Domintell, Homematic IP Wired, Eltako Series 14, Siemens LOGO!, Wago, Shelly Pro, ESPHome, modules Modbus) évaluées pour remplacer l'armoire ESSENSYS sans toucher aux fils des poussoirs ni des charges : seules face à l'exigence de résilience, puis en couche domotique sur le filaire V2."
---

# Solutions du marché : remplacer l'armoire sans recâblage

La V2 « [filaire d'abord, domotique en dérivation](../v2/filaire-d-abord.md) » répond à l'[exigence de résilience](../../resilience.md) avec des télérupteurs, des relais et des variateurs à entrée locale, et laisse ouvert le choix de la couche domotique. Avant de s'engager, une question se pose : une solution domotique du marché, KNX en tête, pourrait-elle remplacer les quatre cartes de l'armoire **sans toucher au câblage existant** ? Et comment une dizaine de solutions, ouvertes, payantes ou issues de l'automatisme, se comparent-elles sur les mêmes critères ?

Cette étude répond en onze dossiers écrits au même gabarit, puis dans un tableau comparatif. Elle a été relue par un relecteur indépendant. Ses chiffres sont des estimations d'octobre 2026, à confirmer par un électricien, des devis, les fabricants et des essais.

!!! abstract "En bref"
    <!-- À compléter après les onze dossiers : réponse courte à « KNX peut-il remplacer l'armoire ? », classement seule, recommandation en dérivation. -->
    À compléter.

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

<!-- À compléter après les onze dossiers. -->
À compléter.

## Classement : seule face à l'exigence

<!-- À compléter. -->
À compléter.

## Recommandation : en dérivation sur le filaire V2

<!-- À compléter. -->
À compléter.

## Réserves

- Les chiffres viennent de fiches techniques, de boutiques en ligne et de retours d'utilisateurs consultés en octobre 2026. Ce sont des estimations, à confirmer par un électricien, des devis, les fabricants et des essais.
- Les comportements en panne sont ceux que la documentation des fabricants décrit ou que des utilisateurs rapportent ; aucun n'a été essayé sur un banc dans cette étude.
- Les études V1 et la V2 ne sont pas modifiées par cette étude. Un point qui les toucherait est signalé ici, pas appliqué.
