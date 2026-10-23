---
title: "Sections de câbles : rigide, souple et embouts"
description: "Correspondance entre les fils rigides du logement et les fils souples à embouts de l'armoire ESSENSYS : section selon le disjoncteur, embouts, couleurs et cas où augmenter la section."
---

# Sections de câbles : rigide, souple et embouts

Ce cahier donne la correspondance entre les fils rigides de l'installation domestique (1,5 et 2,5 mm²) et les fils souples à embouts, plus faciles à poser dans l'armoire, pour choisir la bonne section à chaque liaison.

## La règle

La section ne dépend pas du fil, rigide ou souple : elle dépend du disjoncteur qui protège le circuit. Un souple de 1,5 mm² remplace un rigide de 1,5 mm² derrière un 16 A, et un souple de 2,5 mm² remplace un rigide de 2,5 mm² derrière un 20 A.

- **Même isolant, mêmes tableaux** : le souple H07V-K et le rigide H07V-U sont deux fils PVC de 450/750 V, à 70 °C en service. Les intensités admissibles de la NF C 15-100 sont les mêmes pour les deux.
- **Seule différence, la résistance** : l'âme souple (classe 5) résiste environ 10 % de plus que l'âme rigide (classe 1) : 13,3 contre 12,1 Ω/km en 1,5 mm². Dans l'armoire, c'est négligeable : 1 m de 1,5 mm² souple, aller et retour, fait chuter 0,43 V à 16 A, soit 0,2 % de 230 V.
- **Jamais une section de moins** parce que le fil est souple, court ou caché dans le coffret. Chaque conducteur placé derrière un disjoncteur doit pouvoir porter son calibre.
- **Toujours un embout** sur un fil souple : il tient les brins, évite qu'un brin s'échappe vers la borne voisine, et permet l'enfichage direct dans les bornes Wago.

« GW » n'est pas une désignation normalisée : ce cahier suppose qu'il s'agit du fil de câblage souple courant, le H07V-K. Le H05V-K, plus fin (300/500 V), sert aux petits courants de commande.

## Tableau de correspondance

On lit le tableau par le calibre du disjoncteur : il donne la section, valable en rigide comme en souple, puis l'embout du souple.

| Section (mm²) | Disjoncteur max (A) | Usages domestiques, NF C 15-100 | Souple H07V-K sous conduit, 2 conducteurs chargés (A) | Résistance max à 20 °C, rigide / souple (Ω/km) | Embout, code français |
| --- | --- | --- | --- | --- | --- |
| 0,75 | Fusible 1 A ici | Commande 24 V, signalisation | — | 24,5 / 26,0 | Bleu |
| 1 | Fusible 1 A ici | Commande 24 V | — | 18,1 / 19,5 | Rouge |
| 1,5 | 16 | Éclairage, volets roulants, prises (8 au plus), convecteurs jusqu'à 3 500 W, VMC et pilotage (2 A) | 17,5 | 12,1 / 13,3 | Noir |
| 2,5 | 20 | Prises (12 au plus), lave-linge, lave-vaisselle, four, cumulus, convecteurs jusqu'à 4 500 W | 24 | 7,41 / 7,98 | Gris |
| 4 | 25 | Convecteurs jusqu'à 5 750 W | 32 | 4,61 / 4,95 | Orange |
| 6 | 32 | Plaque de cuisson en monophasé, convecteurs jusqu'à 7 250 W | 41 | 3,08 / 3,30 | Vert |

Lecture : un circuit de volets protégé par un 16 A se câble en 1,5 mm², rigide dans les murs, souple à embout noir dans l'armoire. Le cumulus, protégé par un 20 A, demande du 2,5 mm², embout gris.

- **Exception du tableau Nexans** : le plancher chauffant de 3 400 W se câble en 2,5 mm² sous un 25 A.
- **Section minimale des circuits de pilotage** : 1,5 mm² sous un 2 A, selon le même tableau ; c'est le cas du fil pilote et de l'alimentation 230 V des sources de commande.
- **Commande en 0,75 ou 1 mm²** : réservée aux circuits TBT protégés par un fusible de 1 A, comme les commandes 24 V de l'étude V2. La fiche H05V-K limite le 0,5 mm² à 2 m et 3 A ; mieux vaut s'en passer.
- **Intensités du souple** : fiche Prysmian H07V-K, à 30 °C, conducteur seul dans son conduit. Elles baissent si l'air est plus chaud ou si les circuits sont groupés (section « Quand augmenter la section »).

