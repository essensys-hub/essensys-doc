---
title: "Domintell : remplacer l'armoire sans recâblage"
description: "Domintell, bus propriétaire belge à maître unique, pour remplacer les quatre cartes de l'armoire ESSENSYS sans toucher aux fils : modules d'entrées DISM20 pour les 63 poussoirs, cartes relais DMR02, cartes volets DTRV01, variateurs DD400L. Seul, le Master reste sur le chemin de chaque bouton et la limite de 10 m des entrées met les nappes hors contrainte ; en dérivation, c'est la couche domotique la plus chère du comparatif. Environ 7 530 € HT en configuration par coffret."
---

# Domintell

Domintell est un bus domotique propriétaire belge, vendu par installateurs depuis une vingtaine d'années, avec des modules d'entrées faits pour des poussoirs classiques. Il est dans ce [comparatif](index.md) pour cette raison. Deux faits le cadrent d'emblée : le système est **strictement centralisé** (un Master unique, « aucune information n'est directement échangée entre les modules »), et ses modules d'entrées admettent **10 m** entre le module et le contact, quand les nappes de la maison vont jusqu'à 30 m : la solution est **hors contrainte** tant que Domintell n'a pas écrit le contraire.

!!! abstract "Synthèse"
    - **Seule** : Domintell reprend les 63 poussoirs et toutes les charges sur rail DIN, mais chaque appui passe par le Master : **règle 1 non tenue**. Le découpage par coffret n'y change rien, un seul Master et une seule paire de données : **6 des huit défaillances uniques privent toute la maison de ses boutons**, en configuration par coffret comme en configuration minimale. Les cartes relais DMR02 ont des DIP switches de secours, dans l'armoire. La limite de **10 m** des entrées DISM met les nappes de 30 m **hors contrainte**.
    - **En dérivation** : une couche domotique à Master unique, pilotée par un protocole ASCII documenté (Light Protocol) et une intégration Home Assistant officielle. Le Master reste sur le chemin des contacts ; le signal cyclique du relais de garde doit venir de la passerelle. C'est la couche la plus chère du comparatif.
    - **Coût estimé** : ≈ 6 190 € HT en configuration minimale, ≈ 7 530 € HT par coffret, ≈ 5 570 € HT en couche domotique seule. Prix publics hors TVA du fabricant, octobre 2026 ; logiciel GoldenGate sans prix trouvé.
    - **Réserve** : estimations à confirmer par un électricien, des devis, le fabricant et des essais. La tolérance réelle des entrées au-delà de 10 m, le type des relais et l'isolement bus / 230 V n'ont pas été trouvés.

## Principe et gamme

Domintell SA est installée à Nivelles (Belgique), société constituée en 1986, bus domotique depuis les années 2000, « près de 10 000 installations » revendiquées. La conception et la production sont belges ; la vente passe par des installateurs et des revendeurs, avec un accès « Pro » et des formations gratuites de deux niveaux.

Le bus est un **RS-485 propriétaire à quatre fils** : deux fils d'alimentation en 15 V continu (12 à 20 V admis au point le plus éloigné) et une paire torsadée de données. Longueur totale 500 m au plus, câblage en ligne, pas d'étoile ni de boucle ; un répéteur DHUB01 au-delà de 128 modules ou 300 m, dont la disponibilité n'a pas été vérifiée. Le système est **centralisé** : le manuel de câblage dit que les modules d'entrées envoient leurs informations au Master, que le Master commande les sorties selon son programme, et qu'aucune information ne circule directement entre modules. Les fiches de 2025 présentent toujours le Master comme l'unité centrale qui « effectue la gestion du système ».

