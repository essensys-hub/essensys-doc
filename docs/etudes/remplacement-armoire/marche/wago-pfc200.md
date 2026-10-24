---
title: "Wago PFC200 : remplacer l'armoire sans recâblage"
description: "Automate Wago PFC200 ou Compact Controller 100 avec bornes WAGO-I/O-SYSTEM 750 pour remplacer les quatre cartes de l'armoire ESSENSYS sans toucher aux fils : entrées 24 V pour les 63 poussoirs, bornes relais, coupleurs Modbus TCP par zone. Seul, un automate centralisé reste entre chaque bouton et sa charge ; en dérivation, une couche d'entrées-sorties industrielle, ouverte mais chère. Environ 7 270 € HT en configuration par zone, hors postes non chiffrés."
---

# Wago PFC200

Wago est l'automate industriel ouvert du [comparatif](index.md) : un contrôleur Linux programmé en CODESYS, suivi de bornes d'entrées-sorties enfichées sur un bus interne qui ne sort pas de l'armoire. La V2 emploie déjà du matériel Wago. La question est la même que pour les autres : peut-il reprendre les 63 poussoirs et toutes les charges sans changer un fil, et que reste-t-il quand l'automate s'arrête ?

!!! abstract "Synthèse"
    - **Seule** : Wago remplace les quatre cartes sans recâblage, en passant la boucle des poussoirs de 5 V à 24 V. Mais toute la logique est dans un seul contrôleur : les bornes n'ont pas de logique propre, et les coupleurs de zone 750-362 non plus. **Règle 1 non tenue.** Si le programme ne rafraîchit pas le bus interne dans les 50 ms, les sorties passent en repli, c'est-à-dire à zéro. En configuration par zone, **5 des huit défaillances uniques privent toute la maison de ses boutons** ; le découpage en trois nœuds ne donne aucune autonomie aux zones. La seule commande à la main est le sélecteur manuel de la borne 16 A 750-523, qui enclenche même sans 24 V.
    - **En dérivation** : une couche d'entrées-sorties industrielle, à protocoles ouverts (Modbus TCP, MQTT), dont le repli à 50 ms sert naturellement de battement de cœur au relais de garde. Elle coûte environ deux fois la couche KNX et bien plus qu'un serveur d'entrées-sorties Modbus, pour rendre le même service ; à comparer à la Revolution Pi Connect 5 (≈ 581 € HT nue, modules d'entrées-sorties non chiffrés ici).
    - **Coût estimé** : ≈ 6 250 € HT en configuration minimale, ≈ 7 270 € HT par zone, ≈ 6 350 € HT en couche domotique seule, **hors alimentation 24 V, fin de bus, modules d'alimentation du bus et relais d'interface, dont les prix n'ont pas été trouvés**. Le prix du PFC200 750-8212 lui-même n'a pas été trouvé : les totaux reposent sur le Compact Controller 100. Prix d'octobre 2026, RS France (HT) et Bürklin (TTC à 19 %, converti).
    - **Réserve** : estimations à confirmer par un électricien, des devis, le fabricant et des essais. Les manuels du 750-362 et du PFC200 n'ont pas pu être consultés ; le comportement à la perte du maître vient d'un manuel générique et d'un document tiers.

## Principe et gamme

Le WAGO-I/O-SYSTEM 750 est un système d'automatisme modulaire : un contrôleur, ou un coupleur de bus de terrain, en tête de rail, suivi de bornes d'entrées-sorties de 12 ou 24 mm enfichées côte à côte. Un bus interne, le K-Bus, relie les bornes au contrôleur dans l'embase ; des contacts de puissance traversants distribuent le 24 V de terrain d'une borne à la suivante. Jusqu'à 64 bornes par nœud sans extension, 250 avec.

Le système est **centralisé** : le programme IEC 61131-3 (CODESYS) du contrôleur lit toutes les entrées et écrit toutes les sorties à chaque cycle. Les bornes n'ont aucune logique propre. Le contrôleur **750-8212** (PFC200, deuxième génération) porte un Cortex-A8 à 1 GHz, 512 Mo de RAM, 4 Go de flash, un Linux temps réel, deux ports Ethernet et une liaison série ; il fournit au plus 1 700 mA au bus interne 5 V. Le **751-9301** (Compact Controller 100) est un automate compact à 8 entrées, 4 sorties et 2 ports Ethernet, sans K-Bus direct : il s'étend par un coupleur Modbus TCP **750-362**, lequel expose les bornes d'un nœud distant au maître. Les versions actuelles se programment en CODESYS V3.5 à partir du micrologiciel 23 ; e!COCKPIT servait jusqu'au micrologiciel 22.

Fabricant : Wago, Minden (Allemagne). Fiches consultées datées de 2010 à 2024 ; la date de lancement de la série 750 n'a pas été trouvée.

