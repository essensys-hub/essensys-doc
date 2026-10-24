---
title: "Shelly Pro : remplacer l'armoire sans recâblage"
description: "Modules Shelly Pro sur rail DIN (LAN, Wi-Fi, API locale) pour remplacer les quatre cartes de l'armoire ESSENSYS sans toucher aux fils : chaque module lie lui-même ses entrées à ses relais, sans bus ni contrôleur. Seuls, ils tiennent la règle 1 en partie, sous réserve que les entrées, référencées au secteur d'après le forum, reçoivent un relais d'interface par poussoir ; en dérivation, une couche bon marché mais mal taillée. Environ 2 270 € HT hors relais d'interface et commutateur."
---

# Shelly Pro

Shelly Pro est, dans ce [comparatif](index.md), une gamme sans bus ni contrôleur : des modules autonomes sur rail DIN, chacun avec son microcontrôleur, son port LAN, son Wi-Fi, son serveur web et son API locale. Le poussoir est câblé sur l'entrée du module qui commande sa charge, et le micrologiciel du module fait le lien. Peut-elle reprendre les 63 poussoirs et toutes les charges sans changer un fil, et que reste-t-il quand le réseau, le cloud ou un module tombe ?

!!! abstract "Synthèse"
    - **Seule** : les fils ne changent pas, mais les entrées « S » des Pro ne sont pas séparées du secteur d'après les retours du forum Shelly, et aucune fiche officielle lisible ne dit le contraire : pour garder les 63 poussoirs en TBTS, il faut **un relais d'interface par poussoir**, non chiffré ici. Sous cette réserve, la liaison entrée → relais vit dans le micrologiciel de chaque module, sans bus ni contrôleur : **règle 1 partielle, à confirmer**, faute de phrase officielle disant qu'elle fonctionne sans réseau. **Aucune des huit défaillances uniques ne prive toute la maison de ses boutons**, en configuration minimale comme par zone : le réseau n'est pas sur le chemin du bouton. Mais l'état, les replis et le verrouillage des deux sens d'un volet vivent dans le micrologiciel, et l'isolement n'est documenté nulle part.
    - **En dérivation** : une couche bon marché, sans licence ni cloud, mais faite de relais 16 A qui commutent la phase, pas des contacts secs, avec vingt-deux micrologiciels à tenir à jour ; le battement de cœur du relais de garde passe par un script sur un module.
    - **Coût estimé** : ≈ 2 270 € HT en configuration minimale comme par zone (même matériel), ≈ 1 940 € HT en couche domotique seule, **hors relais d'interface, commutateur Ethernet et passerelle**. Prix d'octobre 2026 d'une boutique française, TTC à 20 % convertis en HT.
    - **Réserve** : estimations à confirmer par un électricien, des devis, le fabricant et des essais. Les fiches techniques officielles n'ont pas pu être lues pendant la recherche ; la tension des entrées, l'isolement et le caractère libre de potentiel des relais restent à établir.

## Principe et gamme

Shelly Group (Sofia, Bulgarie, ex-Allterco ; premiers appareils Shelly en 2013, cotation à Francfort) vend des modules connectés pour particuliers et installateurs. La série **Pro**, lancée en 2021 avec le Pro 4PM, est la déclinaison rail DIN : alimentation 110 à 240 V, port LAN RJ-45, Wi-Fi 2,4 GHz, Bluetooth, mesure de puissance par voie sur les modèles « PM ». Ce sont des appareils « Gen2+ », qui partagent l'API JSON-RPC des gammes Plus, Gen3 et Gen4.

L'architecture est **décentralisée** : il n'y a ni bus propriétaire, ni contrôleur central obligatoire, ni alimentation commune. Chaque module exécute lui-même le mode de ses entrées (`in_mode` : impulsion, suiveur, bascule, détaché), ses scripts et ses replis ; le réseau IP de la maison ne sert qu'à la commande à distance, à la lecture d'état et aux automatisations entre modules. Le cloud Shelly est facultatif : l'interface web locale fonctionne sans compte ni Internet.

Références retenues pour chiffrer : Pro 4PM (V2), Pro 2PM, Pro Dual Cover PM, Pro Dimmer 2PM. Les fiches du Pro 1, du Pro Dimmer 1PM et du Pro 3EM n'ont pas pu être lues. Le lieu de fabrication n'a pas été trouvé.

## Dans l'armoire sans recâblage

Les poussoirs se câblent sur les entrées S du module qui commande leur charge ; les charges se câblent sur ses relais. Aucun bus ne parcourt la maison, et le réseau n'est pas nécessaire au bouton.