Les Masters actuels datent de 2019 : **DGQG04** (alimenté par le bus, Ethernet), DGQG02 (tout-en-un avec entrées-sorties et alimentation 230 V), DGQG05 (avec un bus d'éclairage 48 V). La configuration se fait sous Windows avec **GoldenGate**. Chronologie : protocole d'intégration public en 2012, application Pilot en 2017, Pilot 2 avec cloud optionnel en 2023, intégration Home Assistant officielle le 12 janvier 2026.

## Dans l'armoire sans recâblage

Les poussoirs sont des contacts secs : des **modules DISM** les lisent, sur rail DIN pour le DISM20, en boîtier libre pour les DISM04 et DISM08. Le bus peut rester dans les coffrets ; seuls les fils des contacts en sortent.

| Fonction | Module | Voies | Largeur | Ce qu'il faut savoir |
| --- | --- | --- | --- | --- |
| 63 poussoirs | DISM20 | 20 contacts secs, un commun par groupe de 3 | 4 modules | « Doit être connecté à un vrai contact sec » ; **10 m au plus entre le module et l'entrée**, câble alarme ou téléphone. Les nappes vont jusqu'à 30 m : **hors contrainte** sans tolérance écrite du fabricant. Tension et courant sur le contact, isolation galvanique : non trouvés |
| | DISM04 / DISM08 | 4 / 8 | boîtier 46 × 28 × 15 mm, hors rail | Même limite de 10 m ; conçus pour être posés près des poussoirs |
| 25 éclairages | DMR02 | 8 relais monopolaires 16 A | 5 modules | **DIP switches pour la commande manuelle sans Master** ; 50 A au plus commutés par carte ; charge LED non chiffrée (« voir courant de pointe ») ; compatible DGQG02 et suivants seulement ; type de relais (monostable ou bistable) : non trouvé |
| | DTRP01 + 4 × TL2001 | 4 télérupteurs mécaniques 2 × 16 A | 2 + 4 × 1,5 modules | Télérupteurs Schneider à **manette** en face avant, bistables par construction ; 1,2 A à l'enclenchement sur le bus |
| 15 volets dont le store | DTRV01 | 4 sorties montée / descente, 8 relais 8 A | 9 modules | Inductif 200 W par relais ; deux contacts en face avant commandent les 4 montées ou les 4 descentes ensemble ; verrouillage des deux sens et pause à l'inversion : non trouvés |
| | DTRP02 + 4 × TL1001 | 2 volets par télérupteurs inverseurs 16 A | 2 + 4 × 1,5 modules | Pour moteurs lourds ; manette par télérupteur |
| 8 variateurs | DDIM01 + 8 × DD400L | 1 interface pour 8 variateurs 400 W (200 W en LED) | 4 + 8 × 2 modules | Synchronisation par la phase de chaque variateur ; fusible 2,5 A en face avant ; la commande manuelle du DDIM01 ne fait que tout ou rien ; procédé de variation non trouvé |
| Fil pilote | aucune offre trouvée | | | Repli : relais DMR02 ; à vérifier avec Domintell |
| Cumulus, prises, arrosage, machines | DMR02 (7 relais restants) | 16 A | | DBIR01 bipolaire si l'on veut couper les deux pôles |
| Master | DGQG04 | | 6 modules | Alimenté par le bus ; Ethernet ; horloge ; démarrage 2 à 3 min ; 600 modules selon la page produit, 60 selon le catalogue 2025 |
| Alimentation | DALI05 | 15 V, 4 A, 60 W | 6 modules | « Impératif de placer une alimentation dans chaque coffret » ; dialogue avec le Master ; protections contre le court-circuit non trouvées ; puissance divisée par deux au-delà de 45 °C |
| Interface réseau | DNET02 (optionnelle) | | 3 modules | Le DGQG04 porte déjà l'Ethernet et le protocole d'intégration |

Les boutons Domintell (Rainbow, Axolute), les écrans tactiles et les boutons LCD ne sont pas retenus : ils demanderaient de tirer le bus jusqu'aux murs.

### Configuration minimale

Un bus, une alimentation, un Master, tout dans l'armoire : DGQG04, DALI05, quatre DISM20 (80 entrées), quatre DMR02 (32 relais : 25 éclairages et 7 divers), quatre DTRV01 (16 volets), un DDIM01 et huit DD400L. **104 modules, soit ≈ 1,82 m de rail**, 23 appareils ; consommation sur le bus au pire cas ≈ 2,3 A à 15 V, sous les 4 A de la DALI05, à vérifier au point le plus éloigné toutes sorties enclenchées.

### Configuration résiliente

La gamme ne permet pas un contrôleur par zone : **un seul Master par installation**, pas de coupleur de ligne ni de segmentation documentés. Ce qu'elle permet, et impose : **une alimentation par coffret**, le fil +15 V non relié entre coffrets, la paire de données et la masse communes à tous. La configuration par coffret est donc : trois coffrets, un par zone, chacun avec sa DALI05, son DISM20 (plus un DISM04 hors rail pour les chambres et les pièces d'eau), ses DMR02, DTRV01, DDIM01 et DD400L ; le Master dans l'un des trois.

