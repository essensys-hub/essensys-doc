---
title: "Modbus et passerelle : remplacer l'armoire sans recâblage"
description: "Des modules d'entrées-sorties Modbus RTU ou TCP sur rail DIN, interrogés directement par la passerelle Raspberry Pi CM5 qui devient le maître, pour remplacer les quatre cartes de l'armoire ESSENSYS sans toucher aux fils. Seule, toute la logique est dans la passerelle, cause commune unique ; en dérivation, c'est la forme concrète du serveur d'entrées-sorties léger de la V2 et la couche domotique la moins chère du comparatif. De l'ordre de 700 à 820 € HT en armoire complète, 430 € HT en couche domotique seule."
---

# Modbus et passerelle

Modbus est le protocole d'automatisme le plus ancien encore en service : ouvert, sans redevance, porté par des centaines de fabricants de modules d'entrées-sorties. Ce dossier du [comparatif](index.md) regarde la forme la plus dépouillée qu'une armoire puisse prendre : des modules sans logique, un bus RS-485 ou un réseau Ethernet dans le coffret, et la passerelle Raspberry Pi CM5 existante, avec son backend Go, comme **maître unique**. Aucun automate, aucun serveur domotique entre les deux. C'est la forme concrète du « serveur d'entrées-sorties léger » que la V2 cite comme candidat pour sa couche domotique.

!!! abstract "Synthèse"
    - **Seule** : des modules Waveshare à 8 entrées et 8 relais reprennent les 63 poussoirs et ≈ 70 relais sans changer un fil, pour ≈ 705 à 820 € HT, variateurs compris. Mais chaque appui traverse la passerelle, son Linux et son logiciel : **règle 1 non tenue**. Le maître est unique quel que soit le découpage : en configuration par zone (un segment RS-485, une alimentation par zone), **3 défaillances uniques privent toute la maison** de ses boutons, le contrôleur, son logiciel figé et une mise à jour ratée ; 4 en variante TCP, avec le commutateur ; 6 en configuration minimale. Les modes locaux de certains modules (bascule ou recopie entrée → relais dans le module) peuvent ramener ce compte à 0, à confirmer au banc.
    - **En dérivation** : la couche domotique la moins chère du comparatif, **≈ 430 € HT** pour 88 sorties et 88 entrées en RTU, sans aucune logique dans l'armoire, avec la passerelle comme seul cerveau et comme émetteur du battement de cœur. La fonction clé est le chien de garde de communication qui ouvre les relais quand le maître se tait : présent chez Seneca, Advantech, ICP DAS, Wago et Wiren Board, **absent chez Waveshare**, où seule une impulsion à durée bornée en tient lieu. Les variantes industrielles coûtent 3 000 à 6 600 € HT.
    - **Coût estimé** : ≈ 705 € HT en configuration minimale RTU, ≈ 820 € HT par zone, ≈ 430 € HT en couche domotique seule ; variante TCP non chiffrée en armoire complète. Les variateurs EUD12D-UC sont comptés au prix boutique de 43,45 € HT retenu par la V2, le prix catalogue Eltako (89,37 € HT) restant en note. Prix d'octobre 2026, boutiques allemandes et fabricants, TTC convertis en HT à 19 %.
    - **Réserve** : estimations à confirmer par un électricien, des devis, les fabricants et des essais. Aucune tension d'isolement ni marquage CE trouvés pour les modules Waveshare ; le comportement de leurs relais au démarrage n'est pas documenté.

## Principe et gamme

Modbus a été publié par Modicon en 1979 ; les droits sont passés à Schneider Electric en 1997, puis en 2004 à la Modbus Organization, qui le tient « ouvert et sans redevance ». Le modèle est simple : un **maître** interroge des **esclaves** adressés, lit des entrées (fonction 02), écrit des sorties ou « coils » (05, 15) et des registres (06, 16). Deux transports :

- **Modbus RTU** : trames binaires avec CRC sur une ligne série RS-485 à deux fils et un commun ; 32 appareils sans répéteur, 1 000 m à 9 600 bauds, dérivations de 20 m au plus, 247 adresses par ligne ;
- **Modbus TCP** : même modèle de données sur Ethernet, port 502, un module ou un coupleur par adresse IP, en étoile à travers un commutateur.

Le système est **centralisé** : lecture des poussoirs, commande des relais, verrouillage des volets, minuteries et scénarios sont dans le logiciel du maître. Les modules n'ont pas de logique entre eux, à trois exceptions : les modes « linkage », « toggle » et « edge » des Waveshare à entrées et relais, la logique graphique GCL des Advantech ADAM-6000, et les réponses aux appuis configurables des Wiren Board.

Fabricants retenus pour chiffrer : Waveshare (Chine, le moins cher), Seneca (Italie), Advantech et ICP DAS (Taïwan), Wago (Allemagne), Wiren Board (origine à vérifier), Phoenix Contact et DEHN pour les parafoudres ; Eltako pour les variateurs.

## Dans l'armoire sans recâblage

Les poussoirs sont des contacts secs : les entrées optocouplées des modules les lisent, en fournissant elles-mêmes la boucle (Waveshare, Seneca, Advantech, ICP DAS) ou avec une boucle 24 V prise sur l'alimentation de l'armoire (Wago). Le bus reste dans l'armoire ; seules les nappes parcourent la maison, comme aujourd'hui.