| Fonction | Module | Voies | Largeur | Ce qu'il faut savoir |
| --- | --- | --- | --- | --- |
| 25 éclairages, divers | Shelly Pro 4PM (V2) | 4 relais 16 A, 40 A au total ; 4 entrées S1 à S4 | 3 modules (56 × 96 × 59 mm) | Mesure par voie ; écran couleur 1,8" à touches, dont le rôle sur les relais n'est pas établi ; protections surchauffe, surcharge, surtension ; la V2 annonce des « distances électriques améliorées côté LAN », sans chiffre |
| 15 volets dont le store | Shelly Pro 2PM | 2 relais 16 A, 25 A au total ; 2 entrées | non trouvée | Mode « cover » bidirectionnel ; calibration, position en %, détection d'obstacle par la puissance ; **verrouillage des deux sens logiciel** (erreur `bad_feedback` si les deux sorties sont actives) |
| | Shelly Pro Dual Cover PM | 2 volets, 16 A par sortie ; entrées non trouvées | ≈ 3 modules (96 × 53 × 59 mm) | Même composant Cover ; capteur de température interne |
| 8 variateurs | Shelly Pro Dimmer 2PM | 2 voies, 200 W par voie | ≈ 1 module (19 mm) | Coupure de phase descendante ; halogène, LED, transformateurs ferromagnétiques ; protection externe 10 A au plus ; neutre requis ; entrées pour un ou deux poussoirs, tension non trouvée |
| 63 poussoirs | entrées S des modules ci-dessus | 78 entrées | — | **Tension non trouvée sur une page officielle** ; d'après le forum, « non séparées électriquement du secteur » : poussoirs 24 V via relais d'interface, ou modules i4 DC reliés par le réseau |
| Fil pilote, cumulus, prises, arrosage, machines | Shelly Pro 4PM | 8 à 12 relais | 6 à 9 modules | Contacts qui commutent la phase amenée au module ; le fil pilote demande ses diodes en aval |
| Contact sec | Shelly Pro 1 | 1 relais, 2 entrées | non trouvée | Réputé libre de potentiel ; fiche illisible pendant la recherche |
| Réseau | commutateur Ethernet ≥ 29 ports, ou Wi-Fi | | | Seul élément partagé ; hors du chemin du bouton |

Le point qui conditionne tout est la **tension des entrées S**. Les 63 poussoirs arrivent en boucle TBTS, sur des jonctions IDC données pour 1 A. Si les entrées sont référencées au secteur, trois voies s'ouvrent : réalimenter les nappes en 230 V, ce qui change la classe du câblage et sort de la contrainte « sans recâblage » au sens de la sécurité ; interposer **un relais d'interface par poussoir**, bobine côté TBTS, contact côté entrée S, ce que le forum pratique avec des relais 24 V ; ou lire les poussoirs par des modules d'entrées basse tension (i4 DC) qui commandent les relais par le réseau, ce qui fait passer le bouton par le réseau. Ce dossier retient les relais d'interface : les fils ne changent pas, mais 63 relais s'ajoutent dans l'armoire, et ce sont eux qui portent la barrière d'isolement.

### Configuration minimale

Sept Pro 4PM pour les éclairages (28 relais), quinze Pro 2PM en mode volet, quatre Pro Dimmer 2PM, deux ou trois Pro 4PM pour le fil pilote, le cumulus, les prises, l'arrosage et les machines : **28 à 29 modules Shelly**, 78 entrées pour 63 poussoirs (10 × 4 + 15 × 2 + 4 × 2), chacun alimenté par le 230 V de sa rangée et relié par câble RJ-45 à un commutateur Ethernet, ou en Wi-Fi. Largeur : 34 modules pour les Pro 4PM et les variateurs (10 × 3 + 4 × 1), plus quinze Pro 2PM de largeur non trouvée, soit **≈ 60 modules, ≈ 1,1 m de rail, à vérifier**, hors relais d'interface. En variante, huit Pro Dual Cover PM (16 volets) remplacent les quinze Pro 2PM.

### Configuration résiliente

La gamme n'a ni segment, ni alimentation commune, ni contrôleur : il n'y a rien à découper par zone au sens du comparatif. La seule ressource partagée est le réseau IP, qui n'est pas sur le chemin du bouton tant que chaque poussoir est câblé sur l'entrée du module qui commande sa charge. La configuration résiliente est donc **la même que la minimale**, avec les modules regroupés par zone dans le coffret et, si l'on veut isoler aussi la commande à distance, un petit commutateur par zone. Les comptages et les prix qui suivent portent sur ce matériel.