| Coffret | Modules | Largeur |
| --- | --- | --- |
| Pièces de vie (20 poussoirs, 5 éclairages, 6 volets, 3 variateurs) | DALI05, DISM20, DMR02, 2 × DTRV01, DDIM01, 3 × DD400L | 43 |
| Chambres (21, 7, 5, 4) | DALI05, DISM20 + DISM04, DMR02, 2 × DTRV01, DDIM01, 4 × DD400L | 45 |
| Pièces d'eau (22, 13, 4 dont le store, 1) | DALI05, DISM20 + DISM04, 2 × DMR02, DTRV01, DDIM01, DD400L | 35 |
| Master | DGQG04 | 6 |

**129 modules, soit ≈ 2,26 m de rail**, trois alimentations, un Master. Une panne d'alimentation ne prive que son coffret, sauf celui du Master ; une panne du Master ou de la paire de données touche les trois zones.

## Seule face à l'exigence

### Les sept règles

| Règle | Tenue | Pourquoi |
| --- | --- | --- |
| 1. Pas de calculateur entre le bouton et sa charge | **Non tenue** | Le poussoir attaque un DISM, qui parle au Master, qui commande la carte de sortie : « aucune information n'est directement échangée entre les modules ». Aucun mode autonome entrée → sortie trouvé. Les DIP switches des DMR02 commandent les relais sans Master, mais dans l'armoire, pas depuis le mur. Et la limite de **10 m** des DISM met les nappes de 30 m **hors contrainte** |
| 2. L'état vit dans un organe bistable | **Non tenue** avec les DMR02 ; tenue avec les télérupteurs TL2001 | Le type des relais DMR02, DBIR01 et DTRV01 et leur état au retour de tension ne sont pas documentés. Les TL2001 et TL1001 sont des télérupteurs mécaniques à manette, qui gardent leur état |
| 3. La domotique ajoute, ne retire jamais | Non tenue | Le bus **est** la domotique : un ordre faux du Master ou du protocole d'intégration commute n'importe quelle voie. Parade : mot de passe et WebSocket chiffré sur le Master, deux connexions au plus |
| 4. Une source et un fusible par zone, un fusible pour la domotique | Partielle | Une alimentation par coffret est imposée ; mais boutons et domotique partagent le bus, et le coffret du Master alimente aussi le Master. Aucun fusible ne sépare les deux |
| 5. Barrière 4 kV et 8 mm, 0 V jamais au PE, parafoudres hors coffrets | **Non tenue, sauf attestation** | Le bus 15 V n'est pas qualifié TBTS dans les fiches ; l'isolation des entrées DISM n'est pas documentée (contact très probablement référencé au bus) ; aucune tension d'essai bus / 230 V, aucun parafoudre recommandé. Le blindage du bus ne doit pas être relié à la terre |
| 6. Replis choisis au câblage, essayés à la recette | Partielle | Les secours existent en matériel (DIP du DMR02, contacts groupés du DTRV01, manettes des TL), mais le comportement des relais à la perte du bus et au retour de tension n'est pas documenté, et le programme vit dans le Master |
| 7. Isolement mesuré chaque année | Tenue | Rien ne l'empêche ; GoldenGate signale les modules qui ne répondent plus, et la fiche diagnostic donne les tensions à mesurer sur le bus |

### Les causes communes

Dans la configuration par coffret, la liste fermée du comparatif donne :

| Défaillance unique | Prive de ses boutons… | Pourquoi |
| --- | --- | --- |
| 1. Alimentation du bus | toute la maison | Trois DALI05, mais le Master est alimenté par le bus de son coffret : cette alimentation morte éteint le Master, donc les trois zones. Les deux autres ne privent que leur coffret. Parade non chiffrée : une seconde alimentation en parallèle dans ce coffret, « avec précautions » |
| 2. Court-circuit ou ligne collée | toute la maison | Une seule paire de données traverse les trois coffrets ; pas de coupleur. Le dépannage se fait au multimètre, alimentations coupées ; un module perturbateur se trouve en débranchant tout puis en rebranchant un à un |
| 3. Contrôleur central | toute la maison | Master unique ; redondance non trouvée ; redémarrage 2 à 3 min |
| 4. Logiciel figé | toute la maison | Le programme tourne dans le Master ; chien de garde ou redémarrage automatique non trouvés |
| 5. Mise à jour ratée | toute la maison | La mise à jour du Master dure 20 à 30 min, « connexion au Master coupée » ; l'effet d'une mise à jour interrompue n'est pas documenté |
| 6. Licence, compte ou cloud | rien | Aucune licence d'exploitation ; cloud Pilot 2 optionnel ; fonctionnement local en LAN, sans déclaration explicite du fabricant (à confirmer) |
| 7. Commutateur ou routeur | rien | Hors du chemin du bouton : le bus RS-485 relie les DISM, le Master et les sorties sans passer par l'Ethernet |
| 8. Foudre sur le chemin du bus | toute la maison | Le bus reste dans les coffrets, mais les entrées DISM ne sont pas documentées isolées : une onde entrant par une nappe atteint vraisemblablement le bus 15 V, commun aux trois coffrets |

