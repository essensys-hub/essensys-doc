---
title: "Autocritique des études V1"
description: "Ce que le conseil d'autocritique du 21 octobre 2026 reproche aux études V1 Revolution Pi, Arduino Opta et Raspberry Pi, et ce que la V2 en garde."
---

# Autocritique des études V1

Le 21 octobre 2026, un conseil d'autocritique a jugé les trois études V1 sur une exigence nouvelle, née de la foudre du 9 août 2026 : si le contrôleur, un automate ou un Raspberry Pi grille, les 63 boutons muraux doivent toujours commander leurs lumières, leurs volets et leurs variateurs, en filaire. Aucune des trois ne la tient : chacune met un calculateur entre le bouton et le relais, sauf pour les 8 variateurs. Le verdict et la méthode sont sur la page [du conseil](conseil.md) ; l'architecture retenue est l'[étude V2 « filaire d'abord »](filaire-d-abord.md).

| Étude V1 | Si le calculateur meurt | Verdict |
| --- | --- | --- |
| [Revolution Pi](#revolution-pi) | 55 boutons sur 63 perdus | Transformer : la Connect 5 reste candidate pour la couche domotique, achetée en dernier |
| [Arduino Opta](#arduino-opta) | Sa zone perdue ; le bloc 24 V commun éteint les trois | Abandonner ; garder le fusible par zone |
| [Raspberry Pi et Ethernet](#raspberry-pi-et-ethernet) | Sa zone perdue, lumières éteintes | Abandonner les cartes ; garder l'isolement des entrées, le relais de garde et le battement de cœur |

Chaque section reprend l'autocritique ajoutée en tête de la copie de travail V2 de l'étude ; le texte des études V1 reste inchangé.

## Revolution Pi { #revolution-pi }

Étude V1 figée : [Revolution Pi](../revolution-pi.md).

Le conseil demande de transformer l'étude : les 63 boutons quittent la Revolution Pi, désormais candidate pour la couche domotique et achetée en dernier. Le Mainteneur juge la Revolution Pi surdimensionnée et préfère un serveur d'E/S léger, piloté par la passerelle. L'îlot filaire vient d'abord, zone par zone et sans logiciel.

### Pourquoi

L'étude échoue à l'exigence V2 par construction, et le conseil y relève dix faiblesses vérifiées dans son texte. Chaque puce cite la section, puis les conseillers qui l'ont relevée.

- **Contrôleur unique** : sa panne prive 55 boutons sur 63 de leur charge, décompte à confirmer au relevé. C'est une régression : aujourd'hui, un BP planté laisse les boutons actifs (Synthèse, « Modes dégradés » ; Automaticien, Mainteneur, Électricien).
- **Service Go figé** : les sorties restent figées et les boutons morts jusqu'au chien de garde applicatif, logé dans le même Linux. Un fil pilote figé sur « arrêt » laisse les radiateurs coupés, au risque du gel (« Modes dégradés » ; Automaticien, Sûreté).
- **Repli** : la matrice de repli éteint toutes les lumières et oublie le cumulus. Des télérupteurs commandés par les boutons y figurent, mais comme option à arbitrer, non chiffrée (« Modes dégradés » ; Électricien, Automaticien, Avocat du diable).
- **Connect 5 de rechange** : c'est celle du banc, déjà montée dans l'armoire. Une vraie rechange, 777 € HT avec une DIO, manque au budget (« Modes dégradés », « Nomenclature et budget » ; Sûreté, Mainteneur).
- **Alimentation** : le pire cas atteint 150 W, soit 100 % du HDR-150-24, et seule une règle logicielle l'évite. Un tableautier ne dépasse pas 80 % environ (« Alimentation et autonomie » ; Électricien, Sûreté, Avocat du diable).
- **Autonomie** : les 8 h annoncées prennent 78 % d'une batterie neuve à 20 °C, et 98 % en fin de vie. Aucune marge ne reste pour le froid (« Alimentation et autonomie » ; Sûreté).
- **Statut réel des relais** : promis, il n'est que l'ordre donné. Les 76 entrées servent aux 63 boutons et à 13 autres signaux ; aucune ne relit un relais (Synthèse, « Correspondance fonctionnelle » ; Automaticien, Sûreté).
- **Isolement des entrées DIO** : annulé, car la fiche DIO exige trois sources indépendantes. Un seul bus 24 V alimente ici la base, les DIO, les bobines et le commun des boutons (« Gamme », « Alimentation et autonomie » ; Spécialiste foudre).
- **Foudre** : l'étude annonçait la « fin des points faibles révélés par la foudre ». Ses frontières isolées oublient pourtant les 63 lignes de boutons, et aucun parafoudre n'est prévu. Son essai CEM ne vise que l'émission, sans onde de choc (Synthèse, « Correspondance fonctionnelle », « Risques et points ouverts » ; Spécialiste foudre, Automaticien).
- **Coffret photovoltaïque** : l'étude accole le coffret ajouté à droite, là où le retex place le coffret photovoltaïque, à quelques centimètres. Elle ne le cite jamais (« Câblage de migration et évolutivité » ; Spécialiste foudre, Avocat du diable).

### Ce qu'on garde pour la V2

Cinq éléments passent dans la V2, avec des règles nouvelles.

- **Câblage de migration** : répartiteur X1, blocs de phase X3, jonctions IDC et plan de bornage, avec un bloc par disjoncteur. Il se pose zone par zone, disjoncteurs consignés, sans journée de bascule.
- **Connect 5** : candidate pour la couche domotique, derrière des contacts secs et un relais de garde, avec une vraie rechange.
- **Relais Finder 38.51** : réemployés en couplage, comme contacts secs du contrôleur, ou devant un télérupteur à bobine 230 V faute d'attestation.
- **Variateurs EUD12D-UC** : entrée locale sur la source de commande de zone, réglage en PRI 1 ou 5.
- **Barrières de 4 kV** : FL ISOLATOR, tenue à vérifier, et bloc de classe II aux frontières de l'îlot domotique.

L'architecture retenue est décrite dans l'[étude « filaire d'abord »](filaire-d-abord.md), et chaque avis cité se lit dans le [rapport du conseil](conseil.md).

## Arduino Opta { #arduino-opta }

Étude V1 figée : [Arduino Opta](../arduino-opta.md).

Verdict : à abandonner, car le découpage par zone n'arrête pas les causes communes, et les entrées non isolées reprennent la topologie du 9 août. Face à l'exigence V2, l'Opta garde la panne d'aujourd'hui : un cerveau mort, une zone morte.

Ce que l'étude promettait, et ce que le conseil a établi :

- **Panne unique** (Synthèse, Modes dégradés) : la Synthèse promet « pas de panne unique pour les boutons ». Les Modes dégradés montrent pourtant que le bloc 24 V du bus secteur éteint les trois zones à la fois. Relevé par l'Électricien, l'Automaticien, la Sûreté, le Mainteneur et l'Avocat du diable.
- **Causes communes** (Migration logicielle, Comparaison avec la Revolution Pi) : les quatre Opta « partagent un même code », mis à jour ensemble ; le gain de résilience annoncé ne vaut que pour une panne isolée. La Sûreté compte encore cinq modes qui privent toute la maison de ses boutons. Relevé aussi par l'Automaticien et le Spécialiste foudre.
- **Entrées non isolées** (Correspondance fonctionnelle) : les 63 lignes de boutons arrivent sur des entrées non isolées, qui partagent le 0 V du bus 24 V des trois zones. La règle des 4 kV aux frontières de l'îlot oublie ces lignes. Relevé par le Spécialiste foudre, qui y reconnaît la topologie du 9 août, et par l'Électricien, la Sûreté et l'Avocat du diable.
- **Bus I2C des extensions** (Synthèse, Modes dégradés) : chaque Opta parle à ses extensions par un bus I2C, sans signal de vie. Leur repli n'est pas documenté : le fil pilote peut rester figé sur un ordre « arrêt » en plein hiver. Relevé par l'Automaticien, la Sûreté, l'Électricien et l'Avocat du diable.
- **Retour du secteur** (Modes dégradés) : chaque zone garde ses boutons « sans dépendre du BP », mais lui redemande l'état de ses sorties au retour du secteur. Le cas d'un Opta « BP » mort à ce moment n'est pas décrit. Relevé par l'Automaticien.
- **Coffrets à droite** (Synthèse, Architectures cibles) : l'étude demande environ 3,1 m de rail et deux coffrets « accolés à droite » du coffret actuel. Le retex y place le coffret photovoltaïque, à quelques centimètres ; l'étude ne le cite jamais. Relevé par le Spécialiste foudre et l'Avocat du diable.
- **Plateforme en transition** (Synthèse, Migration logicielle) : Mbed OS est arrêté, et le cœur Arduino sous Zephyr n'est déclaré stable que depuis fin juillet 2026. Le Mainteneur y ajoute seize firmwares à garder cohérents et un portage sous-estimé de 20 à 40 %. Relevé aussi par l'Électricien et l'Avocat du diable.
- **Ni parafoudre ni essai de choc** (Nomenclature et budget, Feuille de route) : le mot « parafoudre » n'apparaît pas dans l'étude. L'essai CEM de G1 ne vise que l'émission radio, et l'essai d'isolement de G2 ne dit rien de la tenue aux chocs. Relevé par le Spécialiste foudre, la Sûreté et l'Automaticien.
- **Lumières éteintes** (Modes dégradés) : la matrice de repli éteint les lumières quand l'Opta d'une zone se tait, et ses boutons ne les rallument plus. Relevé par l'Électricien et le Spécialiste foudre.

Ce qu'on garde pour la V2 :

- **Câblage de migration** : le répartiteur X1, les jonctions IDC, les blocs de phase X3 et le plan de bornage, avec un bloc par disjoncteur.
- **Fusible par zone** : il protège désormais la source de commande de chaque zone, à 1 A.
- **Logique des boutons dans leur zone** : l'idée reste, sans calculateur. Chaque bouton commande sa charge, alimenté par la source de commande de sa zone.
- **Commun ouvert pendant la migration** : le commun d'une zone reste ouvert tant que sa nappe est branchée sur un BA (Électricien).
- **Liaisons isolées entre coffrets** : des coffrets non accolés se relient par des liaisons isolées à 4 kV, comme l'étude le prévoit (Spécialiste foudre).

La suite est dans l'étude V2 [« filaire d'abord »](filaire-d-abord.md), et le détail des six avis dans le [rapport du conseil](conseil.md).

## Raspberry Pi et Ethernet { #raspberry-pi-et-ethernet }

Étude V1 figée : [Raspberry Pi et Ethernet](../raspberry-pi-ethernet.md).

Le conseil abandonne les cartes nœuds de cette étude, à relais soudés et à 230 V. Il en garde l'isolement des entrées, le monostable devenu relais de garde et le battement de cœur.

### Pourquoi

L'étude ne tient pas l'exigence V2 : un calculateur reste entre le bouton et le relais, sauf pour les 8 variateurs. Sa « Synthèse » promettait des boutons qui ne dépendent que de leur zone et des cartes dessinées contre la foudre, pour 3 160 € HT.

- **Repli** : un nœud mort prive sa zone de ses boutons et éteint ses lumières (« Modes dégradés et sécurité » ; Électricien, Spécialiste foudre). « Le repli tient sans logiciel » vaut pour les sorties, pas pour les boutons (Automaticien).
- **Causes communes** : le bloc 24 V secteur ou un défaut du firmware commun coupe les trois zones (« Modes dégradés et sécurité », « Logiciel » ; Sûreté, Automaticien). Pour cette étude, l'AMDEC de la Sûreté compte quatre modes qui privent toute la maison de ses boutons, foudre et chaleur comprises.
- **230 V** : les cartes maison portent le 230 V sans marquage CE ni qualification (« Synthèse » ; Électricien, Spécialiste foudre). Les ondes de choc prévues en G2 ne sont ni chiffrées ni outillées (« Feuille de route » ; Avocat du diable). Les communs de 16 A de la carte n'ont aucun essai d'échauffement (Sûreté).
- **Relais soudés** : réparer un relais collé arrête la zone et demande un fer à souder (« Nomenclature et coût par carte » ; Électricien, Sûreté).
- **Isolement** : les entrées des boutons sont isolées à 3 kV, pas aux 4 kV du retex (« Améliorations des schémas existants » ; Spécialiste foudre). Les lignes du nœud temps réel vers les fuites et la sirène ne sont pas isolées.
- **Supervision** : « Plus de défaut silencieux » ne tient pas (« Ethernet à la place de l'I2C » ; Sûreté). Le battement de cœur ne voit pas un contact collé.
- **Charge** : l'étude demande 19 à 28 semaines-personne avant la bascule, dont 6 à 9 d'électronique, à une seule personne (« Synthèse » ; Mainteneur, Avocat du diable). Le Mainteneur réévalue cette charge à 23 à 35 semaines, soit 9 à 14 mois à 20 h par semaine.
- **Coût** : sous la V2, l'avance de 2 300 € en matériel disparaît (« Synthèse » ; Électricien). L'amortissement « en 3 à 5 armoires » oublie l'écart de 15 000 à 30 000 € de logiciel que l'étude chiffre elle-même (« Comparaison » ; Mainteneur). En le comptant, il faut 9 à 17 maisons.
- **Implantation** : le coffret « accolé à droite » bute contre le coffret photovoltaïque, absent de l'étude (« Architecture proposée » ; Spécialiste foudre, Avocat du diable). Le retex demande 30 à 50 cm entre les câbles photovoltaïques et le coffret.

Sur le papier, l'étude reste pourtant la mieux conçue contre la foudre, selon le Spécialiste foudre. Ses entrées optocouplées en font la seule à traiter les lignes de boutons comme une frontière exposée (Électricien). Son principe, « plus une fonction est critique, moins elle dépend d'autres organes », devient celui de la V2, poussé jusqu'au bouton (Automaticien, Mainteneur).

Sources : [analyse experte du retex](../../../retex/foudre-2026/analyse-experte.md).

### Ce qu'on garde pour la V2

La V2 reprend quatre éléments de l'étude : trois pour l'îlot domotique, un pour l'îlot filaire.

- **Isolement des entrées** : l'îlot domotique lit les états par optocoupleurs, dans l'ordre connecteur, TVS, résistance, mais à 4 kV au moins (Spécialiste foudre).
- **Relais de garde** : le monostable devient un relais de garde, qui débranche la couche domotique dès que le contrôleur se tait (Automaticien).
- **Battement de cœur** : du contrôleur vers la passerelle, avec alerte, complété par des essais périodiques (Sûreté).
- **Câblage de migration** : répartiteur X1, blocs de phase X3, jonctions IDC et plan de bornage, communs aux trois études.

La suite est décrite dans [l'étude V2 « filaire d'abord »](filaire-d-abord.md) et dans [le rapport du conseil](conseil.md).