| Fonction | Module | Voies | Largeur | Ce qu'il faut savoir |
| --- | --- | --- | --- | --- |
| 63 poussoirs | Waveshare Modbus RTU Relay (D) | 8 entrées 5 à 36 V, optocoupleur bidirectionnel, et 8 relais 10 A | 175 × 90 × 40 mm, boîtier ABS « rail-mounted » | Entrée passive si la borne DI COM reste libre ; antirebond intégré ; tension d'isolement en kV **non publiée** ; marquage CE non trouvé |
| | Waveshare Modbus RTU IO 8CH | 8 entrées et 8 sorties transistor 500 mA | cotes non trouvées | Même électronique d'entrée ; fusibles réarmables et TVS |
| | Seneca ZC-16DI-8DO | 16 entrées auto-alimentées 16 V | 35 mm | 1,5 kV CA trois voies ; support de bus obligatoire |
| | Advantech ADAM-4051 | 16 entrées, contact sec vers DGND | non trouvée | 2 500 V CC |
| | Wago 750-1405 (TCP via coupleur 750-362) | 16 entrées 24 V, filtre 3 ms | 12 mm | 500 V entre système et terrain ; boucle 24 V à câbler |
| 25 éclairages | Relais des Waveshare Relay (D), 16CH ou 32CH | 8, 16 ou 32 relais 10 A 250 V, un NO et un NC | 175, 200 ou 300 mm | Le 16CH ne s'alimente qu'en 5 V ; le 32CH en 7 à 36 V, 11,7 W relais collés ; marque et endurance des relais non indiquées |
| | Wago 750-517 ; Advantech ADAM-4068 | 2 inverseurs 1 A ; 8 relais 0,25 A à 240 V | 12 mm ; non trouvée | Pour des bobines seulement : relais d'interface obligatoires devant toute charge 230 V |
| 15 volets dont le store | Deux relais par volet | 30 relais | | Aucun module « volet » Modbus trouvé ; verrouillage des deux sens **logiciel**, ou câblé en croisant les contacts NO et NC ; le « flash-on / flash-off » Waveshare borne une marche de 0,1 s à ≈ 54 min sans le maître |
| 8 variateurs | Eltako EUD12D-UC commandé par un relais | 1 par lampe, 400 W | 18 mm | Entrée universelle 12 à 230 V isolée ; appui court allume, appui long varie ; le poussoir existant **peut rester câblé en parallèle** du relais Modbus sur son entrée |
| | Wiren Board WB-MDM3 (RTU) | 3 voies 300 W, 6 entrées poussoir | 3 modules | Variateur Modbus natif ; origine et conformité UE à vérifier |
| Fil pilote, cumulus, prises, arrosage, machines | Relais 10 A des mêmes modules | ≈ 7 | | Fil pilote à quelques mA ; cumulus par son contacteur |
| Maître | Raspberry Pi CM5 et convertisseur USB-RS485 isolé Waveshare 15817 | 1 par segment | | Isolation magnétique et TVS, kV non publié ; une version à 4 ports isolés existe, prix non relevé |
| Alimentation | Mean Well HDR-60-24 | 60 W | rail DIN | ≈ 25 W pour 72 relais collés, extrapolé du 16CH |
| Parafoudre RS-485 | Phoenix Contact DT-UFB-485/BS ou MT-RS485 ; DEHN BXT ML4 BE BD 24 | | | Facultatif, le bus ne sort pas du coffret ; prix DEHN non obtenu |

Aucun module n'a de bouton de commande manuelle en face avant, seulement des voyants. La longueur de nappe admise sur les entrées n'est publiée par aucun fabricant.

### Configuration minimale

Un bus RS-485, une alimentation : **neuf Waveshare Relay (D)**, soit 72 entrées et 72 relais pour 63 poussoirs et ≈ 70 relais (25 éclairages, 30 volets, 8 impulsions de variateurs, ≈ 7 divers) ; huit EUD12D-UC ; un convertisseur USB-RS485 isolé sur le CM5 ; une HDR-60-24. Une seule référence de module. **≈ 1,75 m** de rail : 9 × 175 mm de boîtiers Waveshare et 8 × 18 mm d'Eltako. Variante plus compacte en deux références : deux Relay 32CH (600 mm) et huit IO 8CH (cotes non publiées).

### Configuration résiliente

**Un segment RS-485, un convertisseur isolé et une alimentation par zone**, plus un module pour les fonctions communes :

| Zone | Entrées | Relais | Modules Relay (D) |
| --- | --- | --- | --- |
| Pièces de vie (20 poussoirs, 5 éclairages, 6 volets, 3 variateurs) | 20 | 20 | 3 |
| Chambres (21, 7, 5, 4) | 21 | 21 | 3 |
| Pièces d'eau (22, 13, 4 dont le store, 1) | 22 | 22 | 3 |
| Commun (fil pilote, cumulus, prises, arrosage, machines) | — | ≈ 7 | 1 |

**Dix Relay (D), trois convertisseurs, trois alimentations, ≈ 1,9 m de rail.** Le découpage isole les pannes de bus et d'alimentation, pas celle du maître : la gamme ne permet pas un contrôleur par zone sans ajouter un automate, ce qui serait une autre solution. Un segment en défaut, un convertisseur grillé ou une alimentation morte ne touchent que leur zone ; le CM5 reste au bout des trois segments.

**Variante Modbus TCP** : un coupleur Wago 750-362 par zone (409 € HT) avec deux bornes 750-1405 (32 entrées) et des bornes relais, ou un Waveshare Modbus POE ETH Relay 30CH par zone (70 $) avec des IO 8CH PoE ; un commutateur Ethernet commun, PoE pour Waveshare. Le 750-517 ne commute que 1 A : la borne relais 16 A Wago et son prix n'ont pas été trouvés, et le prix de l'IO 8CH PoE n'a pas été relevé. La variante TCP n'est donc pas chiffrée en armoire complète. Elle isole mieux chaque module qu'un bus multipoint, et ajoute le commutateur comme cause commune.

<!-- schemas:fritzing:debut -->
### Câblage d'un poussoir à une charge (Fritzing)