## Dans l'armoire sans recâblage

Les poussoirs sont des contacts secs : des bornes d'entrées 24 V les lisent, et le K-Bus reste dans l'armoire. La boucle actuelle de 5 V devient une boucle de 24 V continu à 2 à 2,5 mA par entrée, ce que les jonctions IDC données pour 1 A acceptent. Aucune longueur de ligne admise n'est publiée sur la fiche des entrées.

| Fonction | Module | Voies | Largeur | Ce qu'il faut savoir |
| --- | --- | --- | --- | --- |
| 63 poussoirs | 750-1405 | 16 entrées 24 V | 12 mm | Niveau 1 de 15 à 30 V, filtre 3 ms, 2,1 à 2,4 mA par entrée ; optocoupleur entre bus et terrain, isolement 500 V ; +24 V et 0 V communs aux 16 voies ; 25 mA sur le bus 5 V |
| | 750-1415 | 8 entrées | — | Même famille, pour un découpage par zone ; fiche non consultée |
| Éclairages, cumulus, machines | 750-523 | 1 contact NO 16 A | 24 mm | Libre de potentiel ; **sélecteur manuel/automatique en face avant** : en manuel, la bobine est coupée et le contact s'enclenche « même sans alimentation 24 V » ; consommation bus et isolement non trouvés |
| Éclairages, volets, variateurs, divers | 750-517 | 2 relais inverseurs libres de potentiel | 12 mm | 250 V CA / 1 A, 40 V CC / 1 A ; isolement 1 500 V ; 90 mA sur le bus 5 V ; 1 A par contact : pas de commande directe d'un circuit protégé à 16 A ni d'un moteur de volet au-delà de 230 W, relais d'interface en aval |
| | 750-514 | 2 relais | — | Fiche non consultée |
| 8 variateurs | aucun module 230 V identifié | | | Options : contact 750-517 sur l'entrée d'un variateur universel externe, sortie 0-10 V (750-559) ou maître DALI (753-647) ; fiches non consultées |
| Alimentation 24 V | 787-1602 | 2,5 A | — | Prix et fiche non trouvés |
| Fin de bus | 750-600 | | ≈ 12 mm, à vérifier | Obligatoire en fin de nœud |
| Alimentation du bus interne | 750-613 | | — | Référence attendue, **non vérifiée** ; nécessaire si les bornes dépassent le courant du contrôleur |
| Contrôleur | 750-8212 | 2 Ethernet, série | 78,6 mm | 1 700 mA au bus 5 V ; 64 bornes sans extension ; isolement 500 V ; mémoire rémanente 128 Ko |
| Contrôleur compact | 751-9301 | 8 DI, 4 DO, 2 AI, 2 AO | 108 mm | Pas de K-Bus direct : s'étend par un 750-362 ; CODESYS 3.5 « sans frais » selon un distributeur |
| Coupleur de zone | 750-362 | Modbus TCP/UDP | non trouvée | 64 bornes sans extension ; deux ports Ethernet à commutateur intégré ; adresse IP par commutateur DIP ; **aucune logique** |

Le piège de la gamme est le **courant du bus interne 5 V** : 43 bornes 750-517 consomment 3 870 mA, les quatre 750-1405 100 mA de plus, contre 1 700 mA fournis par le PFC200. Il faut deux ou trois modules d'alimentation du bus, dont la référence et le prix n'ont pas été vérifiés. Le courant disponible sur un 750-362 n'a pas été trouvé.

### Configuration minimale

Un contrôleur, un nœud, une alimentation 24 V : un 750-8212, quatre 750-1405 (64 entrées), 43 bornes 750-517 (86 contacts pour 75 à 85 sorties), une fin de bus, deux ou trois modules d'alimentation du bus. **47 bornes, soit ≈ 0,65 m de rail hors alimentation**, en dessous des 64 bornes qui imposeraient une extension de bus. Avec un Compact Controller 100 à la place du PFC200, il faut ajouter un 750-362 pour porter le K-Bus : ≈ 0,75 m. Les relais d'interface 230 V derrière les contacts 1 A ne sont pas comptés.

### Configuration résiliente

Un maître en tête (750-8212 ou 751-9301) et **trois nœuds de zone**, chacun porté par un coupleur 750-362, avec ses entrées, ses sorties, sa fin de bus et sa propre alimentation 24 V, reliés au maître par Ethernet en ligne, grâce aux commutateurs intégrés des coupleurs.

