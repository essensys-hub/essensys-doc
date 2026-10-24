---
title: "ESPHome sur rail DIN : remplacer l'armoire sans recâblage"
description: "Trois cartes KinCony KC868-A32 sous ESPHome, une par zone, avec Home Assistant en supervision, pour remplacer les quatre cartes de l'armoire ESSENSYS sans toucher aux fils. Seule, la logique tourne sur chaque ESP32 sans Home Assistant, mais l'état vit dans un micrologiciel compilé par le projet et le redémarrage automatique éteint les relais ; en dérivation, c'est la couche d'entrées-sorties la moins chère en cartes, sans isolement chiffré. De l'ordre de 710 € HT en armoire complète, 360 € HT en couche domotique seule, hors alimentation, port et droits."
---

# ESPHome sur rail DIN

ESPHome compile un fichier YAML en micrologiciel pour une carte ESP32 ; les cartes KinCony KC868 portent 16 ou 32 entrées à contact sec et autant de relais 230 V. C'est la voie « maison » la moins chère de ce [comparatif](index.md), à rapprocher de la refonte Raspberry Pi des V1 : que vaut-elle quand on lui demande de reprendre les 63 poussoirs et toutes les charges, et que reste-t-il quand Home Assistant, le réseau ou une carte se tait ?

!!! abstract "Synthèse"
    - **Seule** : trois KC868-A32, une par zone, reprennent les 63 poussoirs et jusqu'à 96 relais sans changer un fil, mais pas sur rail DIN modulaire : trois boîtiers de 320 mm à visser sur platine. La liaison entrée → relais tourne sur l'ESP32 de chaque carte et marche sans Home Assistant : **règle 1 non tenue**, avec une logique locale par carte, mais un micrologiciel du projet, compilé à partir d'un YAML et non fixé par le fabricant. Deux pièges documentés : par défaut, une carte **redémarre toutes les 15 minutes** quand aucun client ne lui parle (`reboot_timeout`) et ses relais reviennent à `ALWAYS_OFF` au redémarrage. Correctement paramétrée, aucune des huit défaillances uniques ne prive toute la maison ; mal paramétrée, deux le font toutes les 15 minutes.
    - **En dérivation** : 96 contacts inverseurs et 96 entrées pour ≈ 360 € HT, le prix de cartes le plus bas du comparatif, derrière les relais de couplage et le relais de garde de la V2. Mais aucune tension d'isolement publiée, un marquage CE qui ne couvre que la radio, et un micrologiciel du projet à maintenir dans l'armoire.
    - **Coût estimé** : ≈ 710 € HT en armoire complète, configuration minimale et par zone confondues, dont ≈ 360 € HT de cartes et ≈ 350 € HT de variateurs Eltako au prix boutique retenu par la V2 ; ≈ 360 € HT en couche domotique seule. Hors alimentation 12 V, commutateur, port, droits et TVA d'import, non chiffrés. Prix en dollars d'octobre 2026 convertis au change du jour, non vérifiés.
    - **Réserve** : estimations à confirmer par un électricien, des devis, le fabricant et des essais. La boutique du fabricant n'a pas pu être consultée en direct ; les prix viennent de résumés de recherche.

## Principe et gamme

**ESPHome** est un projet open source (GPLv3 pour le code C++, MIT pour la partie Python) qui transforme un fichier YAML en micrologiciel pour ESP32, ESP8266 et quelques autres microcontrôleurs. Depuis avril 2024, ESPHome et Home Assistant appartiennent à l'Open Home Foundation, organisation sans but lucratif ; la société Nabu Casa reste partenaire et vend le matériel Home Assistant. Le principe affiché est que les automatisations tournent **sur le microcontrôleur** et continuent si le réseau ou le serveur tombe. Home Assistant se connecte par une API native chiffrée ou par MQTT ; il sert à la supervision et aux scènes entre cartes, pas à la liaison entrée → relais.

**KinCony** (Hangzhou, Chine, fondée en 2007, effectif non trouvé) fabrique des cartes ESP32 à relais prêtes pour ESPHome, Tasmota ou son propre micrologiciel KCS. Cartes retenues :

- **KC868-A32** : ESP-WROOM-32, 32 entrées « optoisolated dry contact », 32 relais « 220 V / 10 A » inverseurs, 4 entrées analogiques, Ethernet, RS-485, USB, alimentation 12 V ;
- **KC868-A32 Pro** (2024) : ESP32-S3, 32 relais, 32 boutons manuels annoncés « qui peuvent commander les relais même si le système tombe », deux sorties 0-10 V, mécanisme des boutons et prix non trouvés ;
- **KC868-A16** : 16 entrées, 16 relais, Ethernet, RS-485 ; version A16v3 à caractéristiques non trouvées ;
- extensions : KC868-D8 (8 sorties 0-10 V), KC868-E16v2 (16 relais), KC868-A32M (entrées 24 V).

La topologie est une **étoile IP** : chaque carte est autonome, reliée au réseau par Ethernet ou Wi-Fi ; aucun bus de terrain ne relie les cartes entre elles.