**Total : 6 défaillances uniques privent toute la maison**, aucune ne s'arrête à une zone sauf la perte d'une alimentation hors du coffret du Master. En configuration minimale, le compte est le même : **6**. Le découpage par coffret n'achète donc rien sur ce critère ; il n'y a pas de configuration par zone chez Domintell, seulement une répartition de l'alimentation.

Ce décompte ramène à l'architecture d'avant la V2, en pire : le BP actuel pouvait planter sans priver les boutons, puisque chaque BA basculait lui-même ses relais ; ici, le Master est sur le chemin de chaque appui. Aucun témoignage de panne de Master n'a été trouvé sur les forums, ni aucun retour de foudre.

### Ce qui reste, panne par panne

| Panne | Ce qui reste |
| --- | --- |
| Master arrêté, en redémarrage (2 à 3 min) ou en mise à jour (20 à 30 min) | Aucun bouton. Dans l'armoire : les DIP switches des DMR02 relais par relais, les deux contacts du DTRV01 pour les 4 montées ou les 4 descentes ensemble, les DIP du DDIM01 en tout ou rien ; en variante télérupteurs, les manettes des TL. État des relais DMR02 et DTRV01 : non trouvé |
| Alimentation du coffret du Master | Comme ci-dessus, plus les modules de ce coffret hors tension |
| Alimentation d'un autre coffret | Sa zone sans boutons, modules hors tension ; les deux autres zones fonctionnent par le Master |
| Court-circuit sur la paire de données | Aucun bouton, jusqu'à la recherche au multimètre |
| Réseau ou passerelle | Tout le local ; perdues : l'application Essensys et l'accès Pilot par le LAN |
| Coupure du secteur | Au retour, 2 à 3 min de redémarrage ; état des relais au retour non documenté ; les TL gardent leur état |
| Un module | Ses voies ; échange, nouveau scan dans GoldenGate ; un mot de passe de module perdu « ne peut pas être récupéré » |
| Foudre par une nappe | Le DISM touché au mieux ; au pire le bus commun, faute d'isolation documentée |

## En dérivation sur le filaire V2

Dans cette lecture, les télérupteurs, les chaînes de volets et les variateurs à entrée locale gardent le chemin du bouton. Domintell fournit la couche domotique :

- **Sorties** : onze DMR02 (88 relais 16 A) commandent les bobines 24 V des relais de couplage 38.51 de la V2. Le contact est sec si l'on n'alimente pas le commun en 230 V ; les borniers « L N / OUT » par groupe sont à vérifier sur le schéma. Des cartes dédiées à la TBTS, sans voie 230 V dans le même boîtier.
- **Entrées** : quatre DISM20 (80 entrées) lisent les contacts des relais de recopie ; à l'intérieur du coffret, la limite de 10 m est tenue. L'isolation des entrées n'étant pas documentée, la barrière est le 38.51 de recopie, pas le DISM.
- **Battement de cœur** : aucune sortie cyclique autonome trouvée dans le Master. Le signal du relais de garde vient donc de la **passerelle**, qui bascule un relais DMR02 par le Light Protocol (`%I`, `%O`) à travers le Master et le bus. Si la passerelle, le Master ou le bus se tait, le relais ne bascule plus et le relais de garde retombe : le chien de garde matériel de la V2 reste en place. Une cadence de 200 ms sur un relais électromécanique et sur un bus RS-485 est à essayer avant d'être retenue ; les événements périodiques du Master sont une autre piste, à confirmer avec Domintell.
- **Logique et interface utilisateur** : la passerelle, par le Light Protocol en WebSocket Secure (deux connexions au plus), ou Home Assistant par l'intégration officielle. Le Master porte scènes, groupes, horloge et horloge astronomique.
- **Durées bornées** : le câblage de la V2 les borne ; aucune minuterie de voie n'a été relevée sur les DMR02.