| Nœud | Bornes | Largeur hors coupleur |
| --- | --- | --- |
| Maître | 751-9301 ou 750-8212 | 108 mm ou 78,6 mm |
| Pièces de vie (20 poussoirs, 5 éclairages, 6 volets, 3 variateurs, divers) | 750-362, 2 × 750-1405, 15 × 750-517, 750-600 | ≈ 216 mm |
| Chambres (21, 7, 5, 4) | 750-362, 2 × 750-1405, 13 × 750-517, 750-600 | ≈ 192 mm |
| Pièces d'eau (22, 13, 4 dont le store, 1) | 750-362, 2 × 750-1405, 15 × 750-517, 750-600 | ≈ 216 mm |

Les 43 bornes relais de la configuration minimale sont réparties par zone avec la même réserve (86 contacts pour 75 à 85 sorties) : les charges ne changent pas d'une configuration à l'autre. Les largeurs comptent les bornes d'entrées, les bornes relais et la fin de bus 750-600, chacune à 12 mm (largeur du 750-600 à vérifier). **≈ 0,85 à 0,9 m de rail** avec les trois coupleurs (largeur non trouvée, de l'ordre de 50 à 60 mm chacun) et le maître, hors alimentations. Chaque nœud consomme 1 220 à 1 400 mA sur son bus 5 V, à comparer au courant du 750-362, non trouvé. La fiche du coupleur n'impose pas une alimentation par nœud : c'est un choix d'installation.

Cette configuration **ne découpe que le matériel, pas la logique** : les trois coupleurs restent des esclaves d'un maître unique, qui lit toutes les entrées et écrit toutes les sorties.

## Seule face à l'exigence

### Les sept règles

| Règle | Tenue | Pourquoi |
| --- | --- | --- |
| 1. Pas de calculateur entre le bouton et sa charge | **Non tenue** | Le poussoir attaque une borne d'entrées sans logique ; le programme du contrôleur écrit la sortie. Les coupleurs 750-362 n'ont pas de logique non plus. Seul le sélecteur manuel du 750-523 commande un contact sans l'automate |
| 2. L'état vit dans un organe bistable | Non tenue | Les relais des bornes sont monostables et passent à zéro en repli ; l'état vit dans le programme, qui dispose d'une mémoire rémanente de 128 Ko mais doit lui-même le restituer |
| 3. La domotique ajoute, ne retire jamais | Non tenue | L'automate **est** le seul chemin ; un programme faux ou un ordre Modbus faux commute n'importe quelle voie |
| 4. Une source et un fusible par zone, un fusible pour la domotique | Partielle | Une alimentation 24 V par nœud est possible ; Wago impose de séparer l'alimentation du système et celle du terrain, et une protection externe contre les surintensités. Mais l'alimentation du maître est commune, et rien ne sépare « boutons » et « domotique » : c'est le même bus |
| 5. Barrière 4 kV et 8 mm, 0 V jamais au PE, parafoudres hors coffrets | Non tenue | Isolement 500 V entre bus et terrain sur les entrées et le contrôleur, 1 500 V sur les relais 750-517 ; 0 V commun aux 16 entrées d'une borne ; catégorie de surtension et tension d'essai en kV non trouvées ; aucune recommandation de parafoudre trouvée |
| 6. Replis choisis au câblage, essayés à la recette | Partielle | Le repli existe et il est déterministe : sorties à zéro après 50 ms sans rafraîchissement. Mais il est le même pour toutes les voies et ne se choisit pas au câblage ; une source secondaire indique qu'il n'est pas réglable borne par borne |
| 7. Isolement mesuré chaque année | Tenue | Rien ne l'empêche ; le contrôleur journalise les erreurs de bus interne par son interface web |

### Les causes communes

Dans la configuration résiliente, la liste fermée du comparatif donne :

| Défaillance unique | Prive de ses boutons… | Pourquoi |
| --- | --- | --- |
| 1. Alimentation du système | toute la maison | L'alimentation du maître fait tomber le maître ; les coupleurs détectent la perte du bus de terrain et passent leurs sorties à zéro (manuel générique). L'alimentation d'un nœud ne prive que sa zone |
| 2. Court-circuit ou ligne collée | toute la maison | Un défaut sur la liaison Ethernet du maître, ou sur le K-Bus de tête d'un PFC200, arrête le maître ; une source secondaire indique qu'une erreur de K-Bus met le runtime en STOP. Un défaut sur le K-Bus d'un nœud de zone ne prive que sa zone |
| 3. Contrôleur central | toute la maison | Un seul maître ; les coupleurs n'ont pas de logique |
| 4. Logiciel figé | toute la maison | Si le programme ne rafraîchit pas le bus interne dans les 50 ms, les sorties passent en repli (document ADI/DAL cité par un tiers) ; aucun chien de garde matériel ni redémarrage automatique trouvé |
| 5. Mise à jour ratée | toute la maison | Un seul micrologiciel, un seul programme ; comportement en cas d'échec non trouvé |
| 6. Licence, compte ou cloud | rien | Aucun cloud en exploitation ; la licence du runtime est une question de mise en service (voir plus bas) |
| 7. Commutateur ou routeur | rien | Si les coupleurs sont chaînés par leurs commutateurs intégrés, aucun commutateur externe n'est sur le chemin ; avec un commutateur externe, il priverait toute la maison |
| 8. Foudre sur le chemin du bus | une zone | Le K-Bus et l'Ethernet restent dans l'armoire ; l'onde entre par une ligne de poussoir et frappe la borne d'entrées de la zone, isolée à 500 V seulement : la tenue du coupleur et de l'Ethernet n'est pas chiffrée |