## Seule face à l'exigence

### Les sept règles

| Règle | Tenue | Pourquoi |
| --- | --- | --- |
| 1. Pas de calculateur entre le bouton et sa charge | **Partielle, à confirmer** | Le poussoir attaque l'entrée d'un module du commerce dont le micrologiciel, fixé par le fabricant, commande le relais (`in_mode`, exécuté dans l'appareil) ; une panne ne prive que ses deux ou quatre circuits. Aucune phrase officielle ne dit que cette liaison fonctionne sans réseau ; un guide tiers l'affirme. Si les poussoirs passent par des modules i4 et le réseau, la règle n'est plus tenue |
| 2. L'état vit dans un organe bistable | Non tenue | L'état est retenu par le micrologiciel (`initial_state` : éteint, allumé, dernier état, suit l'entrée) et restitué au retour du 230 V, avec un délai réglable de 1 à 600 s ; le type de relais n'est pas documenté dans les sources lues. Un volet perd sa calibration au redémarrage |
| 3. La domotique ajoute, ne retire jamais | Non tenue | Le module **est** la domotique : un ordre RPC faux, un script ou `in_locked` commute ou verrouille n'importe quelle voie. Parades : authentification, réseau local sans cloud, pare-feu |
| 4. Une source et un fusible par zone, un fusible pour la domotique | Partielle | Chaque module vit sur le 230 V de sa rangée, derrière son disjoncteur ; il n'y a pas de source de commande 24 V, donc pas de F1 ni de F2. Avec des relais d'interface, leurs bobines peuvent reprendre la source et le fusible de zone de la V2 |
| 5. Barrière 4 kV et 8 mm, 0 V jamais au PE, parafoudres hors coffrets | Non tenue, à confirmer | Aucune tension d'essai, aucune catégorie de surtension, aucune mention SELV trouvée ; entrées au secteur d'après le forum ; côté LAN « amélioré » sans chiffre. Les relais d'interface, choisis à 4 kV et 8 mm, porteraient la barrière |
| 6. Replis choisis au câblage, essayés à la recette | Non tenue | Les replis sont des paramètres du micrologiciel : état initial, délai de remise sous tension, durée maximale de course, obstacle, interrupteur de sécurité ; le verrouillage des deux sens d'un volet est détecté par logiciel, aucun verrouillage matériel n'est documenté |
| 7. Isolement mesuré chaque année | Tenue | Rien ne l'empêche ; avec des entrées au secteur sans relais d'interface, les lignes de poussoirs deviendraient des lignes 230 V et se mesureraient comme telles |

### Les causes communes

Dans la configuration résiliente, identique à la minimale, la liste fermée du comparatif donne :

| Défaillance unique | Prive de ses boutons… | Pourquoi |
| --- | --- | --- |
| 1. Alimentation du système | rien | Aucune alimentation commune ; chaque module vit sur le 230 V de sa rangée. Le disjoncteur d'une rangée prive ses modules, et ses charges avec eux |
| 2. Court-circuit ou ligne collée | rien | Aucun bus ; un défaut réseau ne touche pas la liaison entrée → relais, si elle est bien locale (à confirmer) |
| 3. Contrôleur central | rien | Il n'y en a pas ; la passerelle et Home Assistant sont facultatifs pour le bouton |
| 4. Logiciel figé | un module | Le micrologiciel d'un module figé prive ses voies ; aucun chien de garde ni redémarrage automatique documenté |
| 5. Mise à jour ratée | un module | La mise à jour se lance appareil par appareil (`Shelly.Update`), elle n'est pas imposée à distance ; aucun retour arrière documenté, et un module bloqué peut être irrécupérable : il se remplace |
| 6. Licence, compte ou cloud | rien | Aucune licence ; cloud et compte facultatifs, l'interface locale suffit |
| 7. Commutateur ou routeur | rien | Hors du chemin du bouton ; perdus : la commande à distance et les automatisations entre modules |
| 8. Foudre sur le chemin du bus | un module | Aucun bus ; l'onde entre par une ligne de poussoir et frappe le relais d'interface, puis au pire le module ; sans relais d'interface, elle entre directement dans le module par une entrée au secteur |

**Total : 0 défaillance unique prive toute la maison**, 3 privent un module. En configuration minimale, le décompte est le même : **0**.

Ce décompte dit l'essentiel : par son architecture à un module par groupe de circuits, Shelly Pro est la solution de ce comparatif la plus proche de la V2 dans l'esprit, aucune panne unique ne faisant taire toute la maison. La distance est ailleurs : le lien du bouton à sa charge est un micrologiciel, l'état et les replis vivent dans ce micrologiciel, et le poussoir en TBTS demande un relais de plus.

### Ce qui reste, panne par panne

| Panne | Ce qui reste |
| --- | --- |
| Réseau, commutateur, routeur, Internet | Tous les boutons, si la liaison locale est confirmée ; perdus : l'application, la commande à distance, les scènes entre modules, les scripts qui appellent un autre module |
| Passerelle ou Home Assistant | Idem ; les scripts locaux de chaque module continuent |
| Cloud Shelly | Rien de perdu en exploitation ; le forum signale une application « capricieuse » sans cloud et conseille une connexion Internet pour la première configuration |
| Un module figé ou bloqué en mise à jour | Ses deux ou quatre circuits, jusqu'au redémarrage ou au remplacement ; les autres modules ne voient rien |
| Coupure du secteur | Au retour, chaque sortie reprend l'état réglé (dernier état, éteint, allumé ou suit l'entrée), après un délai réglable ; les volets perdent leur calibration et ne gardent que montée et descente à durée bornée |
| Disjoncteur d'une rangée | Les modules des autres rangées ; la rangée perd ses charges et ses boutons ensemble |
| Foudre par une ligne de poussoir | Le relais d'interface au pire, puis le module ; les autres modules |

## En dérivation sur le filaire V2

Dans cette lecture, les télérupteurs, les chaînes de volets et les variateurs à entrée locale gardent le chemin du bouton. Shelly Pro fournit la couche domotique :

- **Sorties** : vingt-deux Pro 4PM (88 relais, 88 entrées). Les relais du Pro 4PM commutent la phase amenée au module : ils ne sont pas documentés comme libres de potentiel. Ils ne peuvent donc pas fermer directement un contact sec sur la TBTS de zone ; ils commandent la **bobine d'un relais de couplage 38.51 en 230 V**, dont le contact sec rejoint le poussoir, ce qui garde la barrière de la V2. Le Pro 1, réputé à contact sec, serait l'autre voie, sa fiche n'ayant pas pu être lue.
- **Entrées** : les 88 entrées S lisent les relais de recopie de la V2. Si elles sont référencées au secteur, le contact du relais de recopie, qui commute déjà le 230 V du circuit, convient tel quel.
- **Battement de cœur** : la **passerelle** réarme le chien de garde. Elle envoie un ordre RPC périodique à un module qui ferme un relais pendant une durée bornée, par un script local (`Timer.set`, `Shelly.call`), vers la bobine du relais de garde. Si la passerelle se tait, le script n'est plus relancé et le relais retombe. Un script qui battrait seul, sans la passerelle, tiendrait la couche armée sans personne pour la piloter : à éviter. Aucun chien de garde matériel n'est documenté sur les modules.
- **Logique et interface utilisateur** : la passerelle, par MQTT ou HTTP RPC. Les modules offrent des scripts JavaScript (trois par appareil), des webhooks et des actions ; les horaires et les scénarios restent dans la passerelle.
- **Durées bornées** : les scripts et le composant Cover les bornent ; le câblage de la V2 les borne de toute façon.

Ce que la couche apporte : un prix bas, ≈ 1 940 € HT, aucune licence, aucun compte, une API documentée que Home Assistant et openHAB parlent déjà, et Modbus TCP ou MQTT pour la passerelle. Ce qu'elle coûte : 22 modules de trois unités, ≈ 1,2 m de rail en plus de la couche filaire, 88 relais 16 A pour commander des bobines, 22 adresses IP et 22 micrologiciels à suivre, aucune donnée d'isolement, et des relais de couplage à bobine 230 V plutôt que 24 V. À comparer à la Revolution Pi Connect 5 (≈ 581 € HT nue, modules d'entrées-sorties non chiffrés ici) : une architecture éclatée, sans Linux dans l'armoire ; face à KNX (≈ 3 100 € HT), c'est moins cher et aussi large ; face au serveur d'entrées-sorties léger ([dossier Modbus](modbus-es.md)), c'est plus cher et beaucoup plus encombrant pour une fonction d'entrées-sorties pure.

## Foudre et isolement

- **Aucun bus** ne parcourt la maison, et le réseau n'est pas sur le chemin du bouton. Les nappes des poussoirs portent ce que les entrées imposent : du 230 V si elles sont au secteur sans relais d'interface, ce qui ferait disparaître l'îlot TBTS des boutons ; la TBTS de la V2 si des relais d'interface les séparent.
- **Tensions d'essai** : aucune fiche lisible ne donne de tension d'essai, de catégorie de surtension ni de mention SELV, ni pour les entrées, ni entre LAN et 230 V ; le Pro 4PM V2 annonce seulement des « distances électriques améliorées côté LAN ». La barrière de 4 kV et 8 mm de la V2 n'est donc **pas établie** par les modules : elle repose sur les relais d'interface et de couplage, choisis pour la tenir.
- **Deux îlots** : le 0 V des boutons ne touche aucun module, si les relais d'interface sont là ; le réseau Ethernet relie tous les modules entre eux et à la passerelle, et l'isolateur Ethernet de la V2 garde sa place vers la passerelle.
- **Parafoudres** : aucune recommandation Shelly trouvée.
- **Wi-Fi** : il évite le câble réseau entre modules, pas la question de l'isolement des entrées ; il n'est pas sur le chemin du bouton.

## Logiciel, paramétrage et passerelle Essensys

| Point | Ce qu'on a trouvé |
| --- | --- |
| Outil | Interface web locale de chaque module, sans compte ni Internet ; application Shelly Smart Control, cloud facultatif ; API RPC. Aucune licence, aucun outil payant |
| Formation | Aucune ; à la portée d'un installateur ou d'un particulier. Les scripts demandent un peu de JavaScript |
| Mise à jour | `Shelly.Update` par appareil, canal stable ou bêta, lancée par l'utilisateur ; « ne jamais couper l'alimentation pendant une mise à jour » (site d'employés Shelly, non officiel) ; aucun retour arrière documenté ; incidents rapportés avec certains points d'accès Wi-Fi |
| Sécurité | Authentification digest SHA-256 facultative, utilisateur unique ; limitation des tentatives depuis le micrologiciel 2.0.0 ; HTTPS, TLS, WebSocket |
| API pour la passerelle | **JSON-RPC 2.0** par HTTP (`/rpc`), WebSocket, **MQTT** (`<id>/rpc`, `<id>/events/rpc`, `<id>/online`), UDP sans garantie ; notifications d'état et d'événements ; **Modbus TCP** (port 502, registres par composant) ; KNXnet/IP annoncé sur le Pro Dimmer 2PM et contesté sur le Pro 4PM selon les revendeurs |
| Scripts | JavaScript sur l'appareil : gestionnaires d'événements et d'état, appels RPC, minuteries ; trois scripts actifs, démarrage automatique, mémoire partagée |
| Home Assistant, openHAB | Intégration Shelly native et locale dans Home Assistant ; binding openHAB |
| Cloud | Facultatif ; mis en avant commercialement, non requis |

Côté passerelle, le backend Go parle MQTT ou HTTP RPC à chaque module, s'abonne aux notifications et aux événements d'entrée (appui simple, double, triple, long), et porte le battement de cœur. L'estimation de cette étude, sans source, est de **deux à quatre semaines-personne**, plus l'écriture et la recette du script de garde. Aucun logiciel du projet ne tourne dans l'armoire, mais vingt-deux micrologiciels du fabricant y tournent.

## Nomenclature et coût estimé

Prix relevés le 24 octobre 2026 chez une boutique française (Domadoo), TTC à 20 % avec une remise de 10 % incluse, convertis ici en HT. Les prix du Pro 1, du Pro Dimmer 1PM et du Pro 3EM n'ont pas été trouvés ; le prix du Pro Dual Cover PM vient de revendeurs britanniques et finlandais, TVA non précisée.

### Configuration minimale

| Poste | Référence | Qté | Prix unitaire HT | Total HT | Source |
| --- | --- | --- | --- | --- | --- |
| Éclairages et divers | Shelly Pro 4PM | 10 | 88,11 € (105,73 € TTC) | 881 € | Domadoo |
| Volets | Shelly Pro 2PM | 15 | 75,10 € (90,12 € TTC) | 1 127 € | Domadoo |
| Variateurs | Shelly Pro Dimmer 2PM | 4 | 64,42 € (77,30 € TTC) | 258 € | Domadoo |
| Relais d'interface des poussoirs | 63 relais bobine 24 V, contact 230 V | 63 | non chiffré | — | — |
| Commutateur Ethernet ≥ 29 ports | — | 1 | non trouvé | — | — |
| **Matériel** | | | | **≈ 2 270 € HT** | hors relais d'interface et commutateur |
| Logiciel | aucun | | 0 € | 0 € | |
| **Total** | | | | **≈ 2 270 € HT** | |

Variante volets : huit Pro Dual Cover PM à ≈ 105 € (TVA non précisée) remplacent les quinze Pro 2PM, soit ≈ 840 € au lieu de ≈ 1 130 €. D'autres boutiques affichent le Pro 2PM de 69,99 € à 99,90 € TTC et le Pro Dimmer 2PM de 57 £ à 95 £ : les totaux varient de ± 15 % selon la boutique.

### Configuration résiliente

| Poste | Référence | Qté | Prix unitaire HT | Total HT |
| --- | --- | --- | --- | --- |
| Même matériel que la configuration minimale | Pro 4PM × 10, Pro 2PM × 15, Pro Dimmer 2PM × 4 | 29 | voir ci-dessus | ≈ 2 266 € |
| Commutateurs | un petit commutateur par zone, facultatif | 3 | non trouvé | — |
| **Matériel** | | | | **≈ 2 270 € HT**, hors relais d'interface et commutateurs |
| Logiciel | aucun | | 0 € | 0 € |
| **Total** | | | | **≈ 2 270 € HT** |

La gamme n'ayant ni segment ni contrôleur, la configuration par zone ne coûte rien de plus que la minimale : elle change la disposition dans le coffret, pas le matériel, et le décompte des causes communes est le même, 0.

### Couche domotique en dérivation

| Poste | Référence | Qté | Total HT |
| --- | --- | --- | --- |
| Sorties vers les relais de couplage et entrées de recopie | Shelly Pro 4PM × 22 (88 relais, 88 entrées) | 22 | ≈ 1 938 € |
| Commutateur Ethernet ≥ 22 ports | — | 1 | non trouvé |
| **Matériel** | | | **≈ 1 940 € HT** |
| Logiciel | aucun | | 0 € |
| **Total** | | | **≈ 1 940 € HT**, ≈ 66 modules (≈ 1,2 m de rail) |

Sous réserve que les relais commandent des bobines 230 V de relais de couplage, et que les entrées acceptent les recopies, leur tension n'étant pas établie.

### Ce qui n'est pas dans les totaux

- **Fonctions à reporter** : aucune fonction d'alarme native ; la sirène et les détecteurs se raccordent à des voies, la logique revient à la passerelle. Écran : seul le Pro 4PM en a un, sans rôle établi sur les relais. Délestage : seuils de puissance et de courant par sortie, mesure par voie sur les « PM », la logique d'ensemble revient à la passerelle.
- **Relais d'interface pour les 63 poussoirs** : non chiffrés dans la recherche ; l'ordre de grandeur est celui des relais de couplage 38.51 de la [V2](../v2/filaire-d-abord.md), 1 200 à 1 350 € HT pour 63 à 71 relais, et ≈ 0,4 m de rail de plus.
- **Fil pilote** : contacts des Pro 4PM, diodes en aval, à chiffrer.
- **Commutateur Ethernet** : 22 à 29 ports, ou Wi-Fi ; non trouvé.
- **Électricien** : de l'ordre de 4 à 6 jours (estimation sans devis), les relais d'interface comptant pour une bonne part.
- **Logiciel** : ≈ 2 à 4 semaines-personne (passerelle et script de garde), estimation sans source.
- **Place** : ≈ 1,1 m (minimale et par zone, à vérifier, largeur du Pro 2PM non trouvée), ≈ 1,2 m (dérivation, en plus de la couche filaire), relais d'interface non compris.

## Ouverture et pérennité

- **Un seul fabricant**, micrologiciel propriétaire sans source publié, mais **API locale documentée publiquement** (HTTP, WebSocket, MQTT, UDP), Modbus TCP, KNXnet/IP sur certains modèles ; interopérabilité par MQTT, Home Assistant, openHAB.
- **Ancienneté** : premiers Shelly en 2013, Pro 4PM en 2021. La génération 1 (CoAP) a été remplacée par Gen2+ ; le Pro 4PM a déjà connu une révision matérielle V1 → V2. Politique de support à long terme et disponibilité à dix ans non trouvées.
- **Entreprise** : Shelly Group SE, cotée, 350 employés, chiffre d'affaires 2025 de 149,7 M€ en croissance, résultat positif ; actionnariat fondateur majoritaire. Pas de signe de fragilité dans les documents lus.
- **Cloud facultatif**, interface locale sans compte ; la mise à jour n'est pas imposée à distance.
- **Vente libre**, prix publics bas, nombreux revendeurs.
- **Communauté** : forum officiel actif, Home Assistant, openHAB ; c'est au forum, pas aux fiches, que l'on a trouvé la question des entrées.

## Verdict

- **Seule** : Shelly Pro est une architecture sans bus ni contrôleur, et aucune défaillance unique ne prive toute la maison de ses boutons. Elle tient la règle 1 en partie, sous réserve de confirmation : le lien du bouton à sa charge est le micrologiciel d'un module du commerce, et une panne ne prive que ses deux ou quatre circuits. Mais la contrainte « sans recâblage » ne tient qu'au prix d'un relais d'interface par poussoir, si les entrées sont bien au secteur ; l'état, les replis et le verrouillage des volets vivent dans le micrologiciel ; et l'isolement n'est documenté nulle part. C'est l'esprit de la V2 avec un microcontrôleur et un micrologiciel à la place de chaque télérupteur.
- **En dérivation** : une couche bon marché et simple à mettre en service, sans licence ni cloud, mais mal taillée : des relais 16 A qui commutent la phase pour commander des bobines, 22 modules et 22 micrologiciels, aucune donnée d'isolement, un battement de cœur par script. Un serveur d'entrées-sorties Modbus fait la même chose en plus petit et plus propre.
- **À qui elle convient** : à qui veut une maison commandable localement sans bus, sans licence et sans contrôleur, accepte un micrologiciel du commerce sur le chemin du bouton, et pose un relais d'interface par poussoir.

## Sources

Toutes consultées le 24 octobre 2026.

1. [Montega, Shelly Group SE, note du 12 mai 2026](https://corporate.shelly.com/uploads/analysts/1778596895525-2026-05-12_Montega_79.pdf) : historique, effectifs, chiffre d'affaires 2025, actionnariat.
2. [EQS, chiffre d'affaires du premier semestre 2026](https://www.gettex.de/en/news-overview/newsdetail/eqs-adhoc-shelly-group-reports-preliminary-group-revenue-for-the-first-half-of-2026/) et [des neuf premiers mois](https://www.webdisclosure.com/press-release/eqs-adhoc-shelly-group-reports-preliminary-consolidated-revenue-for-the-first-nine-months-of-2026-8aa5m4OdNqg).
3. [Shelly API, protocole RPC](https://shelly-api-docs.shelly.cloud/gen2/General/RPCProtocol), [canaux](https://shelly-api-docs.shelly.cloud/gen2/General/RPCChannels), [authentification](https://shelly-api-docs.shelly.cloud/gen2/General/Authentication).
4. [Shelly, documentation Pro 4PM](https://shelly.com/blogs/documentation/shelly-pro-4pm) et [Pro 4PM V2](https://automations.shelly.com/blogs/documentation/shelly-pro-4pm-v2) : entrées S1 à S4, borne Live 110-240 V, fonctionnement local, distances côté LAN.
5. [Next, Shelly Pro 4PM en précommande](https://next.ink/2200/le-shelly-pro-4pm-en-precommande-relais-4x-16-a-sur-rail-avec-ou-sans-fil-et-ecran-couleur/) (2021) : 4 × 16 A, écran 1,8", prix de lancement.
6. Revendeurs du Pro 4PM : [BayWa r.e.](https://solar-distribution.baywa-re.de/en/system-accessories/shelly-pro-4pm.html) (protections, 40 A), [Ahlsell](https://www.ahlsell.se/en/products/electric/installation-equipment-11-18/17-17-property-automation--iot/shelly/relay/1302016e---rela-din-wifi-pro-4pm) (3 modules, fonctionnement local, KNX non supporté), [Alloys](https://www.alloys.com.au/security-and-automation/lighting-control/relays/shelly-4pm-pro-4-circuit-din-rail-wi-fi-relay-switch-with-power-metering) (touches, KNXnet/IP).
7. [The Pi Hut, Pro 2PM](https://thepihut.com/products/shelly-pro-2pm) : 2 × 16 A, moteur bidirectionnel, température.
8. [Ameridroid, Pro Dual Cover PM](https://ameridroid.com/products/shelly-pro-dual-cover-shutter-pm) : 2 volets, dimensions, CoAP non supporté.
9. [The Pi Hut, Pro Dimmer 2PM](https://thepihut.com/products/shelly-pro-dimmer-2pm), [Smart-Secure](https://www.smart-secure.co.uk/?p=49356) et [NetXL](https://www.netxl.com/switches-and-dimmers/shelly-pro-dimmer-2pm-din-rail-smart-dimmer-power-metering.md) : 200 W par voie, 19 mm, protocoles, protection 10 A.
10. Forum Shelly : [déclenchement par contact libre de potentiel](https://shelly-forum.com/thread/11555-triggering-floodlights-with-volt-free-contact-closure) et [entrées du Pro 4PM](https://shelly-forum.com/thread/11641-switch-input-4pm) : entrées non séparées du secteur, relais 24 V ou modules i3.
11. [Shelly API, composant Cover](https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Cover) : modes d'entrée, calibration, durée maximale, obstacle, `bad_feedback`.
12. [Shelly API, composant Switch](https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Switch) : `in_mode`, `in_locked`, `initial_state`, délai de remise sous tension, limites.
13. [Shelly API, composant Input](https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Input) : événements d'appui.
14. [Shelly API, tutoriel des scripts](https://shelly-api-docs.shelly.cloud/gen2/Scripts/Tutorial) et [composant Script](https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Script) : scripts sur l'appareil, minuteries, trois scripts, démarrage automatique.
15. [Shelly API, service Shelly](https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Shelly) : `Shelly.Update`, `Shelly.Reboot`, `Shelly.FactoryReset`.
16. [Shelly API, composant Modbus](https://shelly-api-docs.shelly.cloud/gen2/ComponentsAndServices/Modbus) : port 502, registres.
17. [Shelly, guide d'interface web 2PM Gen3](https://www.shelly.com/fr/blogs/documentation/shelly-2pm-gen3-web-interface-guide) : ni Internet ni cloud nécessaires.
18. [shelly.guide, problèmes de mise à jour](https://shelly.guide/en/troubleshooting/update-problems/) (site d'employés Shelly, non officiel) : alimentation à ne pas couper, remise à zéro inutile, support.
19. Forum Shelly et openHAB : [mise à jour bloquée avec certains points d'accès](https://shelly-forum.com/thread/23156-firmware-update-with-unifi-aps-not-working), [binding openHAB et micrologiciel 1.4.0](https://community.openhab.org/t/shelly-binding-error-gen-2-firmware-1-4-0/157664), [fonctionnement sans cloud](https://shelly-forum.com/user-post-list/35880-doron).
20. Prix : [Domadoo Pro 4PM](https://www.domadoo.fr/fr/objets-communicants/5890-shelly-pro-4pm-module-rail-din-4-canaux-wi-fi-avec-mesure-d-energie-3800235268049.html), [Domadoo Pro 2PM](https://www.domadoo.fr/fr/modules-connectes/6004-shelly-module-rail-din-2-canaux-wi-fi-avec-mesure-d-energie-shelly-3800235268032.html), [Domadoo Pro Dimmer 2PM](https://www.domadoo.fr/fr/eclairage-connecte/6973-shelly-module-variateur-rail-din-2-canaux-wi-fi-avec-mesure-d-energ-3800235268179.html), [Powerplanet Pro 2PM](https://www.powerplanetonline.com/fr/shelly-pro-2pm-noir), [Bürklin Pro 2PM](https://www.buerklin.com/en/p/70P0048/), [shelly.com série Pro](https://www.shelly.com/en-pl/products/professional-series), [The Pi Hut Pro Dual Cover PM](https://thepihut.com/products/shelly-pro-dual-cover-shutter-pm).

!!! note "À confirmer auprès des fabricants"
    La tension et la référence des entrées S1 à S4 des Pro 4PM, Pro 2PM, Pro Dual Cover PM et Pro Dimmer 2PM (au secteur ou contact sec) ; une déclaration officielle que la liaison entrée → relais fonctionne sans réseau, sans cloud et sans Home Assistant, et son comportement pendant un redémarrage ; les tensions d'essai entrées / 230 V et LAN / 230 V, la catégorie de surtension et la mention SELV ; le ou les modèles Pro à relais libre de potentiel (Pro 1, Pro 2) et leur fiche ; le rôle des touches du Pro 4PM sur les relais et l'existence de boutons de façade sur les autres Pro ; le chien de garde, le redémarrage automatique, la double partition ou le retour arrière du micrologiciel, et la procédure de récupération après une mise à jour échouée ; la largeur du Pro 2PM et du Pro Dimmer 1PM, le nombre d'entrées du Pro Dual Cover PM et du Pro Dimmer 2PM ; les prix du Pro 1, du Pro Dimmer 1PM et du Pro 3EM ; la liste des modèles et micrologiciels qui parlent KNXnet/IP ; la version courante du micrologiciel Gen2+, la politique de support et le lieu de fabrication.