Ce que la couche apporte : un fabricant unique de vingt ans, un protocole ASCII simple et documenté, une intégration Home Assistant maintenue par le fabricant, une mise en service par GoldenGate. Ce qu'elle coûte : ≈ 5 570 € HT, 83 modules (≈ 1,45 m de rail, à ajouter aux 1,6 à 2,1 m de la couche filaire), un Master unique sur le chemin de tous les contacts, un logiciel Windows à accès Pro. À comparer à la Revolution Pi Connect 5 (≈ 581 € HT nue, modules d'entrées-sorties non chiffrés ici) ; face à KNX en dérivation (≈ 3 100 € HT), presque le double, sans la norme ni les 500 fabricants ; face au serveur d'entrées-sorties léger ([dossier Modbus](modbus-es.md)), sans comparaison.

## Foudre et isolement

- **Le bus reste dans les coffrets** avec des DISM20 et des poussoirs classiques ; les nappes portent la tension d'entrée des DISM, dont la nature n'est pas documentée. Le manuel impose un conduit propre au câble bus, 2 cm d'écart au moins dans les goulottes, blindage non raccordé et non mis à la terre.
- **Tensions d'essai** : aucune fiche ne donne la tension d'essai entre le bus et les contacts 230 V des DMR02, DBIR01 ou DTRV01, ni la classe d'isolement de la DALI05. Le bus 15 V n'est pas qualifié TBTS dans les documents consultés ; seul le bus d'éclairage 48 V exige une alimentation « de classe 2 à double isolation ». La barrière de 4 kV et 8 mm de la V2 est donc **à faire attester** ; sans attestation, un relais 38.51 (6 kV) devant chaque voie et chaque entrée, comme la V2 le prévoit en dérivation.
- **Entrées** : « doit être connecté à un vrai contact sec », commun par groupe de trois ; optocoupleur ou référence au bus : non trouvé. Si le contact est au potentiel du bus, l'îlot des boutons et l'îlot du bus sont le même, et une onde par une nappe traverse les trois coffrets.
- **Parafoudres** : aucune recommandation du fabricant trouvée. Les parafoudres de la V2 restent hors des coffrets.
- **Retours de terrain** : aucun retour de foudre sur une installation Domintell n'a été trouvé.

## Logiciel, paramétrage et passerelle Essensys