**Total : 5 défaillances uniques privent toute la maison**, 1 prive une zone. En configuration minimale, la foudre frappe le seul nœud : **6**.

Ce décompte dit l'essentiel : le découpage en trois coupleurs rapproche le matériel de la V2, mais pas la logique. Le PFC200 reproduit l'architecture de l'étude V1 Revolution Pi, un contrôleur unique entre les boutons et les charges, avec des bornes industrielles au lieu de modules DIO. Pour donner une autonomie aux zones, il faudrait un contrôleur par zone, soit trois PFC200 ou trois Compact Controller 100 chacun avec son coupleur : la gamme le permet, le coût non chiffré du PFC200 en décide.

### Ce qui reste, panne par panne

| Panne | Ce qui reste |
| --- | --- |
| Contrôleur arrêté, runtime stoppé ou figé | Rien au bouton. Sorties à zéro en 50 ms : lumières éteintes, volets arrêtés, fil pilote selon le câblage du repli. Les 750-523 en position manuelle restent enclenchés |
| Alimentation 24 V d'un nœud de zone | Les deux autres zones. Dans la zone touchée : rien au bouton, sorties à zéro |
| Coupleur 750-362 ou son K-Bus | Idem, pour sa zone ; redémarrage du nœud par coupure de l'alimentation après réparation (manuel générique) |
| Liaison Ethernet du maître | Rien au bouton, dans les trois zones |
| Passerelle ou réseau local | Tout le local : le programme de l'automate ne dépend pas de la passerelle ; perdue : l'application |
| Coupure du secteur | Tout s'arrête ; au retour, le programme restitue ou non les états, selon ce qu'il a été écrit pour faire |
| Une borne | Ses voies ; échange borne par borne, l'adressage suivant la position sur le rail |
| Foudre par une ligne de poussoir | La borne d'entrées de la zone au moins ; au-delà, l'isolement de 500 V ne garantit rien |

## En dérivation sur le filaire V2

Dans cette lecture, les télérupteurs, les chaînes de volets et les variateurs à entrée locale gardent le chemin du bouton. Wago fournit la couche domotique :

- **Sorties** : 43 bornes 750-517 (86 contacts inverseurs, 1 A sous 40 V continu) commandent les bobines 24 V des relais de couplage 38.51 de la V2, qui ferment les contacts secs en parallèle des poussoirs. La charge d'une bobine est très en dessous du minimum de 12 V / 100 mA des contacts, à vérifier au banc.
- **Entrées** : cinq 750-1405 (80 entrées 24 V) lisent les contacts des relais de recopie, qui ferment la boucle 24 V de la borne.
- **Battement de cœur** : le programme CODESYS bat sur un contact 750-517 qui tient la bobine du relais de garde. **C'est le contrôleur qui réarme le chien de garde.** Si le runtime s'arrête ou se fige, le repli à 50 ms ouvre le contact et le relais de garde retombe : ce comportement, fixé par le système, est ici un avantage. Si la **passerelle** se tait, l'automate continue de battre : le programme doit explicitement cesser de battre quand la passerelle ne lui a rien dit depuis un délai, sinon la couche reste armée sans personne pour la piloter.
- **Logique et interface utilisateur** : la passerelle, par Modbus TCP ou MQTT. L'automate peut porter la logique des horaires et des scénarios, ou n'être qu'un serveur d'entrées-sorties ; dans ce second cas, c'est l'architecture du serveur d'entrées-sorties léger de la V2, avec un automate industriel à la place.
- **Durées bornées** : le câblage de la V2 les borne ; le programme peut les borner aussi, mais un relais soudé y échappe.