## Dans l'armoire sans recâblage

Les poussoirs sont des contacts secs : ils se ferment vers le GND de la carte, qui fournit elle-même la boucle (« only need digital input short with GND, not need 12v »). Les niveaux suivent l'alimentation de la carte : 0 à 4 V pour « 0 », 6 à 12 V pour « 1 » ; du 24 V direct « casserait la carte ».

| Fonction | Module | Voies | Largeur | Ce qu'il faut savoir |
| --- | --- | --- | --- | --- |
| 63 poussoirs | KC868-A32 | 32 entrées à contact sec | 320 × 122 mm, profilé ouvert | Optocoupleurs EL357 lus par quatre PCF8574 sur un bus I2C interne ; une borne GND par groupe de 8, **tous les GND reliés** à celui de l'alimentation 12 V ; courant de boucle, filtrage et longueur de ligne admise non trouvés |
| | KC868-A16 | 16 | boîtier aluminium | Même principe, deux PCF8574 ; prix non trouvé |
| 25 éclairages | Relais de la KC868-A32 | 32 relais 10 A, COM/NO/NC | sur la carte | Pilotés par ULN2003A derrière quatre PCF8574 sur un second bus I2C ; référence du relais, tenue à l'appel de courant des LED et endurance non trouvées ; le fabricant conseille des contacteurs pour les charges inductives |
| 15 volets dont le store | Deux relais de l'A32 par volet | 30 relais | sur la carte | Verrouillage `interlock` **logiciel** ; ESPHome « recommande fortement » un verrouillage matériel, obtenu ici en croisant les contacts NO et NC des relais inverseurs ; plateforme `cover: time_based`, position estimée et restaurée après redémarrage |
| 8 variateurs | Aucune carte triac 230 V | | | Options : KC868-D8 et variateurs à entrée 0-10 V (prix du D8 non trouvé) ; deux sorties 0-10 V sur l'A32 Pro ; ou un Eltako EUD12D-UC par lampe, commandé par un relais de l'A32 en parallèle du poussoir |
| Fil pilote, cumulus, prises, arrosage, machines | Relais de l'A32 | ≈ 10 relais | sur la carte | Un relais par ordre de fil pilote ; la bobine du contacteur de cumulus se commande par un relais |
| Alimentation | Bloc 12 V continu | | non chiffré | Consommation d'une A32 avec 32 relais collés non trouvée |
| Réseau | Commutateur Ethernet | | | Hors du chemin du bouton, sauf piège `reboot_timeout` (voir plus bas) |
| Hôte Home Assistant | Raspberry Pi CM5 existant ou autre | | | Supervision, scènes entre cartes, compilation des micrologiciels |

Les cartes ne sont pas des modules de 17,5 mm : le fabricant les livre en profilé ouvert à visser sur une platine, et le montage sur rail DIN n'est pas mentionné. Trois A32 côte à côte font ≈ 0,96 m de large.

### Configuration minimale

Deux KC868-A32 et une KC868-A16, soit 80 entrées et 80 relais, ou plus simplement **trois A32** (96 et 96), une alimentation 12 V, un commutateur, Home Assistant sur le CM5. Les huit variateurs passent par des EUD12D-UC ou par un D8. Une seule alimentation et un seul GND pour les 63 boutons.

### Configuration résiliente

**Trois A32, une par zone** : pièces de vie 20 entrées et ≈ 22 relais, chambres 21 et ≈ 23, pièces d'eau 22 et ≈ 26, chacune sous les 32 voies de la carte. Chaque carte a sa propre alimentation 12 V et son GND ; les cartes ne se touchent que par Ethernet, à transformateur d'isolement. La logique de zone (poussoir → relais, verrouillage des volets, minuteries) est écrite dans le YAML de la carte et tourne sans Home Assistant. La configuration comprend trois réglages sans lesquels elle ne tient pas : `reboot_timeout: 0s` sous `api:`, sous `ethernet:` ou `wifi:` et sous `mqtt:` ; `restore_mode: RESTORE_DEFAULT_OFF` sur les éclairages ; mise à jour carte par carte.

<!-- schemas:fritzing:debut -->
### Câblage d'un poussoir à une charge (Fritzing)