Sources : [Nexans, tableau des sections et calibres (NF C 15-100, tableau 10-1F)](https://home.nexans.fr/app/uploads/2022/03/Tableau-section-et-calibres.pdf), [fiche Prysmian H07V-K](https://fr.prysmian.com/sites/fr.prysmian.com/files/media/documents/FT%20H07%20V-K.pdf), [résistances CEI 60228 (Bayka)](https://www.bayka.de/en/service/technical-information/conductor-resistance), [embouts Chorus, code français](https://www.thierry-lequeu.fr/data/A4FP063.pdf), [fiche H05V-K (Sonepar)](https://res.cloudinary.com/sonepar-fr/raw/upload/s--pITqvyHM--/v1/documents/42/20034423.pdf).

## Dans l'armoire ESSENSYS

Le répartiteur X1 est le point de passage du rigide au souple : le fil du logement y arrive tel quel, et tout ce qui en repart est souple à embout. Chaque liaison prend la section du disjoncteur de son circuit, sauf la commande 24 V, protégée par ses fusibles : F1 de 1 A pour les boutons, F2 de 0,5 A au plus pour les contacts domotiques.

| Liaison | Protection en amont | Fil | Section | Embout (code français) |
| --- | --- | --- | --- | --- |
| Fil du logement → étage haut de X1 | Disjoncteur du circuit | Rigide existant, inchangé | Celle du circuit | Aucun : le rigide s'enfiche directement |
| Pont X1 → bloc de phase X3 | Disjoncteur du circuit, 16 A | Souple H07V-K | 1,5 mm² (2,5 mm² sous 20 A) | Noir (gris) |
| Bloc X3 → télérupteur, relais, variateur | Même disjoncteur | Souple H07V-K | Comme le pont | Noir (gris) |
| Contact de sortie → départ X1 vers la charge | Même disjoncteur | Souple H07V-K | Comme le pont | Noir (gris) |
| Second contact du télérupteur → bobine 230 V du relais de recopie | Disjoncteur du circuit d'éclairage | Souple H07V-K | Comme le pont | Noir (gris) |
| Neutre du circuit, bobine de recopie comprise | Même disjoncteur | Souple H07V-K bleu | Comme la phase | Noir (gris) |
| Terre (PE) | — | Souple H07V-K vert-jaune | Comme la phase | Noir (gris) |
| Disjoncteur 2 A → source de commande de zone (230 V) | 2 A | Souple H07V-K | 1,5 mm² | Noir |
| Fil pilote | 2 A | Souple H07V-K | 1,5 mm² | Noir |
| Source 24 V → fusible F1 → bornier X4, commun des boutons | Fusible F1, 1 A | Souple H05V-K | 0,75 mm², ou 1 mm² | Bleu (rouge) |
| Source 24 V → fusible F2 → relais de garde → bornier X4, commun domotique | Fusible F2, 0,5 A au plus | Souple H05V-K | 0,75 mm² | Bleu |
| Bornier X4 → bobine, entrée locale d'un variateur | Fusible F1, 1 A | Souple H05V-K | 0,75 mm², ou 1 mm² | Bleu (rouge) |
| Contact du relais de recopie → entrée isolée de la domotique | Source de la domotique | Souple H05V-K | 0,75 mm² | Bleu |
| Poussoirs muraux → jonction IDC → X4 | Fusible F1, 1 A | Nappe existante | Inchangée | Aucun : borne à vis de l'interface |

Quatre règles en plus :

- **Un bloc X3 derrière un 20 A** : tout ce qui en part passe en 2,5 mm². Les bornes Wago 2002 acceptent le souple à embout jusqu'à 2,5 mm², et leur courant nominal est de 24 A.
- **Neutre de la recopie** : la bobine 230 V du relais de recopie revient sur le neutre de son propre circuit, jamais sur un neutre voisin, que la NF C 15-100 interdit de partager ; sinon le différentiel peut déclencher.
- **Couleurs** : bleu réservé au neutre, vert-jaune à la terre. Pour la commande 24 V, une couleur qu'aucune pieuvre de la maison ne porte : on la choisit après avoir relevé les couleurs des lignes commandées dans le dossier d'exécution. Par exemple blanc pour les boutons, et rose pour l'îlot domotique, dont le 0 V ne touche jamais celui des boutons ; à fixer avec l'électricien.
- **Séparation de la TBTS** : les fils 24 V passent dans leur propre goulotte, ou sont isolés pour la tension la plus élevée du coffret. C'est la règle de séparation de la TBTS, que l'électricien appliquera ; le bornier X4 a déjà sa cloison dans l'étude V2.

Sources : [Nexans, tableau des sections et calibres](https://home.nexans.fr/app/uploads/2022/03/Tableau-section-et-calibres.pdf), [borne Wago 2002-1401](https://buerklin.com/en/p/wago/series-terminals/2002-1401/09H4219), [bornes Wago série 2002](https://wago.com/lv/rail-mount-terminal-blocks/4-conductor-through-terminal-block/p/2002-1801), [étude V2 filaire d'abord](filaire-d-abord.md).

## Embouts et cosses

Dans l'armoire, chaque fil souple reçoit un embout isolé à sa section ; les cosses ne servent qu'aux raccords vissés sur goujon ou barrette.

| Pièce | Où | Règle |
| --- | --- | --- |
| Embout simple isolé, à collerette | Toute borne à vis ou à ressort : Wago, disjoncteurs, télérupteurs, relais, sources | Un embout par fil, de la section du fil |
| Embout double | Deux fils dans une même borne à vis, quand la fiche de l'appareil l'admet | Jamais sur les Wago du répartiteur : un fil par point |
| Cosse à œillet ou à fourche | Barrette de terre, borne à goujon | Pas dans la cage d'un appareil modulaire |

Le piège des couleurs : deux codes coexistent. En code français, un embout bleu fait 0,75 mm² (Legrand Starfix) ; en code DIN, un embout bleu fait 2,5 mm² (Weidinger), et un gris fait 0,75 mm² (Knipex). Un embout de 2,5 mm² serti sur un 0,75 mm² ne serre rien.

- **Un seul code dans l'armoire** : acheter tous les embouts chez une même marque, et lire la section imprimée sur le sachet, pas la couleur.
- **Code français, pour mémoire** : 0,5 mm² blanc, 0,75 bleu, 1 rouge, 1,5 noir, 2,5 gris, 4 orange, 6 vert (catalogue Chorus).
- **Sertissage** : une pince à cliquet, à profil carré ou trapézoïdal, réglée à la section ; le cuivre arrive au bout de la douille, sans brin rebroussé. On tire sur chaque fil serti : il ne doit pas bouger.
- **Dénudage** : les bornes Wago 2002 demandent 10 à 12 mm. La longueur de douille qui convient à chaque borne se lit sur sa fiche.
- **Wago 2002** : section nominale 2,5 mm², de 0,25 à 4 mm² ; le rigide et le souple à embout s'enfichent sans outil. Pour retirer un fil, on ouvre la borne avec son outil de manœuvre, un tournevis plat de la largeur indiquée par Wago.
- **Autres appareils** : la section maximale et le nombre de fils par borne d'un télérupteur, d'un relais ou d'un disjoncteur se lisent sur sa fiche, avant de choisir l'embout.

Sources : [embout Legrand Starfix 0,75 mm², bleu](https://www.legrand.fr/pro/catalogue/sachet-dembouts-de-cablage-a-collerette-isolante-starfix-simple-unitaire-pour-conducteurs-section-075mm2-bleu), [embout DIN 2,5 mm², bleu (Weidinger)](https://datasheets.weidinger.eu/fr/wl72761), [embout DIN 0,75 mm², gris (Knipex)](https://bilder01.dabag.ch/documents/kataloge/knipex/9799351_fr.pdf), [embouts Chorus, code français](https://www.thierry-lequeu.fr/data/A4FP063.pdf), [bornes Wago série 2002](https://wago.com/lv/rail-mount-terminal-blocks/4-conductor-through-terminal-block/p/2002-1801), [borne Wago 2002-1401](https://buerklin.com/en/p/wago/series-terminals/2002-1401/09H4219).

## Quand augmenter la section

Le couple 1,5 mm² sous 16 A et 2,5 mm² sous 20 A reste la règle. On prend une section de plus pour un fil qui porte tout le courant d'un circuit dans un coffret chaud ou une goulotte chargée.

- **Chaleur** : les intensités sont données pour 30 °C. Pour un isolant PVC, on les multiplie par 0,94 à 35 °C, 0,87 à 40 °C et 0,79 à 45 °C.
- **Groupement** : dans un même conduit, le souple de 1,5 mm² porte 17,5 A avec deux conducteurs chargés, 15,5 A avec trois, 14 A avec quatre et 12 A avec six.
- **Longueur** : dans l'armoire, la chute de tension ne compte pas ; elle compte pour les grandes longueurs de la maison, que l'électricien a déjà dimensionnées.

| Pont X1 → X3 sous un 16 A, trois conducteurs chargés, coffret à 40 °C | Intensité à 30 °C (A) | Coefficient à 40 °C | Intensité admissible (A) | Verdict |
| --- | --- | --- | --- | --- |
| 1,5 mm² | 15,5 | 0,87 | 13,5 | Juste, sous les 16 A |
| 2,5 mm² | 21 | 0,87 | 18,3 | Marge |

Lecture : le tableau 10-1F de la NF C 15-100 suppose des conditions de pose courantes. Dans un coffret plein et chaud, l'électricien peut demander du 2,5 mm² pour les ponts de phase qui portent tout un circuit. C'est toujours permis, et les Wago 2002 prennent le 2,5 mm² à embout ; les fils d'un seul appareil restent à la section du circuit. La température réelle du coffret se mesure avec l'enregistreur prévu dans l'étude V2.

Sources : [facteurs de correction PVC (LAPP, DIN VDE 0298-4)](https://www.thierry-lequeu.fr/data/T12_Tableaux_fondamentaux_des_intensites.pdf), [fiche Prysmian H07V-K](https://fr.prysmian.com/sites/fr.prysmian.com/files/media/documents/FT%20H07%20V-K.pdf), [Nexans, tableau des sections et calibres](https://home.nexans.fr/app/uploads/2022/03/Tableau-section-et-calibres.pdf).

## À faire valider par l'électricien

Le relevé fixe la section de chaque liaison ; ces points sont à trancher avec lui avant de commander le fil et les embouts.

- [ ] Relever le calibre de chaque disjoncteur qui alimente l'armoire : il donne la section de chaque circuit.
- [ ] Vérifier la section et l'état des fils rigides du logement à leur arrivée dans le coffret.
- [ ] Décider si les ponts de phase X1 → X3 passent en 2,5 mm², selon la température mesurée du coffret.
- [ ] Choisir une seule marque d'embouts, donc un seul code couleur, et une pince à sertir à cliquet adaptée.
- [ ] Fixer la couleur des fils 24 V et leur cheminement séparé du 230 V.
- [ ] Lire, sur la fiche de chaque télérupteur, relais et source, la section maximale et le nombre de fils admis par borne.
- [ ] Confirmer la section des fils de commande, 0,75 ou 1 mm², derrière les fusibles F1 (1 A) et F2 (0,5 A au plus).

## Sources

- Sections et calibres : [Nexans, tableau des sections et calibres (NF C 15-100, tableau 10-1F)](https://home.nexans.fr/app/uploads/2022/03/Tableau-section-et-calibres.pdf).
- Fils : [fiche Prysmian H07V-K](https://fr.prysmian.com/sites/fr.prysmian.com/files/media/documents/FT%20H07%20V-K.pdf), [fiche H05V-K (Sonepar)](https://res.cloudinary.com/sonepar-fr/raw/upload/s--pITqvyHM--/v1/documents/42/20034423.pdf), [résistances CEI 60228 (Bayka)](https://www.bayka.de/en/service/technical-information/conductor-resistance), [facteurs de correction PVC (LAPP, DIN VDE 0298-4)](https://www.thierry-lequeu.fr/data/T12_Tableaux_fondamentaux_des_intensites.pdf).
- Embouts : [Legrand Starfix 0,75 mm², bleu](https://www.legrand.fr/pro/catalogue/sachet-dembouts-de-cablage-a-collerette-isolante-starfix-simple-unitaire-pour-conducteurs-section-075mm2-bleu), [DIN 2,5 mm², bleu (Weidinger)](https://datasheets.weidinger.eu/fr/wl72761), [DIN 0,75 mm², gris (Knipex)](https://bilder01.dabag.ch/documents/kataloge/knipex/9799351_fr.pdf), [catalogue Chorus, code français](https://www.thierry-lequeu.fr/data/A4FP063.pdf).
- Bornes : [Wago 2002-1401](https://buerklin.com/en/p/wago/series-terminals/2002-1401/09H4219), [Wago série 2002](https://wago.com/lv/rail-mount-terminal-blocks/4-conductor-through-terminal-block/p/2002-1801).
- Projet : [étude V2 filaire d'abord](filaire-d-abord.md).