Ce que la couche apporte : des bornes industrielles à ressort, un protocole Modbus TCP que tout parle, un micrologiciel et un kit de développement publiés par le fabricant, des pièces que l'industrie achète encore dans dix ans. Ce qu'elle coûte : ≈ 6 350 € HT hors alimentation, soit **environ deux fois la couche KNX** (≈ 3 100 € HT), à comparer à la Revolution Pi Connect 5 (≈ 581 € HT nue, modules d'entrées-sorties non chiffrés ici), pour ≈ 0,75 m de rail en plus de la couche filaire, un Linux à maintenir dans l'armoire et CODESYS à apprendre. Les 43 bornes relais 1 A sont surdimensionnées en isolement et sous-dimensionnées en courant pour tout autre usage que des bobines. Face au serveur d'entrées-sorties léger ([dossier Modbus](modbus-es.md)), Wago est nettement plus cher pour la même fonction ; son avantage est la qualité industrielle du matériel et le repli à 50 ms garanti par le système.

## Foudre et isolement

- **Le bus reste dans l'armoire** : le K-Bus vit dans l'embase des bornes, l'Ethernet entre nœuds dans le coffret. Les nappes des poussoirs portent le 24 V de terrain des bornes d'entrées, référencé à l'alimentation 24 V ; elles restent en TBTS si cette alimentation est SELV, comme Wago le demande (« seules des sources SELV/PELV »).
- **Tensions d'essai** : 500 V entre système et terrain sur le 750-1405 et le 750-8212, 1 500 V sur le 750-517 ; valeurs du 750-523 et du 750-362 non trouvées ; aucune catégorie de surtension, aucune tension d'essai en kV sur les fiches lues. La barrière de 4 kV et 8 mm de la V2 **n'est pas atteinte** par les bornes : en lecture seule, l'onde qui entre par une ligne de poussoir trouve 500 V entre elle et le K-Bus. En dérivation, les relais de couplage 38.51 (6 kV) et de recopie portent la barrière, comme la V2 le prévoit.
- **Communs** : les 16 entrées d'un 750-1405 partagent le même +24 V et le même 0 V ; il n'y a pas de groupes isolés dans une borne. Les contacts d'un 750-517 sont isolés entre eux.
- **Alimentations séparées** : Wago impose de séparer l'alimentation du système (bus interne) et celle du terrain (contacts des entrées, bobines), pour que le bus survive à un court-circuit côté actionneurs, et une protection externe contre les surintensités « car la plupart des composants n'ont pas de protection interne ».
- **Parafoudres** : aucune recommandation Wago trouvée dans les documents consultés.

## Logiciel, paramétrage et passerelle Essensys

| Point | Ce qu'on a trouvé |
| --- | --- |
| Outil | **CODESYS V3.5** à partir du micrologiciel 23 (e!COCKPIT jusqu'au 22) ; langages IEC 61131-3 : IL, LD, FBD, CFC, ST, SFC. Prix des licences d'atelier e!COCKPIT non trouvés |
| Licence du runtime | « Sans frais » pour le Compact Controller 100 selon un distributeur ; pour le 750-8212, une source secondaire rapporte des unités livrées sans licence de runtime (« The project requires software license »). **À confirmer auprès de Wago.** BACnet/IP, EtherCAT maître et MQTT Sparkplug demandent des licences supplémentaires |
| Formation | Automaticien ou apprentissage de CODESYS ; forums CODESYS Forge et sps-forum |
| Mise à jour | Micrologiciel par l'interface web ou carte SD ; micrologiciels et kit de développement publiés sur GitHub par Wago ; comportement en cas de mise à jour ratée non trouvé |
| Sécurité | SSH, HTTPS, FTPS, SNMP ; OpenVPN, IPsec et pare-feu intégré d'après un article de 2018 |
| API pour la passerelle | **Modbus TCP/UDP** et Modbus RTU, MQTT, OPC UA serveur et client, EtherNet/IP ; serveur web et Web Visu. Un conteneur Docker et une « Open Source Kbus API » en MQTT existent, mais exigent d'arrêter le runtime CODESYS : le K-Bus n'a qu'un maître, et la règle des 50 ms s'applique alors au conteneur |
| Home Assistant, openHAB | Aucune intégration Wago native trouvée ; passage par Modbus TCP ou MQTT |
| Cloud | Aucune dépendance ; un « WAGO Cloud » optionnel existe, non étudié |

Côté passerelle, le backend Go doit parler Modbus TCP ou MQTT à l'automate, et le programme CODESYS doit exposer entrées, sorties et battement de cœur. L'estimation de cette étude, sans source, est de **quatre à huit semaines-personne** : programme d'automate, table Modbus, intégration Go, essais au banc. Un Linux et un runtime tournent dans l'armoire.

## Nomenclature et coût estimé

Prix relevés le 24 octobre 2026 : RS France affiche des prix HT ; Bürklin (Allemagne) des prix TTC à 19 %, convertis ici en HT ; le Compact Controller 100 est un prix Farnell Portugal dont la TVA n'est pas précisée. **Aucun prix public en euros n'a été trouvé pour le 750-8212** : les totaux reposent sur le 751-9301 et un 750-362 pour porter le K-Bus. Les prix de l'alimentation 24 V, de la fin de bus 750-600, des modules d'alimentation du bus et du 750-523 n'ont pas été trouvés et ne sont pas dans les totaux. Les prix eBay (34,80 € le 750-517, 150 € le 750-362) diviseraient les totaux par trois ou quatre, mais ne sont pas des prix de distributeur.

### Configuration minimale

| Poste | Référence | Qté | Prix unitaire HT | Total HT | Source |
| --- | --- | --- | --- | --- | --- |
| Contrôleur | Wago 751-9301 | 1 | 553,07 € (TVA non précisée) | 553 € | Farnell Portugal |
| Coupleur pour porter le K-Bus | Wago 750-362 | 1 | 409,05 € | 409 € | RS France |
| Entrées | Wago 750-1405 | 4 | 112,26 € (133,59 € TTC) | 449 € | Bürklin, sans stock, 5 semaines |
| Sorties relais | Wago 750-517 | 43 | 112,05 € (à partir de 3) | 4 818 € | RS France |
| Fin de bus | Wago 750-600 | 1 | non trouvé | — | — |
| Alimentation du bus | 750-613 (à vérifier) | 2 à 3 | non trouvé | — | — |
| Alimentation 24 V | Wago 787-1602 | 1 | non trouvé | — | — |
| **Matériel** | | | | **≈ 6 230 € HT** | hors postes non trouvés |
| Logiciel | CODESYS V3.5 | 1 | 0 € (à confirmer) | 0 € | distributeur |
| **Total** | | | | **≈ 6 250 € HT** | |

Avec le 750-517 de Bürklin (61,70 € HT, sans stock), les bornes de sorties coûteraient ≈ 2 650 € au lieu de ≈ 4 820 €, et le total ≈ 4 100 € HT.

### Configuration résiliente

| Poste | Référence | Qté | Prix unitaire HT | Total HT |
| --- | --- | --- | --- | --- |
| Maître | Wago 751-9301 | 1 | 553,07 € (TVA non précisée) | 553 € |
| Coupleurs de zone | Wago 750-362 | 3 | 409,05 € | 1 227 € |
| Entrées | Wago 750-1405 | 6 | 112,26 € | 674 € |
| Sorties relais | Wago 750-517 | 43 | 112,05 € | 4 818 € |
| Fins de bus | Wago 750-600 | 3 | non trouvé | — |
| Alimentations 24 V | Wago 787-1602 | 3 | non trouvé | — |
| **Matériel** | | | | **≈ 7 270 € HT**, hors postes non trouvés |
| Logiciel | CODESYS V3.5 | 1 | 0 € (à confirmer) | 0 € |
| **Total** | | | | **≈ 7 270 € HT** |

Soit ≈ 1 020 € HT de plus que la configuration minimale, pour passer de 6 à 5 défaillances uniques touchant toute la maison : le prix des deux coupleurs et des deux bornes d'entrées supplémentaires. Avec un 750-8212 en tête au lieu du 751-9301, le prix change d'un montant non trouvé.

### Couche domotique en dérivation

| Poste | Référence | Qté | Total HT |
| --- | --- | --- | --- |
| Sorties vers les relais de couplage | Wago 750-517 × 43 (86 contacts) | 43 | ≈ 4 818 € |
| Entrées de recopie | Wago 750-1405 × 5 (80 entrées) | 5 | ≈ 561 € |
| Contrôleur et coupleur | 751-9301, 750-362 | 2 | ≈ 962 € |
| Fin de bus, alimentation du bus, alimentation 24 V | 750-600, 750-613, 787-1602 | | non trouvés |
| **Matériel** | | | **≈ 6 340 € HT** |
| Logiciel | CODESYS V3.5 | 1 | 0 € (à confirmer) |
| **Total** | | | **≈ 6 350 € HT**, ≈ 0,75 m de rail |

### Ce qui n'est pas dans les totaux

- **Fonctions à reporter** : aucune centrale d'alarme, aucun écran, aucune mesure d'énergie en natif ; des bornes de mesure existent dans la série 750, non étudiées. L'alarme, la sirène et les détecteurs se raccordent à des bornes et se programment ; une alarme certifiée reste un produit à part. Le délestage se programme, avec des bornes de mesure à chiffrer.
- **Relais d'interface** : derrière les contacts 1 A des 750-517, un relais 230 V par circuit d'éclairage et par moteur de volet au-delà de 230 W (lecture « seule »), non chiffrés ; ou des 750-523 à 16 A pour les 25 éclairages et les divers, soit ≈ 0,8 m de rail de plus, prix non trouvé.
- **Variateurs** : aucun module 230 V ; un variateur universel externe par voie, à chiffrer.
- **Fil pilote** : contacts 750-517, suffisants pour les diodes du fil pilote ; aucune fonction native.
- **Électricien** : de l'ordre de 4 à 6 jours (estimation sans devis) ; les bornes à ressort vont vite, les relais d'interface ajoutent du câblage.
- **Logiciel** : ≈ 4 à 8 semaines-personne (CODESYS et passerelle), estimation sans source.
- **Place** : ≈ 0,65 à 0,75 m (minimale), ≈ 0,85 à 0,9 m (par zone), ≈ 0,75 m (dérivation, en plus de la couche filaire), alimentations et relais d'interface non compris.

## Ouverture et pérennité

- **Protocoles ouverts** en sortie : Modbus TCP/UDP, Modbus RTU, MQTT, OPC UA ; le K-Bus est propriétaire mais son interface logicielle (ADI/DAL) est documentée et utilisable par une application propre. CODESYS est un environnement tiers très répandu dans l'industrie.
- **Micrologiciel, kit de développement, exemples et Docker publiés** par Wago sur GitHub (une cinquantaine de dépôts), sous licence Apache-2.0 pour le paquet Docker.
- **Un seul fabricant** pour les bornes de la série 750 ; Modbus TCP, lui, est multi-fabricants, et le maître pourrait être remplacé.
- **Ancienneté** : PFC200 de première génération documenté en 2018, deuxième génération depuis 2019 ; fiches des bornes datées de 2023 et 2024, borne 750-517 « en production ». Date de lancement de la série 750 et politique de disponibilité à long terme non trouvées. Transition logicielle récente : e!COCKPIT remplacé par CODESYS V3.5 au micrologiciel 23.
- **Vente libre** chez les distributeurs industriels (RS, Bürklin, Farnell), avec des délais : Bürklin annonçait 5 semaines sans stock sur deux références.
- **Cloud** : aucun en exploitation ; offre optionnelle non étudiée.
- **Communauté** : CODESYS Forge, sps-forum, projets libres (4diac FORTE), orientés industrie plus que maison.

## Verdict

- **Seule** : Wago remplace l'armoire sans toucher un fil et apporte des bornes industrielles, mais garde un automate unique entre chaque bouton et sa charge : règle 1 non tenue, 5 défaillances uniques sur 8 privent toute la maison, et le découpage en coupleurs de zone ne change rien, faute de logique dans les coupleurs. Les sorties passent à zéro 50 ms après l'arrêt du programme : la maison s'éteint avec l'automate. Seul le sélecteur manuel du 750-523 rallume une lumière à la main. C'est l'architecture de l'étude V1 Revolution Pi, en matériel industriel.
- **En dérivation** : une couche d'entrées-sorties sérieuse, ouverte et durable, dont le repli à 50 ms est une qualité pour le relais de garde, mais qui coûte environ deux fois KNX pour commander des bobines, à comparer à la Revolution Pi Connect 5 (≈ 581 € HT nue, modules d'entrées-sorties non chiffrés ici), avec un Linux et CODESYS à maintenir.
- **À qui elle convient** : à qui pratique déjà CODESYS, veut des pièces industrielles disponibles dans dix ans et accepte de payer les bornes relais au prix de l'industrie.

## Sources

Toutes consultées le 24 octobre 2026.

1. [Fiche Wago 750-8212/000-100](https://cdn.soselectronic.com/productdata/2c/40/7e3f8956/750-8212-000-100.pdf) (15.03.2021) : processeur, mémoires, 250 et 64 bornes, protocoles, 500 V, 78,6 mm, 1 700 mA, licences e!COCKPIT.
2. [Fiche Wago 750-8212/025-000](https://www.farnell.com/datasheets/4151995.pdf) (12.02.2024) : OPC UA, MQTT, BACnet/IP sous licence, CODESYS V3.5 à partir du micrologiciel 23.
3. [Fiche Wago 750-1405](https://static.chipdip.ru/lib/293/DOC033293734.pdf) : niveaux, courants, 500 V, 12 mm, optocoupleur ; [fiche 2024](https://www.farnell.com/datasheets/4151964.pdf), non lue.
4. [Fiche Wago 750-362](https://www.farnell.com/datasheets/3938315.pdf) (28.04.2023) : 250 et 64 bornes, image process, deux ports, commutateur DIP.
5. [Wago, page produit 751-9301](https://www.wago.com/global/plcs-%E2%80%93-controllers/compact-controller-100/p/751-9301) et [Cebeo](https://www.cebeo.be/catalog/products/wago-controleur-compact-100-8di-4do-2ai-2ao-7502612) : entrées-sorties, 108 mm.
6. [DigiKey, Compact Controller 100](https://www.digikey.com/en/product-highlight/w/wago/751-compact-controller-100-series) : CODESYS 3.5 sans frais, Docker, extension par 750-362.
7. [Wago, PFC200 et Docker](https://www.wago.com/in/automation-technology/wireless-ethernet-gateway/pfc200-docker) (2019) et [CNX Software](https://www.cnx-software.com/2018/03/07/wago-pfc200-plc-runs-embedded-linux-supports-web-and-mobile-visualization/) (2018) : générations, protocoles, VPN.
8. [Fiche Wago 750-517](https://att.2ba.nl/4017332000000/master/CHR/2023112308421369_2108873161.pdf) (15.11.2023) et [page Wago](https://www.wago.com/de-en/io-systems/2-channel-relay-output/p/750-517) : 250 V / 1 A, 1 500 V, 90 mA, 12 mm.
9. [Fiche Wago 750-523](https://asset.conrad.com/media10/add/160267/c1/-/de/000191945DS01/datasheet-191945-wago-1-kanaals-relaisuitgangsklem-plc-digital-output-module-750-523-1-pcs.pdf) et [version 2023](https://www.e-sonic.com/productfiles/mf-WAG/WAG-750523.pdf) : 16 A, sélecteur manuel, 24 mm.
10. [gridX, configuration du 750-362](https://support.gridx.ai/en/articles/626047-wago-750-362-fieldbus-coupler) : interface web, port 502, fin de bus 750-600.
11. [Manuel WAGO-I/O-SYSTEM 750, coupleur EtherCAT](https://www.manualslib.com/manual/1983609/Wago-I-O-System-750.html) : perte d'alimentation et perte du bus de terrain, sorties à zéro ; SELV/PELV ; séparation des alimentations.
12. [Eclipse 4diac, Wago PFC200](https://eclipse.dev/4diac/doc/io_config/wago_pfc200.html) : un seul maître K-Bus, arrêt du runtime, repli des sorties après 50 ms.
13. Industrial Monitor Direct (blog distributeur, source secondaire) : [K-Bus et runtime STOP](https://industrialmonitordirect.com/blogs/knowledgebase/wago-750-8212-cpu-stopped-clear-faults-and-restart-plc), [pas de repli réglable par borne sur 750-841](https://industrialmonitordirect.com/blogs/knowledgebase/wago-750-841-io-card-failure-why-all-ios-go-dead), [licence du runtime](https://industrialmonitordirect.com/blogs/knowledgebase/resolving-codesys-license-requirements-on-wago-pfc-200-750-8212-controllers).
14. [GitHub Wago](https://github.com/WAGO) et [docker-ipk](https://github.com/WAGO/docker-ipk) : micrologiciel, kit de développement, Docker, compatibilité, licence Apache-2.0.
15. [IIDM, licence e!RUNTIME Sparkplug](https://shop.iidm.com/2759-247-210-1000-e-runtime-sparkplug-single-license-p-42074).
16. [npm @wago/node-red-io-api](https://npmjs.org/package/@wago/node-red-io-api) : API K-Bus en MQTT, runtime à arrêter.
17. Prix : [Farnell Portugal 751-9301](https://pt.farnell.com/wago/751-9301/controller-2i-o-analog-8-i-4-o/dp/3929186), [Bürklin 750-1405](https://buerklin.com/en/p/wago/digital-modules/750-1405/73F2038), [RS France 750-517](https://fr.rs-online.com/web/p/modules-d-es-api/8687374), [Bürklin 750-517](https://buerklin.com/en/p/wago/digital-modules/750-517/09P0157), [RS France 750-362](https://fr.rs-online.com/web/p/automates-programmables/2885276), [RS Belgique 750-362](https://befr.rs-online.com/web/p/plcs-programmable-logic-controllers/2885276), [Octopart 750-1405](https://octopart.com/part/wago/750-1405).
18. [CODESYS Forge, fils PFC200](https://forge.codesys.com/forge/talk/Deutsch/thread/ed4a058c73/) et [diagnostic K-Bus](https://forge.codesys.com/forge/talk/Deutsch/thread/da52458b34/).

!!! note "À confirmer auprès des fabricants"
    Le prix public du 750-8212 et ceux du 787-1602, du 750-523, du 750-600 et du 750-613 ; le manuel du 750-362 (état des sorties à la perte du maître, registres de chien de garde Modbus, délai, valeurs de substitution, courant disponible sur le bus 5 V) ; le manuel du PFC200 (comportement des sorties à l'arrêt du runtime, chien de garde matériel, redémarrage automatique, mise à jour ratée) ; l'inclusion du runtime CODESYS dans le prix du 750-8212 ; la longueur de ligne admise sur les entrées 750-1405 et la compatibilité avec les jonctions IDC ; les fiches 750-559 et 753-647 pour les variateurs ; l'isolement du 750-523 et du 750-362, la catégorie de surtension et les recommandations de parafoudre ; la largeur du 750-362 et du 750-600 ; la politique de disponibilité à long terme de la série 750.