![Câblage coloré de gauche à droite. Un poussoir mural envoie son contact sec (jaune) vers une entrée de la carte KinCony KC868-A32, et son commun vers le GND de la carte. La carte est dessinée en trois blocs : entrées à optocoupleurs EL357, ESP32 sous ESPHome, relais. Une alimentation 12 V (rouge pour le 12 V, noir pour le GND) alimente la carte. Les entrées parlent à l'ESP32, puis l'ESP32 aux relais, par des bus I2C (bleu). L'ESP32 est relié en violet à un commutateur Ethernet, lui-même relié à la passerelle Essensys. Le secteur envoie la phase (marron) au relais, dont la sortie va à une lampe, qui reçoit aussi le neutre (bleu clair).](fritzing/esphome-rail-din_breadboard.png){ loading=lazy }

Une zone, une lampe, avec les modules de la configuration résiliente. Source Fritzing : [esphome-rail-din.fzz](fritzing/esphome-rail-din.fzz){ download="esphome-rail-din.fzz" } (Fritzing 1.0.x). Principe de câblage, non validé au banc.
<!-- schemas:fritzing:fin -->

## Seule face à l'exigence

<!-- schemas:seule:debut -->
<iframe src="../archify/esphome-rail-din-seule.html?embed=1&amp;theme=light" title="Diagramme d'architecture interactif : ESPHome sur rail DIN seul, du poussoir à la charge, une carte par zone" loading="lazy" style="width:100%;aspect-ratio:1270/660;height:auto;border:0"></iframe>

[Ouvrir le diagramme en plein écran](archify/esphome-rail-din-seule.html){ target="_blank" rel="noopener" }. Le poussoir passe par les entrées de la carte, son ESP32 sous ESPHome et ses relais ; l'alimentation 12 V et le secteur arrivent par le bas ; la carte parle à un commutateur Ethernet, relié à Home Assistant, aux deux autres cartes et à la passerelle.

??? info "Image fixe du diagramme"
    ![Capture du diagramme d'architecture. De gauche à droite : 63 poussoirs muraux, entrées de la carte, ESP32 de la carte, relais de la carte, charges de la zone, les trois blocs du milieu étant dans le cadre « Carte KC868-A32 de la zone : un seul îlot, un seul GND ». Sous l'ESP32, l'alimentation 12 V ; sous les relais, le secteur 230 V. Au-dessus de l'ESP32, un commutateur Ethernet, relié à Home Assistant, aux deux autres cartes et, par MQTT, à la passerelle Essensys. Quatre cartes : règle 1 non tenue, ce qui reste panne par panne, causes communes, réserve.](archify/esphome-rail-din-seule.png){ loading=lazy }
<!-- schemas:seule:fin -->

### Les sept règles

Les [sept règles](../../resilience.md#pour-toutes-les-installations-essensys) de la réponse de résilience, lues sur la configuration résiliente :

| Règle | Tenue | Pourquoi |
| --- | --- | --- |
| 1. Pas de calculateur entre le bouton et sa charge | **Non tenue** ; logique locale par carte, mais micrologiciel du projet | La liaison `on_press` → `switch.toggle` tourne sur l'ESP32 et « marche sans Home Assistant ». Une carte morte ne prive que sa zone. Mais le micrologiciel est compilé par le projet à partir d'un YAML, pas fixé par le fabricant, et l'ordre traverse deux bus I2C internes et huit PCF8574 : la grille ne tolère que le micrologiciel fixé par le fabricant d'un module du commerce. Par défaut, la carte redémarre toutes les 15 minutes sans client (`reboot_timeout`) |
| 2. L'état vit dans un organe bistable | Non tenue | Relais monostables ; l'état est relu dans la flash au démarrage selon `restore_mode`, **`ALWAYS_OFF` par défaut** : tout s'éteint à chaque redémarrage. `RESTORE_DEFAULT_OFF` garde le dernier état, mais « tous les composants ne le respectent pas » |
| 3. La domotique ajoute, ne retire jamais | Non tenue | La carte est la domotique : Home Assistant agit sur les mêmes relais, le verrouillage des volets est logiciel (« un bogue pourrait activer les deux »), et une carte figée bloque ses boutons |
| 4. Une source et un fusible par zone, un fusible pour la domotique | Partielle | Une alimentation 12 V par carte, oui ; mais boutons, logique et relais partagent cette alimentation, et aucun fusible par voie n'est documenté |
| 5. Barrière 4 kV et 8 mm, 0 V jamais au PE, parafoudres hors coffrets | Non tenue | Le GND des entrées est celui de l'alimentation de la carte : l'optocoupleur isole l'ESP32 de la boucle, pas la boucle du reste. Aucune tension d'essai publiée pour les entrées ni pour les relais ; la déclaration CE ne cite que la directive radio |
| 6. Replis choisis au câblage, essayés à la recette | Non tenue | Les replis existent (`restore_mode`, `interlock`, `safe_mode`, `reboot_timeout`) mais vivent dans le YAML ; la recette contrôleur coupé peut les essayer |
| 7. Isolement mesuré chaque année | Tenue | Rien ne l'empêche ; les TVS éventuels de la carte ne sont pas documentés |

### Les causes communes

Dans la configuration résiliente, avec ses trois réglages :

| Défaillance unique | Prive de ses boutons… | Pourquoi |
| --- | --- | --- |
| 1. Alimentation du système | une zone | Une alimentation 12 V par carte ; la carte éteinte perd ses entrées et ses relais retombent |
| 2. Court-circuit ou ligne collée | une zone | Aucun bus de terrain ; une entrée collée vaut un appui maintenu, filtrable par `delayed_on` ; un défaut sur un bus I2C interne fige les voies de sa carte, comportement non documenté |
| 3. Contrôleur central | rien | Home Assistant n'est pas sur le chemin ; **si `reboot_timeout` est resté à 15 min, toute la maison** redémarre et s'éteint toutes les 15 minutes, redémarrages et relais réinitialisés rapportés par un utilisateur de trois KC868-A16 |
| 4. Logiciel figé | une zone | Un plantage fige sa carte ; le chien de garde de tâches de l'ESP-IDF redémarre, relais à `restore_mode`. Le même YAML tourne sur les trois cartes : un défaut de code se répète d'une zone à l'autre |
| 5. Mise à jour ratée | une zone | OTA carte par carte, retour arrière par `enable_ota_rollback`, mode sans échec après dix démarrages ratés ; pousser la même version sur les trois cartes d'un coup en fait une cause commune |
| 6. Licence, compte ou cloud | rien | Aucun : compilation locale, Home Assistant local |
| 7. Commutateur ou routeur | rien | Hors du chemin du bouton ; **mais si `reboot_timeout` d'`ethernet:` est resté à 15 min, « l'appareil redémarre »** et toute la maison s'éteint toutes les 15 minutes |
| 8. Foudre sur le chemin du bus | une zone | Pas de bus ; l'onde entre par la nappe de la zone sur la carte de la zone ; Ethernet à transformateur vers les autres ; tenue en kV non publiée |

**Total : 0 défaillance unique prive toute la maison**, 5 privent une zone, à trois conditions de paramétrage et de procédure, aucune n'étant câblée. Sans `reboot_timeout: 0s`, les défaillances 3 et 7 privent toute la maison toutes les 15 minutes : **2**. En configuration minimale, l'alimentation unique et la foudre, qui trouve un GND commun aux trois cartes, privent toute la maison : **2**, et 4 avec les deux pièges.

Ce décompte vaut ce que valent trois lignes de YAML : le redémarrage toutes les 15 minutes est le comportement par défaut, documenté sur l'API, le Wi-Fi et l'Ethernet, et un utilisateur l'a subi après avoir réglé l'API seule. La V2 obtient 0 par le câblage ; ESPHome l'obtient par la discipline.

### Ce qui reste, panne par panne

| Panne | Ce qui reste |
| --- | --- |
| Home Assistant ou le réseau | Les 63 boutons, les volets et les variateurs, par la logique de chaque carte ; perdus : distance, scènes entre cartes, horaires centralisés. À condition de `reboot_timeout: 0s` partout ; sinon redémarrage et extinction toutes les 15 minutes |
| Une carte A32 | Sa zone perd ses 20 à 22 boutons ; ses éclairages s'éteignent, ses volets s'arrêtent, ses EUD12D gardent leur niveau ; aucune commande manuelle sur l'A32, 32 boutons annoncés sur l'A32 Pro à mécanisme non trouvé. Échange de carte, puis flashage par USB ou OTA |
| Alimentation 12 V d'une zone | Idem : la zone sans boutons, éclairages éteints ; les deux autres zones indemnes |
| Coupure du secteur | Au retour, relais à `restore_mode` : éteints par défaut, dernier état avec `RESTORE_DEFAULT_OFF`, position des volets estimée |
| Carte figée | Sa zone, jusqu'au redémarrage par chien de garde ; relais à `restore_mode` |
| Mise à jour ratée | Retour au micrologiciel précédent si `enable_ota_rollback` ; mode sans échec sinon ; une carte à la fois |
| Foudre par une nappe | La carte de la zone au pire ; les deux autres par l'isolement des transformateurs Ethernet, non vérifié pour cette carte |

## En dérivation sur le filaire V2

<!-- schemas:derivation:debut -->
<iframe src="../archify/esphome-rail-din-derivation.html?embed=1&amp;theme=light" title="Diagramme d'architecture interactif : ESPHome sur rail DIN en dérivation sur le filaire V2" loading="lazy" style="width:100%;aspect-ratio:1260/680;height:auto;border:0"></iframe>

[Ouvrir le diagramme en plein écran](archify/esphome-rail-din-derivation.html){ target="_blank" rel="noopener" }. En bas, le filaire V2 : source 24 V, poussoirs, télérupteur, lampe. En haut, la couche ESPHome : passerelle qui bat le chien de garde, commutateur, trois cartes A32 sans logique, relais de garde, relais de couplage en parallèle du poussoir, relais de recopie qui renvoie l'état aux entrées des cartes.

??? info "Image fixe du diagramme"
    ![Capture du diagramme d'architecture. Cadre du bas « Filaire V2 » : source 24 V de zone, poussoirs muraux, télérupteur Finder 20.22, lampe. Cadre du haut « Couche domotique ESPHome » : commutateur Ethernet, trois cartes A32, relais de garde, relais de couplage et relais de recopie ; la passerelle Essensys, hors du cadre, est reliée au commutateur et bat le chien de garde. Les cartes envoient des impulsions au relais de garde et commandent la bobine du relais de couplage, qui ferme un contact sec en parallèle des poussoirs ; le second contact du télérupteur remonte par le relais de recopie jusqu'aux entrées des cartes. Quatre cartes : si la couche tombe, ce qu'elle apporte, ce qu'elle coûte, réserve.](archify/esphome-rail-din-derivation.png){ loading=lazy }
<!-- schemas:derivation:fin -->

Les télérupteurs, les chaînes de volets et les variateurs à entrée locale de la [V2](../v2/filaire-d-abord.md) gardent le chemin du bouton ; les cartes ne font que fermer des contacts secs et lire des recopies.

- **Sorties** : les 96 relais inverseurs de trois A32 commandent les bobines 24 V des relais de couplage 38.51 de la V2, qui ferment les contacts en parallèle des poussoirs. Les relais 10 A sont surdimensionnés pour une bobine ; les 85 sorties nécessaires tiennent dans trois cartes.
- **Entrées** : les contacts secs des relais de recopie 38.51 se ferment vers le GND de la carte, comme un poussoir ; 96 entrées pour ≈ 70 recopies.
- **Battement de cœur** : c'est **la passerelle qui réarme** le relais de garde, et la carte ne fait que relayer : la passerelle commande par l'API native, à cadence fixe, un relais dont le contact alimente la bobine du relais de garde ; si la passerelle se tait, les impulsions cessent et le chien de garde matériel de la V2 ouvre le relais en moins d'une seconde. Un `interval:` qui ferait battre ce relais depuis la carte est à proscrire : il garderait la couche branchée alors que son cerveau est mort. Si la carte redémarre, ses relais reviennent à `ALWAYS_OFF` et le relais de garde retombe : ce défaut par défaut joue ici dans le bon sens.
- **Logique** : aucune dans les cartes, qui restent des entrées-sorties ; elle est dans la passerelle, en Go par MQTT ou par l'API native, ou sous Home Assistant sur le CM5. Le double appui et l'appui long se lisent côté passerelle, sur les entrées de recopie des poussoirs.
- **Durées bornées** : par le câblage de la V2 ; ESPHome peut y ajouter un `delayed_off` par relais, sans que la V2 en dépende.

Ce que la couche apporte : ≈ 360 € HT de cartes pour 96 sorties et 96 entrées, un logiciel libre très répandu, aucune licence, un matériel que n'importe quelle carte ESP32 à relais peut remplacer. Ce qu'elle coûte : ≈ 0,96 m de platine hors rail DIN, aucune tension d'isolement publiée entre entrées, relais et logique, un marquage CE limité à la radio, et un micrologiciel compilé par le projet dans l'armoire, à tenir à jour. À comparer à la Revolution Pi Connect 5 (≈ 581 € HT nue, modules d'entrées-sorties non chiffrés ici), marquée CE et à entrées isolées. Face au serveur d'entrées-sorties Modbus ([dossier Modbus](modbus-es.md), ≈ 430 € HT), il est un peu moins cher, sans aucune logique dans l'armoire d'un côté, avec un micrologiciel à compiler de l'autre.

## Foudre et isolement

- **Pas de bus de terrain** : les cartes ne se parlent que par Ethernet, à transformateur d'isolement du LAN8720, non vérifié pour cette carte. Les nappes des poussoirs entrent directement sur les optocoupleurs EL357 de la carte de leur zone.
- **Un seul îlot par carte** : le GND des entrées est celui de l'alimentation 12 V, donc celui de l'ESP32, des PCF8574 et des bobines de relais. Les deux îlots TBTS de la V2 n'existent pas sur une A32 : la boucle des boutons et la logique partagent le même 0 V. L'optocoupleur sépare l'ESP32 de la boucle, pas la boucle du reste.
- **Tensions d'essai** : non publiées pour l'EL357 tel qu'implanté, pour les relais « 220 V / 10 A » (bobine / contact, catégorie de surtension), ni pour le circuit imprimé. La barrière de 4 kV et 8 mm de la V2 ne peut pas être affirmée ; en dérivation, les 38.51 (6 kV) la fournissent de part et d'autre.
- **Marquage CE** : la déclaration CCJS.2411163 (novembre 2024, valable jusqu'en novembre 2029, délivrée par un laboratoire de Shanghai) couvre l'A32, l'A32M, l'A32 Pro, l'A16 et l'A16v3 au titre de la seule **directive radio 2014/53/UE** (ETSI EN 301 489-1 et -17, EN 300 328). Aucune norme de sécurité électrique (directive basse tension, EN 62368-1, EN 60669) ni de CEM filaire n'y figure.
- **Parafoudres et règles de pose** : aucune recommandation trouvée chez KinCony ni dans la documentation ESPHome.

## Logiciel, paramétrage et passerelle Essensys

| Point | Ce qu'on a trouvé |
| --- | --- |
| Outil | ESPHome : YAML compilé en micrologiciel, en module Home Assistant ou en ligne de commande ; gratuit ; les YAML d'exemple des A32 et A16 sont publiés (adresses I2C, inversion des entrées-sorties, pilote LAN8720) |
| Compétence | Édition YAML, notions de GPIO et d'I2C ; aucune formation payante |
| Mise à jour | OTA par le réseau ou flashage USB ; `safe_mode` installé par défaut avec l'OTA ; `enable_ota_rollback` sur ESP32 confirme ou annule après `boot_is_good_after` (1 min) |
| Réglages de survie | `reboot_timeout: 0s` sous `api:`, `wifi:` ou `ethernet:` et `mqtt:` ; `restore_mode` par relais ; `interlock` et `interlock_wait_time` ; `on_click`, `on_double_click`, `on_multi_click` pour les appuis |
| Sécurité | API native chiffrée par clé de 32 octets ; `outgoing_connection` pour que la carte appelle Home Assistant |
| API pour la passerelle | API native (TCP) ou MQTT via un courtier local ; bibliothèque `aioesphomeapi` en Python, non vérifiée ; bibliothèque Go non trouvée par cette étude ; RS-485 Modbus RTU présent sur la carte, non étudié |
| Home Assistant | Intégration native ; openHAB par MQTT, non étudié |
| Micrologiciels de rechange | Tasmota, KCS (KinCony), Arduino, ESP-IDF, MicroPython, Zephyr (carte `kincony_kc868_a32` reconnue) |
| Cloud | Aucun ; compilation et exploitation locales |

Côté passerelle, le backend Go parlerait aux cartes par MQTT, le plus simple, ou par l'API native s'il existe une bibliothèque Go, non trouvée. La note ne chiffre pas ce travail ; en lecture « seule », la logique de chaque zone s'écrit en YAML et celle des scènes dans Home Assistant, et c'est du logiciel du projet dans l'armoire, ce que la V2 refuse sur le chemin d'un bouton.

## Nomenclature et coût estimé

La boutique du fabricant a refusé les consultations directes (erreur 429) ; le prix de l'A32 vient de résumés de recherche de sa page de collection, « à partir de 130 $ », vraisemblablement hors taxes et hors port. Conversion ≈ 360 € pour trois cartes au change du jour, non vérifiée. AliExpress et Amazon n'ont pas pu être consultés. Les variateurs sont repris du dossier Modbus au prix boutique de 43,45 € HT (51,70 € TTC chez zaehlerschrank24, le prix retenu par la V2) ; le prix catalogue Eltako est de 89,37 € HT.

### Configuration minimale

| Poste | Référence | Qté | Prix unitaire HT | Total HT | Source |
| --- | --- | --- | --- | --- | --- |
| Entrées et relais | KinCony KC868-A32 | 3 | « à partir de 130 $ » (≈ 120 €) | ≈ 390 $ (≈ 360 €) | boutique KinCony, via résumé |
| Variateurs | Eltako EUD12D-UC | 8 | 43,45 € (51,70 € TTC ; catalogue Eltako 89,37 € HT) | ≈ 348 € | zaehlerschrank24, dossier [Modbus](modbus-es.md) |
| Alimentation 12 V | — | 1 | non chiffrée | non chiffrée | consommation non trouvée |
| Commutateur Ethernet | — | 1 | non chiffré | non chiffré | — |
| Hôte Home Assistant | CM5 existant | 1 | 0 € | 0 € | — |
| **Matériel** | | | | **≈ 710 € HT**, estimé, hors alimentation et commutateur | |
| Logiciel | ESPHome, Home Assistant | | 0 € | 0 € | licences libres |
| **Total** | | | | **≈ 710 € HT**, estimé | |

Hors du total : port, droits de douane et TVA d'import depuis la Chine, non chiffrés. La variante deux A32 et une A16 n'est pas chiffrée, le prix de l'A16 n'ayant pas été trouvé.

### Configuration résiliente

| Poste | Référence | Qté | Prix unitaire HT | Total HT |
| --- | --- | --- | --- | --- |
| Entrées et relais, une carte par zone | KinCony KC868-A32 | 3 | ≈ 120 € | ≈ 360 € |
| Variateurs | Eltako EUD12D-UC | 8 | 43,45 € | ≈ 348 € |
| Alimentations 12 V, une par zone | — | 3 | non chiffrées | non chiffrées |
| Commutateur Ethernet | — | 1 | non chiffré | non chiffré |
| **Matériel** | | | | **≈ 710 € HT**, estimé |
| Logiciel | | | 0 € | 0 € |
| **Total** | | | | **≈ 710 € HT**, estimé, plus deux alimentations |

La configuration résiliente ne coûte que deux alimentations de plus que la minimale : le découpage par zone est gratuit en cartes, puisqu'il en faut trois dans les deux cas.

### Couche domotique en dérivation

| Poste | Référence | Qté | Total HT |
| --- | --- | --- | --- |
| 96 contacts inverseurs vers les bobines des 38.51, 96 entrées de recopie | KinCony KC868-A32 | 3 | ≈ 390 $ (≈ 360 €) |
| Alimentation 12 V, commutateur | — | | non chiffrés |
| **Matériel** | | | **≈ 360 € HT**, estimé |
| Logiciel | ESPHome | | 0 € |
| **Total** | | | **≈ 360 € HT**, ≈ 0,96 m de platine |

Les relais de couplage et de recopie 38.51, le relais de garde et les bornes sectionnables sont déjà dans la V2 et ne sont pas recomptés.

### Ce qui n'est pas dans les totaux

- **Fonctions à reporter** : alarme, rien de natif, entrées libres sur les cartes ; écran, aucun sur l'A32, un afficheur d'adresses IP sur l'A32 Pro ; délestage, aucune mesure de courant sur l'A32, compteurs externes du fabricant (70 à 200 $) non étudiés.
- **Fil pilote** : un relais par ordre, sans module dédié.
- **Électricien** : non estimé par la note ; les cartes remplacent télérupteurs et relais, mais demandent une platine et des borniers intermédiaires.
- **Logiciel** : non estimé par la note ; YAML par carte, logique de zone, scènes Home Assistant, liaison avec la passerelle.
- **Place** : ≈ 0,96 m de platine pour trois A32, hors rail DIN modulaire ; dans les deux lectures.
- **Import** : port, droits et TVA depuis la Chine.

## Ouverture et pérennité

- **Logiciel ouvert** : ESPHome sous GPLv3 et MIT, 11,9 k étoiles sur GitHub, porté par l'Open Home Foundation avec plus de 240 projets ; Home Assistant ouvert ; MQTT ouvert. Toute carte ESP32 à relais fonctionne sous ESPHome : KinCony n'est pas incontournable, et le site des appareils en recense de nombreux fabricants.
- **Matériel documenté** : schémas publiés par KinCony, « protocole ouvert » et code d'exemple revendiqués, A32 reconnue par Zephyr.
- **Fabricant** : petite société chinoise de 2007, cycles de révision rapides (A8v3, A16v3, A32 Pro en 2024) ; disponibilité des pièces à dix ans non trouvée ; l'ESP32 classique reste produit par Espressif, non vérifié ici. Les gammes de 2020 (séries H, COL) restent en ligne mais ne sont plus mises en avant.
- **Cloud** : aucun ; KinCony vend aussi un pilotage local sans Internet ; l'Open Home Foundation se positionne contre la dépendance au cloud.
- **Communauté** : forum KinCony actif, réponses de l'administrateur de 2023 à 2026 ; forum Home Assistant ; documentation ESPHome détaillée.
- **Alternatives notées** : Sonoff SPM (jusqu'à 128 relais 20 A avec mesure, unité principale 76 à 91 € TTC), cartes Waveshare Modbus (voir le [dossier Modbus](modbus-es.md)).

## Verdict

- **Seule** : trois cartes à 130 $ reprennent toute l'armoire, et chaque zone marche sans Home Assistant. Mais le lien du bouton à sa charge est un micrologiciel du projet, pas celui, fixé par le fabricant, d'un module du commerce : règle 1 non tenue. L'état vit dans ce micrologiciel, les relais s'éteignent à chaque redémarrage, et le redémarrage toutes les 15 minutes est le comportement par défaut : la maison tient par trois lignes de YAML, pas par le câblage. Aucun isolement chiffré, un CE radio seulement. C'est la refonte Raspberry Pi des V1 en moins cher et en moins documenté, pas une réponse à l'exigence.
- **En dérivation** : la couche d'entrées-sorties la moins chère en cartes, ≈ 360 € HT, que les 38.51 et le relais de garde de la V2 rendent acceptable ; un micrologiciel à compiler et à maintenir, et un encombrement hors rail DIN.
- **À qui elle convient** : à qui sait écrire du YAML et accepte un matériel peu documenté derrière une couche filaire qui, elle, tient l'exigence ; pas à qui veut une armoire qu'un électricien reprend.

## Sources

Toutes consultées le 24 octobre 2026.

1. [KinCony, « About us »](https://www.kincony.com/about-us) : fondée en 2007, gamme.
2. [GitHub esphome/esphome](https://github.com/esphome/esphome) et [licence](https://github.com/esphome/esphome/blob/dev/LICENSE) : description, 11,9 k étoiles, GPLv3 et MIT.
3. [CNX Software, Open Home Foundation](https://www.cnx-software.com/2024/04/23/open-home-foundation-manage-home-assistant-esphome-zigpy-over-240-open-source-smart-home-projects/) et [notes de version ESPHome 2024.6.0](https://esphome.io/changelog/2024.6.0/) : don d'ESPHome à la fondation.
4. [ESPHome, automatisations](https://esphome.io/automations/actions.html) : logique locale sans réseau, exemple `on_press` → `switch.toggle`.
5. [Zephyr, carte KinCony KC868-A32](https://docs.zephyrproject.org/latest/boards/kincony/kincony_kc868_a32/doc/index.html) : ESP-WROOM-32, 32 entrées, 32 relais 220 V / 10 A, Ethernet, RS-485, 12 V.
6. [KinCony, matériel de l'A32](https://www.kincony.com/a32-esp32-board-hardware.html) : EL357, PCF8574P, ULN2003A, 320 × 122 mm, profilé ouvert, charges inductives.
7. [devices.esphome.io, KC868-A32](https://devices.esphome.io/devices/kincony-kc868-a32/) et [KC868-A16](https://devices.esphome.io/devices/kincony-kc868-a16/) : YAML d'exemple, adresses I2C.
8. [KinCony, annonce A32 Pro](https://www.kincony.com/2024/04/14) : ESP32-S3, 32 boutons manuels, 0-10 V.
9. [Forum KinCony, tension d'entrée de l'A32](https://www.kincony.com/forum/showthread.php?pid=7938) : contact vers GND, niveaux selon l'alimentation, A32M pour 24 V.
10. [Forum KinCony, niveaux 0-4 V et 6-12 V](https://kincony.com/forum/showthread.php?tid=3028) : avertissement 24 et 48 V.
11. [Forum KinCony, GND des groupes d'entrées](https://www.kincony.com/forum/showthread.php?tid=9223) : tous les GND reliés.
12. [KinCony, paramètres KC868 2020](https://www.kincony.com/download/KC868-Smart-Controller-parameters-V202006.pdf) : série H, D8, mémoire d'état, pilotage local.
13. [ESPHome, GPIO Switch](https://esphome.io/components/switch/gpio.html) : `interlock` logiciel, recommandation de verrouillage matériel.
14. [ESPHome, Time Based Cover](https://esphome.io/components/cover/time_based.html) : actions, durées, restauration.
15. [ESPHome, Switch](https://esphome.io/components/switch/index.html) : `restore_mode`, défaut `ALWAYS_OFF`.
16. [ESPHome, Binary Sensor](https://esphome.io/components/binary_sensor/index.html) : `on_click`, `on_multi_click`, filtres.
17. [ESPHome, API native](https://esphome.io/components/api.html) : `reboot_timeout` 15 min, `0s`, chiffrement, `outgoing_connection`.
18. [ESPHome, Wi-Fi](https://esphome.io/components/wifi.html) et [Ethernet](https://esphome.io/components/ethernet.html) : `reboot_timeout`, « l'appareil redémarre ».
19. [Forum KinCony, « Esphome restart stand alone »](https://www.kincony.com/forum/showthread.php?tid=8731) : redémarrages sans Home Assistant, relais réinitialisés.
20. [esp32.co.uk, relais sous ESPHome](https://esp32.co.uk/?p=1842) : `RESTORE_DEFAULT_OFF`, broches tirées au démarrage.
21. [Forum KinCony, état des relais après coupure (KCS)](https://kincony.com/forum/printthread.php?tid=9653) : relais à l'arrêt au redémarrage.
22. [Industrial Shields, chien de garde ESP32](https://www.industrialshields.com/plc-solution-library/esp32-plc-hardware-watchdog-reliability) : redémarrage complet.
23. [ESPHome, Safe Mode](https://esphome.io/components/safe_mode.html) : `num_attempts`, `boot_is_good_after`, `enable_ota_rollback`.
24. [KinCony, déclaration CE CCJS.2411163](https://www.kincony.com/images/patent/CCJS.2411163.pdf) : directive radio, normes ETSI, modèles couverts, validité.
25. [KinCony, certificat CRZJ21050630792](https://www.kincony.com/images/patent/CRZJ21050630792_CE.pdf) et [fil CE 2026](https://kincony.com/forum/showthread.php?tid=8979).
26. [Boutique KinCony, collection KC868-A](https://shop.kincony.com/collections/kc868-ax) : A32 « à partir de 130 $ », via résumé, page inaccessible en direct.
27. [KinCony, pages produit A32](https://www.kincony.com/arduino-esp32-32-channel-relay-module-kc868-a32.html) et [A16](https://www.kincony.com/arduino-esp32-16-channel-relay-module-2.html) : schémas, micrologiciels.
28. [Sonoff SPM chez Domadoo](https://www.domadoo.fr/en/good-deals/5928-sonoff-rail-din-intelligent-power-meter-main-unit.html) : 76 à 91 € TTC.
29. [Eltako, notice EUD12D-UC](https://www.eltako.com/fileadmin/downloads/de/_bedienung/EUD12D_21100905-3_dt.pdf) : variateur universel à entrée poussoir, prix catalogue 89,37 € HT ; [zaehlerschrank24, EUD12D-UC](https://www.zaehlerschrank24.de/multi-dimmschalter-eud12d-uc.html) : 51,70 € TTC, soit 43,45 € HT.

!!! note "À confirmer auprès des fabricants"
    Les prix de l'A32 Pro, de l'A16, du D8 et de l'A32M, le port et les droits ; la tension d'isolement des entrées EL357 telles qu'implantées, le courant de boucle, le filtrage et la longueur de nappe admise ; la référence des relais, leur tension d'essai bobine / contact, leur tenue à l'appel des LED ; la compatibilité rail DIN du profilé et la consommation 12 V d'une A32 relais collés ; le mécanisme des 32 boutons de l'A32 Pro ; l'existence d'un rapport de sécurité électrique au-delà de la directive radio ; l'effet d'un défaut I2C sur les relais ; un chien de garde matériel sous ESPHome ; la tension de commande de l'EUD12D-UC par un relais de l'A32 ; la disponibilité de l'A32 à cinq et dix ans.