| Point | Ce qu'on a trouvé |
| --- | --- |
| Outil | **GoldenGate** (Windows), version 3.x et plus pour les Masters actuels ; distribué par l'espace Pro du site, sur inscription ; prix non affiché, aucune licence payante mentionnée ; conditions d'accès pour un propriétaire non trouvées |
| Formation | Deux niveaux d'une journée, gratuits, en français et néerlandais, à Nivelles, sessions 2026-2027 |
| Mise à jour | Par GoldenGate ; Master 20 à 30 min avec connexion coupée ; versions du Master, de GoldenGate et des écrans à faire concorder, « une discordance des versions est souvent la cause des problèmes » |
| Sécurité | WebSocket Secure (TLS 1.2) et mot de passe sur le Master ; mot de passe de module irrécupérable s'il est perdu |
| API pour la passerelle | **Light Protocol** : trames ASCII (`%I` marche, `%O` arrêt, `%P` appui simulé, `%D` niveau, `%H` / `%L` volets), une ligne par changement d'état en retour, `APPINFO` pour lister les modules et les liens, `HELLO` toutes les 50 s ; sur le DGQG04 en WebSocket Secure, port 17481, **deux connexions au plus**, à activer dans GoldenGate. Ni KNXnet/IP, ni Modbus exposé, ni MQTT, ni REST |
| Bibliothèques libres | Intégration **Home Assistant officielle** (Apache-2.0, HACS, janvier 2026, Masters actuels seulement, position des volets approximative) ; binding openHAB de 2018 sans mainteneur ; bibliothèque Python communautaire sans documentation. Bibliothèque Go : aucune |
| Cloud | Optionnel (Pilot 2 pour l'accès distant) ; local par LAN ou DynDNS ; aucun compte obligatoire trouvé pour le fonctionnement local, à confirmer |

Côté passerelle, le backend Go doit tenir une session WebSocket Secure et parler le Light Protocol, protocole texte simple. L'estimation est de **deux à quatre semaines-personne** pour l'intégration, plus une à deux semaines de paramétrage dans GoldenGate et d'apprentissage : ≈ 3 à 6 semaines avant la bascule, sous réserve de l'accès Pro. Aucun logiciel du projet ne tourne dans l'armoire.

## Nomenclature et coût estimé

Prix publics affichés **hors TVA** sur les pages produit du fabricant, relevés le 24 octobre 2026 ; aucune conversion n'est donc nécessaire. Domintell vend par ses installateurs, dont les tarifs peuvent différer. Câbles, borniers et port exclus.

### Configuration minimale

| Poste | Référence | Qté | Prix unitaire HT | Total HT | Source |
| --- | --- | --- | --- | --- | --- |
| Master | DGQG04 | 1 | 720,00 € | 720 € | domintell.com |
| Alimentation | DALI05 | 1 | 260,10 € | 260 € | domintell.com |
| Entrées | DISM20 | 4 | 198,00 € | 792 € | domintell.com |
| Éclairages et divers | DMR02 | 4 | 345,00 € | 1 380 € | domintell.com |
| Volets | DTRV01 | 4 | 383,20 € | 1 533 € | domintell.com |
| Variateurs | DDIM01 | 1 | 244,10 € | 244 € | domintell.com |
| Variateurs | DD400L | 8 | 158,10 € | 1 265 € | domintell.com |
| **Matériel** | | | | **≈ 6 190 € HT** | |
| Logiciel | GoldenGate | 1 | non trouvé (aucune licence payante mentionnée) | — | domintell.com |
| **Total** | | | | **≈ 6 190 € HT** | |

### Configuration résiliente

| Poste | Référence | Qté | Prix unitaire HT | Total HT |
| --- | --- | --- | --- | --- |
| Master | DGQG04 | 1 | 720,00 € | 720 € |
| Alimentations | DALI05 | 3 | 260,10 € | 780 € |
| Entrées | DISM20 | 3 | 198,00 € | 594 € |
| Entrées | DISM04 | 2 | 72,50 € | 145 € |
| Éclairages et divers | DMR02 | 4 | 345,00 € | 1 380 € |
| Volets | DTRV01 | 5 | 383,20 € | 1 916 € |
| Variateurs | DDIM01 | 3 | 244,10 € | 732 € |
| Variateurs | DD400L | 8 | 158,10 € | 1 265 € |
| **Matériel** | | | | **≈ 7 530 € HT** |
| Logiciel | GoldenGate | 1 | non trouvé | — |
| **Total** | | | | **≈ 7 530 € HT** |

Soit ≈ 1 340 € HT de plus que la configuration minimale, sans changer le compte des défaillances uniques qui touchent toute la maison, 6 dans les deux cas : la dépense n'achète que le confinement d'une panne d'alimentation hors du coffret du Master. La variante à télérupteurs mécaniques, qui tient la règle 2, coûte en plus : ≈ 2 335 € HT et 25 modules pour les volets (huit DTRP02 à 142,20 € et trente TL1001 à 91,00 €, soit 3 868 €, au lieu de quatre DTRV01 à 383,20 €, soit 1 533 €) ; ≈ 1 890 € HT et une trentaine de modules pour les éclairages (sept DTRP01 à 142,20 € et vingt-cinq TL2001 à 91,00 €, soit 3 270 €, au lieu de quatre DMR02 à 345,00 €, soit 1 380 €), calcul sur les prix publics HT du fabricant (source 14).

### Couche domotique en dérivation

| Poste | Référence | Qté | Total HT |
| --- | --- | --- | --- |
| Sorties vers les relais de couplage | DMR02 (88 relais 16 A) | 11 | 3 795 € |
| Entrées de recopie | DISM20 (80 entrées) | 4 | 792 € |
| Master et alimentation | DGQG04, DALI05 | 2 | 980 € |
| **Matériel** | | | **≈ 5 570 € HT** |
| Logiciel | GoldenGate | 1 | non trouvé |
| **Total** | | | **≈ 5 570 € HT**, 83 modules |

Consommation sur le bus au pire cas ≈ 2,9 A, sous les 4 A de la DALI05.

### Ce qui n'est pas dans les totaux

- **Fonctions à reporter** : pas de centrale d'alarme certifiée ; des entrées DISM pour les détecteurs et un ancien module GSM. Écran tactile 7" DTSC05, prix non relevé. Délestage : aucune logique trouvée ; la mesure passe par le module DELEC01 (≈ 128 € HT), qui lit le port P1 des compteurs belges et néerlandais, pas le Linky.
- **Fil pilote** : aucun module ; prévoir des relais DMR02 ou externes, à vérifier avec Domintell.
- **Reprise des nappes** : si Domintell confirme les 10 m, les lignes de plus de 10 m sont à reprendre, ou des DISM04 et DISM08 sont à poser près des poussoirs avec le bus tiré jusqu'à eux ; non chiffré, et contraire à la question posée.
- **Électricien** : de l'ordre de 4 à 6 jours hors reprise des nappes (estimation sans devis).
- **Logiciel** : ≈ 3 à 6 semaines-personne (GoldenGate et passerelle).
- **Place** : ≈ 1,82 m (minimale), ≈ 2,26 m (par coffret), ≈ 1,45 m (dérivation, en plus de la couche filaire), plus les DISM04 hors rail.

## Ouverture et pérennité

- **Protocole propriétaire**, un seul fabricant de modules. Ouverture par le Light Protocol, documenté depuis 2012, et par l'intégration Home Assistant officielle de 2026 ; passerelles vers DALI, DMX et Modbus RTU en maître, mais aucune exposition de Domintell en Modbus, KNX ou MQTT.
- **Ancienneté** : société de 1986, gamme bus depuis les années 2000, références DISM, DBIR, DTRV et DDIM inchangées depuis au moins le manuel de 2010 ; catalogue 2025 de 199 produits. Aucune politique de pièces à dix ans publiée.
- **Ruptures** : les nouveautés (DMR02, écran DTSC05, compteur, Home Assistant) exigent les Masters de 2019 ; le DGQG01 n'est plus pris en charge par l'intégration Home Assistant, et GoldenGate 1.4x a abandonné les anciens écrans ; interfaces Ethernet DETH remplacées ; offre de reprise à −25 % depuis juin 2024 pour migrer les anciens Masters, écrans et variateurs. Le fabricant revendique « une compatibilité ascendante maximale ».
- **Santé de l'entreprise** : le registre consulté donne « situation normale ». La situation financière est à vérifier au registre belge des entreprises avant toute décision.
- **Vente** par installateurs ; prix publics affichés ; logiciel par accès Pro.
- **Communauté** : faible hors Belgique ; un fil Home Assistant, un fil openHAB sans mainteneur, pas de forum officiel.

## Verdict

- **Seule** : Domintell ne répond ni à la question ni à l'exigence. La limite de 10 m de ses entrées exclut les nappes existantes sans recâblage, et son Master unique met un calculateur sur le chemin de chaque bouton : six défaillances uniques privent toute la maison, en configuration minimale comme par coffret. Les DIP switches des cartes relais rendent la main dans l'armoire, pas au mur. C'est la plus centralisée des architectures de ce comparatif.
- **En dérivation** : une couche domotique honnête mais chère, ≈ 5 570 € HT contre ≈ 3 100 € HT pour KNX, à comparer à la Revolution Pi Connect 5 (≈ 581 € HT nue, modules d'entrées-sorties non chiffrés ici), avec un fabricant unique, un logiciel Windows à accès Pro et un Master sur le chemin de tous les contacts. Le protocole ASCII est son meilleur argument.
- **À qui elle convient** : à qui a déjà une installation Domintell et un installateur agréé, et veut une intégration Home Assistant soutenue par le fabricant. Pas à cette armoire.

## Sources

Toutes consultées le 24 octobre 2026.

1. [Domintell, à propos](https://www.domintell.com/en/about-us/) : historique, installations, pays, vente par installateurs.
2. [Registre des entreprises, Domintell SA](https://www.topograph.co/companies/be/domintell-0429942701) : constitution en 1986, « situation normale ».
3. [Formations Domintell](https://www.domintell.com/en/trainings/) : deux niveaux gratuits, sessions 2026-2027.
4. [Manuel technique de câblage (2010)](https://pro.mydomintell.com/share/manual/DGQG01/DocCablage_FR_1_00.pdf) : principe centralisé, bus à quatre fils, 500 m, une alimentation par coffret, commandes manuelles des DBIR01, DTRV01 et DDIM01, dépannage.
5. [Catalogue 2025](https://www.domintell.com/wp-content/uploads/2025/02/Domintell-Catalogue.pdf) : bus RS-485, 15 V, Masters, alimentations, DISM (10 m), DMR02 (DIP sans Master), DTRV01, DDIM01, DD400L.
6. [Light Protocol, fiche v1.27.08 (2018)](https://pro.mydomintell.com/share/manual/DETH02-DRS23202/DS_RS232_ETH_Interfaces_v1_27_08.pdf) : trames ASCII, `APPINFO`, `HELLO`, limites.
7. [Fiche « Diagnostic – Support »](https://pro.mydomintell.com/share/manual/DGQG01/Doc_checks_V1_2.pdf) : tensions du bus, court-circuits, DHUB01, courant de pointe des télérupteurs.
8. [DGQG04](https://www.domintell.com/en/products/system/unite-centrale/dgqg04/) : 720 € HT, alimenté par le bus, Ethernet, 600 modules, alimentations requises.
9. [DGQG02](https://www.domintell.com/en/products/system/unite-centrale/dgqg02/) : 1 110 € HT, tout-en-un.
10. [DALI05](https://www.domintell.com/en/products/system/power-supply/dali05/) : 260,10 € HT, 15 V, 60 W, une alimentation par coffret.
11. [DISM20](https://www.domintell.com/en/products/system/inputs/dism20/), [DISM08](https://www.domintell.com/en/products/system/inputs/dism08/), [DISM04](https://www.domintell.com/en/products/system/inputs/dism04/) : entrées pour contacts secs, 10 m, prix.
12. [DMR02](https://www.domintell.com/en/products/system/outputs/dmr02/) : 345 € HT, 8 × 16 A, DIP switches sans Master, Masters 2019 seulement ; [billet du 8 avril 2024](https://www.domintell.com/en/8-outputs-relay-card/).
13. [DMR01](https://www.domintell.com/en/products/system/outputs/dmr01/) et [DBIR01](https://www.domintell.com/en/products/system/outputs/dbir01/) : microswitches de secours, prix.
14. [DTRP01](https://www.domintell.com/en/products/system/outputs/dtrp01/), [TL2001](https://www.domintell.com/en/products/system/outputs/tl2001/), [DTRP02](https://www.domintell.com/en/products/system/outputs/dtrp02/), [TL1001](https://www.domintell.com/en/products/system/outputs/tl1001/) : télérupteurs à manette ; DTRP01 et DTRP02 à 142,20 € HT, TL1001 et TL2001 à 91,00 € HT.
15. [DTRV01](https://www.domintell.com/en/products/system/outputs/dtrv01/) : 383,20 € HT, 4 volets, 8 relais 8 A.
16. [DDIM01](https://www.domintell.com/en/products/features/lighting-management/ddim01/) et [DD400L](https://www.domintell.com/en/products/features/lighting-management/dd400l/) : interface et variateur 400 W, prix.
17. [DNET02](https://www.domintell.com/en/products/features/communication/dnet02/) : 617 € HT, WebSocket Secure.
18. [FAQ Domintell](https://www.domintell.com/en/faq/) : versions GoldenGate, site Pro, mises à jour 20 à 30 min, redémarrage 2 à 3 min, mot de passe irrécupérable.
19. [Pilot 2](https://www.domintell.com/en/pilot-2-blog/) : cloud optionnel pour l'accès distant.
20. [Offre de reprise (juin 2024)](https://www.domintell.com/en/offre-upgrade-blog/) : −25 %, migrations, compatibilité ascendante.
21. [Intégration Home Assistant officielle](https://github.com/Domintell/ha_domintell) et [billet du 12 janvier 2026](https://www.domintell.com/en/compatible-home-assistant/) : Apache-2.0, port 17481, deux connexions, modules et limites.
22. [DELEC01](https://www.domintell.com/en/products/sensors/electrical-consumption/delec01/) : lecture du port P1, Wi-Fi.
23. [Fil Home Assistant](https://community.home-assistant.io/t/domintell-custom-component/185481?page=6), [fil openHAB](https://community.openhab.org/t/domintell-integration/48184), [fil iRidium](https://iridiummobile.userecho.ru/communities/18/topics/25707-scanning-the-domintell-bus-with-the-new-module?lang=en), [bibliothèque Python](https://pypi.org/project/python-domintell) : intégrations communautaires et leurs limites.

!!! note "À confirmer auprès des fabricants"
    La tolérance réelle des entrées DISM au-delà de 10 m, la tension et le courant sur le contact, l'isolation des entrées et le nombre de communs ; la confirmation écrite qu'aucun lien entrée → sortie ne survit à l'arrêt du Master, et la liste exacte des commandes manuelles sans Master ; le type des relais DMR02, DBIR01 et DTRV01 et leur état au retour de tension ; les protections de la DALI05, le caractère TBTS du bus, la tension d'essai bus / 230 V et les parafoudres recommandés ; le verrouillage des deux sens des volets ; le nombre de modules par DGQG04 (600 ou 60) et la disponibilité du DHUB01 ; les conditions d'accès à GoldenGate pour un propriétaire ; une sortie cyclique du Master pour le relais de garde ; la commande d'un fil pilote par relais ; les prix installateur ; la situation financière de la société au registre belge.