![Câblage coloré de gauche à droite. Un poussoir mural envoie son contact sec (jaune) à une entrée d'un module Waveshare Modbus RTU Relay (D), alimenté en 24 V par une Mean Well HDR-60-24 (rouge pour le 24 V, noir pour le 0 V). Le module, dessiné en deux blocs, entrées puis relais, est relié par deux fils bleus au segment RS-485 de la zone. Le même segment est relié, par deux autres fils bleus, à un convertisseur USB-RS485 isolé, lui-même relié en violet à la passerelle Essensys, maître unique. Le relais reçoit la phase du secteur (marron) et la renvoie par sa sortie NO à une lampe, qui reçoit aussi le neutre (bleu clair).](fritzing/modbus-es_breadboard.png){ loading=lazy }

Une zone, une lampe, avec les modules de la configuration résiliente. Source Fritzing : [modbus-es.fzz](fritzing/modbus-es.fzz){ download="modbus-es.fzz" } (Fritzing 1.0.x). Principe de câblage, non validé au banc.
<!-- schemas:fritzing:fin -->

## Seule face à l'exigence

<!-- schemas:seule:debut -->
<iframe src="../archify/modbus-es-seule.html?embed=1&amp;theme=light" title="Diagramme d'architecture interactif : Modbus RTU seul, le maître unique sur le chemin de chaque appui, un segment par zone" loading="lazy" style="width:100%;aspect-ratio:1230/488;height:auto;border:0"></iframe>

[Ouvrir le diagramme en plein écran](archify/modbus-es-seule.html){ target="_blank" rel="noopener" }. Le poussoir attaque un module Relay (D) ; le contact remonte par le segment RS-485 et le convertisseur jusqu'à la passerelle, maître unique, qui décide et renvoie l'ordre par le même chemin au relais ; l'alimentation 24 V arrive par le haut.

??? info "Image fixe du diagramme"
    ![Capture du diagramme d'architecture. De gauche à droite : 63 poussoirs muraux, module Waveshare Relay (D), segment RS-485, convertisseur USB, passerelle Essensys. Entre le module et la passerelle, chaque liaison est doublée : lecture des entrées en fonction 02 dans un sens, écriture des coils en fonction 05 dans l'autre. Le module commande en dessous les charges de la zone. Au-dessus du module, l'alimentation 24 V ; au-dessus de la passerelle, les deux autres zones, reliées par USB. Le cadre « Une zone » enveloppe le module, le segment, le convertisseur et l'alimentation. Quatre cartes : règle 1 non tenue, ce qui reste panne par panne, causes communes, réserve.](archify/modbus-es-seule.png){ loading=lazy }
<!-- schemas:seule:fin -->

### Les sept règles

Les [sept règles](../../resilience.md#pour-toutes-les-installations-essensys) de la réponse de résilience, lues sur la configuration résiliente RTU :

| Règle | Tenue | Pourquoi |
| --- | --- | --- |
| 1. Pas de calculateur entre le bouton et sa charge | **Non tenue** | Le module lit le contact, le CM5 l'interroge, décide et écrit le coil : Linux, Go et un bus série sont sur le chemin de chaque appui. Exceptions : les voies Waveshare en mode « toggle » (bascule à chaque impulsion, télérupteur logiciel dans le module) ou « linkage » (le relais suit l'entrée), les Wiren Board et la logique GCL des ADAM-6000 atteignent « partielle, à confirmer » ; les 8 variateurs atteignent « tenue » si le poussoir reste câblé en parallèle sur l'EUD12D |
| 2. L'état vit dans un organe bistable | Non tenue | Relais monostables ; l'état vit dans le maître. Au retour du courant, un Waveshare « ne revient pas à son état précédent » (avis client) ; ICP DAS et Wiren Board offrent une valeur au démarrage réglable ; Waveshare ne documente rien |
| 3. La domotique ajoute, ne retire jamais | Non tenue | La passerelle **est** la domotique : un coil faux ou piraté commute n'importe quelle voie ; le verrouillage des volets est logiciel, sauf croisement NO / NC câblé |
| 4. Une source et un fusible par zone, un fusible pour la domotique | Partielle | Une alimentation et un segment par zone, oui ; mais entrées et relais partagent le module et son alimentation, sans fusible qui sépare les boutons de la domotique |
| 5. Barrière 4 kV et 8 mm, 0 V jamais au PE, parafoudres hors coffrets | Non tenue | Les nappes arrivent sur des entrées isolées à 1,5 kV CA (Seneca), 2 à 3,75 kV CC (Advantech, ICP DAS), 500 V (Wago) ou non chiffrées (Waveshare) : aucune n'atteint 4 kV. La spécification Modbus série veut le commun du bus **relié à la terre de protection** en un point, à l'opposé de la règle V2 |
| 6. Replis choisis au câblage, essayés à la recette | Partielle | Chien de garde de communication et état sûr se règlent par registre chez Seneca, Advantech ADAM-6000, ICP DAS, Wago et Wiren Board, pas dans le câblage ; rien de tel chez Waveshare, où seule la durée bornée du flash-off agit sans maître |
| 7. Isolement mesuré chaque année | Tenue | Rien ne l'empêche ; bornes à vis, modules démontables |

### Les causes communes

Dans la configuration résiliente RTU, avec la logique dans la passerelle :

| Défaillance unique | Prive de ses boutons… | Pourquoi |
| --- | --- | --- |
| 1. Alimentation du système ou du bus | une zone | Une alimentation 24 V par segment ; les relais de la zone retombent, ses entrées se taisent |
| 2. Court-circuit ou ligne collée sur un bus | une zone | Un port RS-485 d'esclave en défaut « peut faire tomber tout le bus », rapportent les utilisateurs ; un esclave hors tension, lui, reste en haute impédance. Un segment par zone borne la panne |
| 3. Contrôleur central | **toute la maison** | Le CM5 est le seul maître : carte SD, alimentation, processeur, port USB |
| 4. Logiciel figé | **toute la maison** | Le processus Go figé n'interroge plus rien ; sans chien de garde Waveshare, les relais gardent leur dernier état, un éclairage reste allumé, un volet lancé court jusqu'à son flash-off ou sa fin de course |
| 5. Mise à jour ratée | **toute la maison** | Système ou application de la passerelle ; le micrologiciel des Waveshare n'est pas mis à jour (version en lecture seule) |
| 6. Licence, compte ou cloud | rien | Aucun chez aucun fabricant cité ; bibliothèques libres |
| 7. Commutateur ou routeur | rien | Hors du chemin en RTU ; **toute la maison en TCP**, le commutateur étant entre le maître et chaque module |
| 8. Foudre sur le chemin du bus | une zone | Le bus reste dans l'armoire ; l'onde entre par la nappe de la zone sur les entrées de son module, séparées du RS-485 par une isolation magnétique non chiffrée ; le convertisseur isolé protège le CM5, en kV non publié |

**Total : 3 défaillances uniques privent toute la maison** en RTU, **4** en TCP, 3 privent une zone. En configuration minimale, l'alimentation unique, le court-circuit du bus unique et la foudre s'y ajoutent : **6**. Avec les modes locaux Waveshare, éclairages en « toggle » et volets en « linkage » sur les mêmes voies, les défaillances 3, 4 et 5 ne privent plus ces voies : **0**, à confirmer, car le comportement de ces modes au redémarrage n'est pas documenté, et un client rapporte des relais restés « liés » jusqu'au retour en mode normal.

Ce décompte est celui des V1 : un calculateur sur le chemin du bouton, un découpage en zones qui arrête les pannes indépendantes et pas la cause commune. La passerelle est aujourd'hui une couche d'application ; la mettre sur le chemin de chaque appui change sa nature.

### Ce qui reste, panne par panne

| Panne | Ce qui reste |
| --- | --- |
| Passerelle arrêtée, figée ou en mise à jour | Aucun bouton, sauf voies en mode local et variateurs à poussoir parallèle ; relais Waveshare dans leur dernier état ; relais à chien de garde (Seneca, ICP DAS, Wago, Wiren Board) à l'état sûr après le délai réglé ; EUD12D gardent leur niveau |
| Segment, convertisseur ou alimentation d'une zone | Les deux autres zones ; dans la zone touchée, relais retombés (alimentation) ou figés (bus), aucun bouton, aucune commande manuelle sur les modules |
| Commutateur (TCP) | Aucun bouton, mêmes états de relais |
| Coupure du secteur | Au retour, relais Waveshare non documentés, « pas l'état précédent » selon un client ; valeur au démarrage réglable chez ICP DAS et Wiren Board ; la passerelle relit tout et rétablit |
| Un module | Ses 8 voies ; échange et réadressage par commande, aucun DIP sur Waveshare |
| Foudre par une nappe | Le module de la zone au pire ; les autres par les isolations magnétiques, non chiffrées |

## En dérivation sur le filaire V2

<!-- schemas:derivation:debut -->
<iframe src="../archify/modbus-es-derivation.html?embed=1&amp;theme=light" title="Diagramme d'architecture interactif : Modbus RTU en dérivation sur le filaire V2" loading="lazy" style="width:100%;aspect-ratio:1260/680;height:auto;border:0"></iframe>

[Ouvrir le diagramme en plein écran](archify/modbus-es-derivation.html){ target="_blank" rel="noopener" }. En bas, le filaire V2 : source 24 V, poussoirs, télérupteur, lampe. En haut, la couche Modbus : passerelle qui bat le chien de garde, convertisseur, bus RS-485, modules Relay (D), relais de garde, relais de couplage en parallèle du poussoir, relais de recopie et entrées qui relisent l'état.

??? info "Image fixe du diagramme"
    ![Capture du diagramme d'architecture. Cadre du bas « Filaire V2 » : source 24 V de zone, poussoirs muraux, télérupteur Finder 20.22, lampe. Cadre du haut « Couche domotique Modbus » : convertisseur USB, bus RS-485, modules Relay (D) en sorties, relais de garde, relais de couplage, modules Relay (D) en entrées et relais de recopie ; la passerelle Essensys, hors du cadre, est reliée au convertisseur. Les modules envoient une impulsion flash-on au relais de garde et commandent la bobine du relais de couplage, qui ferme un contact sec en parallèle des poussoirs ; le second contact du télérupteur remonte par le relais de recopie jusqu'aux entrées. Quatre cartes : si la couche tombe, ce qu'elle apporte, ce qu'elle coûte, réserve.](archify/modbus-es-derivation.png){ loading=lazy }
<!-- schemas:derivation:fin -->

Dans cette lecture, les télérupteurs, les chaînes de volets et les variateurs à entrée locale de la [V2](../v2/filaire-d-abord.md) gardent le chemin du bouton ; les modules Modbus ne font que fermer des contacts secs et lire des recopies, et c'est exactement le « serveur d'entrées-sorties léger » de la V2.

- **Sorties** : les relais 10 A des modules commandent les bobines 24 V des relais de couplage 38.51 de la V2, qui ferment les contacts en parallèle des poussoirs ; 88 relais en onze Relay (D), ou 96 en trois 32CH, pour ≈ 85 sorties.
- **Entrées** : les contacts secs des relais de recopie 38.51 se ferment sur des entrées passives, le module fournissant la boucle ; 88 entrées en onze Relay (D), ou 72 en neuf IO 8CH, pour ≈ 70 recopies.
- **Battement de cœur** : c'est **la passerelle qui réarme** le relais de garde. Avec des Waveshare, sans chien de garde, le seul mécanisme qui agit quand le maître se tait est le « flash-on » : la passerelle commande sur une voie une impulsion de durée T et la renouvelle avant son terme ; si elle se tait, le contact retombe seul au bout de T et la bobine du relais de garde lâche ; le chien de garde matériel de la V2 reste en place derrière. Avec un module à chien de garde de communication (Seneca Z-10-D-OUT, ICP DAS, Wago, Wiren Board), le module lui-même ouvre la voie de garde après le délai réglé, 10 s au moins chez Seneca. Dans tous les cas, passerelle muette veut dire couche débranchée en moins d'une seconde côté V2, sans rien de plus à écrire.
- **Logique** : toute dans la passerelle, en Go ; aucune dans l'armoire. Scrutation des entrées en fonction 02, fronts, appui long et double appui côté passerelle sur les recopies des poussoirs, écriture des coils, surveillance des délais, journal.
- **Durées bornées** : par le câblage de la V2 ; le flash-off Waveshare peut doubler la borne par voie, sans que la V2 en dépende.

Ce que la couche apporte : **≈ 430 € HT** en RTU Waveshare, le total le plus bas du comparatif et le repère des autres dossiers ; un protocole que n'importe quel module d'un autre fabricant remplace au prix d'une adaptation du pilote Go ; aucune licence, aucun compte, aucun Linux de plus que celui de la passerelle. Ce qu'elle coûte : ≈ 1,9 m de boîtiers Waveshare en Relay (D), soit un coffret de plus, ou ≈ 0,6 m en 32CH plus des IO 8CH aux cotes inconnues ; aucune tension d'isolement ni marquage CE publiés chez Waveshare, ce que les 38.51 (6 kV) de la V2 rendent acceptable de part et d'autre ; un travail Go à écrire, mais sans intégrateur ni outil propriétaire. À comparer à la Revolution Pi Connect 5 (≈ 581 € HT nue, modules d'entrées-sorties non chiffrés ici) ; Modbus RTU n'ajoute aucun calculateur à la passerelle. En matériel industriel, la même couche vaut ≈ 3 010 € HT en Advantech, ≈ 3 860 € HT en Seneca, ≈ 6 600 € HT en Wago TCP : du prix de KNX (≈ 3 100 € HT), avec des isolements chiffrés et des chiens de garde intégrés.

## Foudre et isolement

- **Le bus reste dans l'armoire** : les poussoirs restent des contacts secs sur leurs nappes, aucun câble RS-485 ni Ethernet ne sort du coffret. Les nappes, elles, restent des antennes, et arrivent sur les entrées des modules.
- **Tensions d'essai** : Seneca 1,5 kV CA (EN 61010-1), Advantech 2 500 V CC (série 4000) et 2 000 V CC (série 6000), ICP DAS 2 000 à 3 750 V CC avec surtension ±2 kV et transitoires ±4 kV sur l'alimentation, Wago 500 V, Eltako « entrées de commande isolées de l'alimentation et de la charge » sans valeur ; **Waveshare : « isolation d'alimentation, optocoupleurs, isolation magnétique du RS-485, fusibles réarmables et TVS », sans aucun kV**. Les convertisseurs USB-RS485 annoncent une isolation magnétique, et pour l'un « 15 kV ESD », qui est une tenue aux décharges, pas un isolement. La barrière de 4 kV et 8 mm de la V2 n'est tenue par aucun module : en dérivation, les 38.51 la fournissent ; seule, l'onde d'une nappe entre dans le module.
- **Mise à la terre du commun** : la spécification Modbus série demande que le commun du bus soit relié à la terre de protection, de préférence en un seul point ; la V2 interdit tout lien entre un 0 V et le PE. Les convertisseurs isolés permettent de garder l'îlot domotique flottant, mais le point est à arbitrer avec l'électricien et le spécialiste foudre.
- **Règles de ligne** : terminaison de 150 Ω, ou 120 Ω et 1 nF si le bus est polarisé ; polarisation de 450 à 650 Ω en un seul point, au maître ; jamais de terminaison sur une dérivation. Texas Instruments conseille l'isolement galvanique des émetteurs-récepteurs.
- **Parafoudres RS-485** : Phoenix Contact DT-UFB-485/BS (≈ 165 € HT, 5 kA par ligne, en D-SUB 9) ou MT-RS485 (336 € TTC, rail DIN) ; DEHN BLITZDUCTOR XT BXT ML4 BE BD 24, prix sous identifiant distributeur. Facultatifs tant que le bus ne sort pas du coffret.

## Logiciel, paramétrage et passerelle Essensys

| Point | Ce qu'on a trouvé |
| --- | --- |
| Outil | Aucun outil obligatoire : adresses et vitesse par registres (Waveshare, « pas de DIP, seulement par commande ») ou par DIP (Seneca) ; page web pour les Waveshare PoE, mot de passe par défaut « 123456 » ou absent ; utilitaire graphique Advantech pour la logique GCL ; outil Wago pour les coupleurs |
| Bibliothèques Go | goburrow/modbus : BSD-3, RTU, ASCII et TCP, client seulement, 1 000 étoiles, 79 commits, 41 problèmes ouverts, aucune version publiée ; simonvetter/modbus : MIT, RTU, TCP, TLS, UDP, client et serveur TCP, 456 étoiles |
| Python | pymodbus : BSD, série, TCP, TLS, UDP, 2 800 étoiles, version 3.16.1 |
| Home Assistant | Intégration Modbus : RTU, TCP, UDP, RTU sur TCP ; entités interrupteur, lumière, volet, capteurs ; scrutation par défaut toutes les 15 s, trop lente pour un poussoir ; un volet sur coil « ne connaît pas les états intermédiaires » |
| Travail côté passerelle | Boucle de scrutation des entrées (9 600 à 115 200 bauds, 8 entrées par trame), fronts, appui long, double appui, verrouillage des volets, minuteries, écriture des coils, battement de cœur, délais et reconnexion, journal ; aucun code Go fourni par les fabricants, démos Python, Arduino et STM32 chez Waveshare ; latence poussoir → relais sur 9 à 11 esclaves à mesurer au banc |
| Mise à jour | Micrologiciel des Waveshare non documenté ; Advantech conditionne P2P et GCL à une version de micrologiciel |
| Cloud, licence | Aucun ; protocole sans redevance |

La note ne chiffre pas le travail Go. La V2 compte 5 à 11 semaines-personne pour sa couche domotique, logique comprise, et ce dossier n'y ajoute pas de dépendance visible : les bibliothèques existent, les cartes de registres sont publiées, et rien ne se compile dans l'armoire.

## Nomenclature et coût estimé

Prix relevés le 24 octobre 2026 : Waveshare en dollars hors taxes sur sa boutique et en euros chez Eckstein (TTC à 19 %, converti en HT) ; convertisseur chez Welectron (TTC à 19 %) ; alimentation chez TME (HT) ; EUD12D-UC au prix boutique de 43,45 € HT (51,70 € TTC chez zaehlerschrank24, le prix retenu par la V2), le prix catalogue Eltako de 89,37 € HT étant rappelé en note ; matériel industriel chez RS, Farnell, Bürklin et Seneca, les deux références Wago au prix RS France du [dossier Wago](wago-pfc200.md). Hors port, droits, rail, coffret et câblage, déjà comptés par la V2.

### Configuration minimale

| Poste | Référence | Qté | Prix unitaire HT | Total HT | Source |
| --- | --- | --- | --- | --- | --- |
| Entrées et relais | Waveshare Modbus RTU Relay (D) | 9 | 35,25 € (41,95 € TTC) ; 34,99 $ chez le fabricant | 317 € | Eckstein, Waveshare |
| Variateurs | Eltako EUD12D-UC | 8 | 43,45 € (51,70 € TTC ; catalogue Eltako 89,37 € HT) | 348 € | zaehlerschrank24 |
| Maître | Convertisseur USB-RS485 isolé Waveshare 15817 | 1 | 22,61 € (26,90 € TTC) | 23 € | Welectron |
| Alimentation | Mean Well HDR-60-24 | 1 | 18,06 € | 18 € | TME |
| **Matériel** | | | | **≈ 705 € HT** | |
| Logiciel | Bibliothèques libres | | 0 € | 0 € | — |
| **Total** | | | | **≈ 705 € HT**, ≈ 1,75 m de rail | |

Avec un parafoudre RS-485 DT-UFB-485/BS (≈ 165 € HT), facultatif : ≈ 870 € HT. Au prix catalogue Eltako de l'EUD12D-UC (89,37 € HT), le total monterait à ≈ 1 073 € HT.

### Configuration résiliente

| Poste | Référence | Qté | Prix unitaire HT | Total HT |
| --- | --- | --- | --- | --- |
| Entrées et relais, trois zones et le commun | Waveshare Modbus RTU Relay (D) | 10 | 35,25 € | 353 € |
| Variateurs | Eltako EUD12D-UC | 8 | 43,45 € | 348 € |
| Maître | Convertisseur USB-RS485 isolé, un par zone | 3 | 22,61 € | 68 € |
| Alimentations, une par zone | Mean Well HDR-60-24 | 3 | 18,06 € | 54 € |
| **Matériel** | | | | **≈ 820 € HT** |
| Logiciel | | | 0 € | 0 € |
| **Total** | | | | **≈ 820 € HT**, ≈ 1,9 m de rail |

Soit ≈ 115 € HT de plus que la minimale pour passer de 6 à 3 défaillances uniques touchant toute la maison. Les trois qui restent sont la passerelle elle-même : aucun module ne les enlève. Variante TCP : trois coupleurs Wago 750-362 (1 227 € HT) et cinq bornes 750-1405 (≈ 560 € HT) sans les bornes relais, non trouvées ; trois Waveshare POE ETH Relay 30CH (210 $) sans les IO 8CH PoE, non relevés : **non chiffrée**.

### Couche domotique en dérivation

| Poste | Référence | Qté | Total HT |
| --- | --- | --- | --- |
| 88 relais vers les bobines des 38.51, 88 entrées de recopie | Waveshare Modbus RTU Relay (D) | 11 | 388 € |
| Maître | Convertisseur USB-RS485 isolé | 1 | 23 € |
| Alimentation | Mean Well HDR-60-24 | 1 | 18 € |
| **Matériel** | | | **≈ 430 € HT** |
| Logiciel | Bibliothèques libres | | 0 € |
| **Total** | | | **≈ 430 € HT**, ≈ 1,9 m de boîtiers |

Variantes, pour les mêmes ≈ 85 sorties et ≈ 70 entrées :

| Variante | Détail | Total HT |
| --- | --- | --- |
| RTU Waveshare, deux références | 3 × Relay 32CH (96 relais, 189 $) et 9 × IO 8CH (72 entrées, 216 $), convertisseur et alimentation | ≈ 410 € HT, ≈ 0,6 m plus les IO 8CH |
| RTU Advantech | 5 × ADAM-4051 (80 entrées, 823 €), 11 × ADAM-4068 (88 relais 0,25 A sur bobines, 2 167 €), convertisseur | ≈ 3 010 € HT |
| RTU Seneca | 5 × ZC-16DI-8DO (1 173 €), 5 × Z-10-D-OUT (660 €), 11 × Z-8R-10A (1 925 €), supports ≈ 100 € | ≈ 3 860 € HT |
| TCP Wago, par zone | 3 × 750-362 (1 227 €), 5 × 750-1405 (≈ 560 €), 43 × 750-517 (86 contacts 1 A, 4 818 €), fins de bus non chiffrées | ≈ 6 600 € HT |
| TCP Waveshare | 3 × POE ETH Relay 30CH (210 $), 9 × POE ETH IO 8CH (prix non relevé), commutateur PoE | incomplet |

Les relais de couplage et de recopie 38.51, le relais de garde et les bornes sectionnables sont déjà dans la V2 et ne sont pas recomptés.

### Ce qui n'est pas dans les totaux

- **Fonctions à reporter** : alarme, sirène et fuites sur les entrées et sorties des mêmes modules, logique dans la passerelle, pas de centrale certifiée ; écran existant en RS-485, qui reste sur un second port série du CM5 ; délestage par un compteur Modbus RTU du marché (Eastron, non chiffré) ou une entrée tore.
- **Mesure d'énergie** : compteurs Modbus RTU du marché, non détaillés.
- **Électricien** : non estimé par la note ; en lecture « seule », les modules remplacent télérupteurs et relais de volets ; en dérivation, le câblage TBT est celui de la V2.
- **Logiciel** : non estimé par la note ; pilote Modbus, logique et supervision dans la passerelle.
- **Place** : ≈ 1,75 m (minimale), ≈ 1,9 m (par zone), ≈ 1,9 m ou ≈ 0,6 m plus les IO 8CH (dérivation, en plus des 1,6 à 2,1 m de la couche filaire : un troisième coffret probable en Relay (D)).
- **Parafoudres RS-485** : ≈ 165 à 336 € par segment, facultatifs.
- **Import** : port, droits et TVA sur les achats en dollars.

## Ouverture et pérennité

- **Protocole ouvert** depuis 1979, sans redevance, spécification série de 2006 toujours en vigueur, tenue par une association d'utilisateurs et de fournisseurs ; fabricants innombrables dans l'automatisme, l'énergie et le chauffage. Dans ce dossier : Waveshare, Seneca, Advantech, ICP DAS, Wago, Wiren Board, Eastron, Schneider, Phoenix Contact, Weidmüller.
- **Interchangeabilité** : les cartes de registres diffèrent d'un fabricant à l'autre (coils et modes chez Waveshare, chien de garde en 0x1000 chez Wago, registre 8 chez Wiren Board) ; changer de fabricant adapte le pilote Go, pas le câblage. À dix ans, un module « 8 entrées, 8 relais à bornier à vis » se retrouvera chez quelqu'un.
- **Waveshare** : aucun marquage CE ni déclaration de conformité trouvés ; origine Chine ; relais « universel 10 A » sans marque ; documentation incohérente par endroits (parité inversée entre deux tableaux, « 8 voies » sur la page du 30 voies). Disponibilité à dix ans non publiée.
- **Industriels** : Seneca cite l'EN 61010-1 ; Advantech vend les ADAM-4000 depuis les années 1990, mais l'ADAM-6050 est « abandonné » chez un distributeur et en réapprovisionnement chez un autre, l'ADAM-4068-C est à 24 semaines de délai ; Wago 750 en quatrième génération, largement distribué. Wiren Board : pays et canal de vente non confirmés, un salon à Moscou en 2023, conditions d'achat à Astana ; conformité UE à vérifier avant de retenir ces références.
- **Cloud et licence** : aucun fabricant n'impose de compte ; bibliothèques Go et Python sous licences libres ; goburrow/modbus sans version publiée et avec 41 problèmes ouverts, à peser contre simonvetter/modbus.

## Verdict

- **Seule** : la forme la plus dépouillée d'une armoire à calculateur, pour ≈ 705 à 820 € HT. Elle met la passerelle, son Linux et son Go sur le chemin de chaque appui ; le découpage par zone ne retire rien à cette cause commune, et 3 défaillances uniques privent toute la maison, 4 en TCP. Les modes locaux Waveshare la rapprocheraient de la règle 1, sans documentation sur leur comportement au redémarrage. Ce n'est pas une réponse à l'exigence : c'est la V1 Revolution Pi sans la Revolution Pi.
- **En dérivation** : la couche domotique la moins chère du comparatif, ≈ 430 € HT, sans logique ni logiciel dans l'armoire, le battement de cœur émis par la passerelle et borné dans le module ; son point faible est l'absence de chien de garde et d'isolement chiffré chez Waveshare, que les 38.51 et le relais de garde de la V2 compensent, ou qu'un module industriel à chien de garde corrige pour 3 000 à 6 600 € HT. Elle fixe le repère de prix des autres dossiers.
- **À qui elle convient** : à qui garde la couche filaire de la V2 et veut, derrière, le serveur d'entrées-sorties le plus simple à piloter depuis le backend Go, en acceptant des boîtiers larges et peu documentés, ou le prix de leurs équivalents industriels.

## Sources

Toutes consultées le 24 octobre 2026.

1. [Wikipédia, Modbus](https://en.wikipedia.org/wiki/Modbus) : historique, Modbus Organization, 247 adresses, RTU et TCP.
2. [Modbus over serial line V1.02](https://millenia.cars.aps.anl.gov/software/epics/Modbus_over_serial_line_V1_02.pdf) : 32 appareils, 1 000 m, dérivations, terminaison, polarisation, commun à la terre.
3. [Waveshare, wiki Modbus RTU Relay 16CH](https://www.waveshare.com/wiki/Modbus_RTU_Relay_16CH), [32CH](https://www.waveshare.com/wiki/Modbus_RTU_Relay_32CH), [IO 8CH](https://www.waveshare.com/wiki/Modbus_RTU_IO_8CH), [Relay (D)](https://www.waveshare.com/wiki/Modbus_RTU_Relay_(D)), [POE ETH Relay 30CH](https://www.waveshare.com/wiki/Modbus_POE_ETH_Relay_30CH) : registres, flash-on / flash-off, modes linkage, toggle et edge, absence de chien de garde.
4. [Waveshare, Modbus RTU Relay 16CH](https://www.waveshare.com/modbus-rtu-relay-16ch.htm), [Relay (D)](https://www.waveshare.com/modbus-rtu-relay-d.htm), [IO 8CH](https://www.waveshare.com/modbus-rtu-io-8ch.htm), [Relay 32CH](https://www.waveshare.com/modbus-rtu-relay-32ch.htm), [POE ETH Relay 30CH](https://www.waveshare.com/modbus-poe-eth-relay-30ch.htm) : prix, cotes, isolations.
5. [Eckstein, Waveshare Relay (D)](https://eckstein-shop.de/WaveShare-Industrial-Modbus-RTU-8CH-Relay-Module-D-with-Digital-Input-and-RS485-Interface-EN) : 41,95 € TTC, origine, avis client sur l'état après coupure et le mode « linked ».
6. [Seneca Z-D-IN](https://www.seneca.it/en/linee-di-prodotto/acquisizione-dati-e-automazione/sistemi-io-modbus-rtu/moduli-io-digitali/z-d-in/), [ZC-16DI-8DO](https://www.seneca.it/en/linee-di-prodotto/acquisizione-dati-e-automazione/sistemi-io-modbus-rtu/moduli-io-digitali/zc-16di-8do/), [Z-10-D-OUT](https://www.seneca.it/en/linee-di-prodotto/acquisizione-dati-e-automazione/sistemi-io-modbus-rtu/moduli-io-digitali/z-10-d-out/) et sa [fiche technique](https://www.seneca.it/media/downloads/prodotti/5891/Z-10-D-OUT_Scheda%20tecnica.pdf) : isolement 1,5 kV CA, état sûr programmable, délai 10 à 2 000 s, prix.
7. [Advantech ADAM-4051 chez RS](https://de.rs-online.com/web/p/sps-ea-module/0657057), [ADAM-4055 chez RS](https://nl.rs-online.com/web/p/interface-modules/2844322), [fiche ADAM-4055](https://csi.pl/wp-content/uploads/2019/01/ADAM_4053_4055_4056S_4056SO_DataSheet.pdf), [ADAM-4068-C chez Farnell](https://be.farnell.com/en-BE/advantech/adam-4068-c/relay-output-module-w-modbus-8/dp/4208710) : isolement 2 500 V CC, chien de garde, contacts 0,25 A, prix, délais.
8. [Fiche ADAM-6050](https://www.bmc.de/datenblaetter/ADAM_6050.pdf), [FAQ ADAM-6000](https://www2.advantech.com/my/edm/eA/2008%20New_ADAM-6000_Series_eDM/index_FAQ.html), [ADAM-6050 chez RS](https://nl.rs-online.com/web/p/plc-accessories/0657063), [ADAM-6060 chez RS](https://fr.rs-online.com/web/p/modules-d-es-api/0718825), [ADAM-6050 chez Gridconnect](https://gridconnect.com/products/adam-6050-18-channel-digital-i-o-ethernet-and-modbus-tcp-module) : chien de garde de communication, logique P2P et GCL, prix, ruptures, « abandonné ».
9. [Fiche ICP DAS M-7055U](https://www.icpdas.com/root/product/solutions/datasheet/i-7000_m-7000/M-7055U(D)_en.pdf), [M-7055-CR chez Consteel](https://consteel-electronics.com/modbus-io-modules-RS485/M-7055-CR-en), [fiche ET-7055](https://elvac.eu/files/shop/icpdas/datasheet/et-7x55_pet-7x55_ELVAC15.pdf) : double chien de garde, valeurs sûre et au démarrage, isolement, surtension.
10. [Wago 750-362](https://www.wago.com/global/controllers-bus-couplers-i-o/controller-modbus-tcp/p/750-362), [750-362 chez RS France](https://fr.rs-online.com/web/p/automates-programmables/2885276), [manuel 750-362, chien de garde](https://www.manualslib.com/manual/1723930/Wago-Wago-I-O-System-750-750-362.html?page=180) et [défaillance de bus](https://www.manualslib.com/manual/1723930/Wago-Wago-I-O-System-750-750-362.html?page=137) : registres 0x1000, exception 0x0004, états définis sur panne du bus local, 409,05 € HT (même prix que le [dossier Wago](wago-pfc200.md)).
11. [Fiche Wago 750-1405](https://www.farnell.com/datasheets/4151964.pdf), [750-1405 chez Bürklin](https://buerklin.com/en/p/wago/digital-modules/750-1405/73F2038), [Wago 750-517](https://www.wago.com/global/i-o-systems/2-channel-relay-output/p/750-517), [750-517 chez RS France](https://fr.rs-online.com/web/p/modules-d-es-api/8687374) : 500 V, 12 mm, 1 A, 112,05 € HT à partir de 3 (même prix que le dossier Wago).
12. [Wiren Board WB-MR6C v.2](https://wirenboard.com/en/product/WB-MR6C_v2/), [WB-MDM3](https://wirenboard.com/en/product/WB-MDM3/), [wiki, réglage des relais](https://wiki.wirenboard.com/wiki/Includes._Relay_tuning/en), [article Habr 2023](https://habr.com/ru/companies/wirenboard/articles/727624/) : mode sûr, commande locale, variateur, origine.
13. [Eltako, notice EUD12D-UC](https://www.eltako.com/fileadmin/downloads/de/_bedienung/EUD12D_21100905-3_dt.pdf) : 400 W, entrée universelle isolée, appui court et long, mémoire ; prix catalogue 89,37 € HT. [zaehlerschrank24, EUD12D-UC](https://www.zaehlerschrank24.de/multi-dimmschalter-eud12d-uc.html) : 51,70 € TTC, soit 43,45 € HT, prix retenu par la V2.
14. [Mouser, Bridgetek MC-0301-01A](https://www.mouser.se/new/bridgetek/bridgetek-mc-0301-01a-modbus-light-dimmer) : variateur Modbus, prix non lu.
15. [Home Assistant, intégration Modbus](https://www.home-assistant.io/integrations/modbus/) : transports, entités, scrutation, limites des volets.
16. [goburrow/modbus](https://github.com/goburrow/modbus), [simonvetter/modbus](https://github.com/simonvetter/modbus), [pymodbus](https://github.com/pymodbus-dev/pymodbus) : licences, transports, activité.
17. [Node-RED, bus série qui tombe](https://discourse.nodered.org/t/modbus-serial-whole-bus-disconnects-when-one-device-drops/48555), [TI E2E, réseau RS-485 en panne](https://e2e.ti.com/support/interface-group/interface/f/interface-forum/650620/sn75176b-rs485-network-failed), [Industrial Shields, dépannage RS-485](https://www.industrialshields.com/blog/prototype-to-plant-34/rs485-bus-troubleshooting-706) : un port esclave en défaut fait tomber le bus, esclave hors tension en haute impédance.
18. [Texas Instruments, SLLA272D](https://www.ti.com/lit/an/slla272d/slla272d.pdf) : 32 charges unitaires, longueur, polarisation, isolement galvanique.
19. [Welectron, Waveshare 15817](https://welectron.com/Waveshare-15817-USB-TO-RS232-485-TTL), [Waveshare USB TO RS232/485 (B)](https://waveshare.com/usb-to-rs232-485-b.htm), [wiki USB TO 4CH RS485 (B)](https://waveshare.com/wiki/USB_TO_4CH_RS485_(B)), [RS485 CAN HAT (B)](https://www.waveshare.com/rs485-can-hat-b.htm) : convertisseurs, isolation, prix.
20. [Bürklin, Phoenix DT-UFB-485/BS](https://www.buerklin.com/en/PHOENIX-CO-2920612/p/64P5603), [MT-RS485](https://www.buerklin.com/en/PHOENIX-CO-2762265/p/64P5744), [RS UK, DT-UFB-485/BS](https://uk.rs-online.com/web/p/surge-protection-devices/0130206), [Phoenix PT 2X2](https://www.phoenixcontact.com/gb/products/2838228/pdf), [DEHN BXT ML4 BE BD 24 chez Cebeo](https://www.cebeo.be/catalog/nl-be/products/dehn-blitzductor-xt-ml4-bd-hf-24-3763776) : parafoudres RS-485, prix.
21. [TME, Mean Well HDR](https://www.tme.eu/dk/en/katalog/p,mean-well_339/) : HDR-60-24 à 18,06 € HT.
22. [Electrokit, Relay 16CH](https://www.electrokit.com/en/relamodul-16-kan-rs-485-/-modbus-din-skena) et [POE ETH Relay 30CH](https://www.electrokit.com/en/relay-module-30-ch-modbus-ethernet-poe-din-rail) : prix TTC en couronnes, rupture.

!!! note "À confirmer auprès des fabricants"
    Chez Waveshare : l'existence d'un chien de garde de communication, l'état des relais à la mise sous tension et après microcoupure, le comportement du mode « toggle » au redémarrage, les tensions d'isolement en kV du RS-485, des entrées et des relais, le marquage CE, la marque et l'endurance des relais, la consommation et les cotes des modules, la mise à jour du micrologiciel. Chez Wago : l'état des sorties à l'expiration du chien de garde Modbus, la borne relais 16 A et son prix. Chez Advantech : les sorties au déclenchement du chien de garde, le statut commercial de l'ADAM-6050, le prix de l'ADAM-6066. Chez Seneca : les registres du fail-safe et le régime de TVA des prix. Chez Wiren Board : le pays de fabrication et la conformité UE. Pour tous : la longueur de nappe admise sur les entrées, la latence poussoir → relais sur 9 à 11 esclaves, le prix du Bridgetek MC-0301-01A et des parafoudres DEHN, et l'arbitrage entre la mise à la terre du commun RS-485 et la règle « 0 V jamais au PE ».
