# Diagnostic et remise en service après une surtension

Procédure à suivre quand une installation Essensys (BP SC944D et BA SC940D, SC941C, SC942C) ne répond plus après un orage, une surtension réseau ou un défaut d'isolement. Elle est issue du [retour d'expérience foudre 2026](../retex/foudre-2026/synthese.md) ; le détail technique (mécanisme, seuils, schémas) est dans l'[analyse experte](../retex/foudre-2026/analyse-experte.md#diagnostic).

!!! danger "Sécurité d'abord"
    Après une surtension, la barrière entre la TBTS et le 230 V peut être rompue : le câble de bus, les nappes d'entrées et les capteurs peuvent se trouver au potentiel du secteur.
    **Toute mesure sous tension est faite par une personne habilitée** (BR ou BE Mesurage). Toute intervention dans le coffret se fait **après consignation selon la NF C 18-510**. Si vous n'êtes pas habilité, faites intervenir un électricien.

!!! warning "Opération de maintenance manuelle"
    Aucun harnais de test, script de non-régression ni stimulus automatisé ne doit viser une armoire réelle. Toutes les étapes ci-dessous sont manuelles et consignées.

Référence des exigences : change OpenSpec `i2c-surge-protection-2026-10-007` (dépôt `essensys-board-SC944D`), capacités `aux-box-interconnect` et `i2c-bus-fault-containment`.

## Vue d'ensemble

| Étape | Objet | Qui |
|---|---|---|
| E-1 | Sécurité : mesure 0 V–PE, consignation, isolement | Personne habilitée |
| E0 | Observation, porte ouverte, sans rien toucher | Mainteneur, en présence d'une personne habilitée |
| E1 / E2 | Isoler la carte fautive par débranchement | Mainteneur, 230 V consigné |
| Établi | Mesures du BP et des BA déposés | Mainteneur |
| Réception | Critères de remise en service | Mainteneur + électricien |

## E-1 : sécurité, avant de toucher quoi que ce soit

1. **Ne rien introduire dans le coffret ouvert** (outil, mètre, pointe de touche) tant qu'il n'est pas consigné. Les photos se prennent porte ouverte, sans rien toucher.
2. **Mesure 0 V–PE, 230 V présent, sans toucher les cartes** (personne habilitée) : tension alternative entre un 0 V TBT accessible (moins de la batterie du BP, borne GND) et le PE, au VAT ou au multimètre en mode basse impédance (LoZ).
    - Quelques volts qui s'effondrent en LoZ : normal (couplage capacitif).
    - Plusieurs dizaines de volts, ou plus, qui tiennent en LoZ : **arrêt**. Consigner l'ensemble et appeler un électricien.
3. **Consigner** (NF C 18-510) :
    - le disjoncteur du BP **et tous les départs** commandés par les BA (il peut y en avoir plusieurs par BA) ;
    - la batterie du BP (J56-4) ;
    - **toute source autonome du site** (installation photovoltaïque, batterie de stockage, sortie secourue) : elle peut maintenir des circuits sous tension disjoncteur général ouvert. Le côté photovoltaïque (chaînes DC, batterie haute tension) est réservé à l'installateur PV ;
    - vérifier l'absence de tension au VAT (NF EN 61243-3) sur chaque bornier de BA et entre J1/J2 et le PE.
4. **Charges figées** : les relais bistables d'un BA hors service restent dans leur dernier état. Couper au disjoncteur toute charge restée sous tension.
5. **Isolement à 500 V continu**, avant toute remise sous tension (voir [Établi](#mesures-a-letabli)) : sur le BP **et sur les trois BA**, pas seulement sur le BA en panne.
6. **Couper toute liaison Ethernet en cuivre** entre un équipement relié au PE (onduleur, borne, équipement extérieur) et le commutateur du BP : débrancher côté commutateur, étiqueter « ne pas rebrancher en cuivre », passer l'équipement en Wi-Fi ou en fibre.
7. **Oscilloscope** : relié à la terre, sa pince de masse va **uniquement** sur GND (J31-3 ou J1-3). Tant que l'isolement n'est pas vérifié, utiliser un oscilloscope sur batterie ou une sonde différentielle.
8. **Ne pas sonder J31/J1/J2 avec des pointes nues** : la broche 4 (+15 V, sans fusible) est voisine des lignes I2C. Un glissement de pointe recrée la panne. Mesurer avec un connecteur femelle aux fils sertis et repérés, ou sur les points de test (JT10/JT11, pastilles de R155/R156, cathodes de D33/D34 au BP ; cathodes de D1/D2 et pastilles de R1/R2 sur un BA).

**Mode de travail recommandé pour E0 à E2** : tout le 230 V consigné, transformateur débranché, BP alimenté par une **alimentation de laboratoire flottante** de 22 à 24 V continu (limitée à 1,5–2 A) sur J56-1/J56-2. La logique des BA n'a besoin que du +15 V fourni par le BP.

## E0 : observer, porte ouverte, sans rien toucher

| Indice | Lecture | Interprétation |
|---|---|---|
| LED DL1 (fenêtre « ÉTAT ») de chaque BA | **Filmer 10 s** : un éclair bref environ chaque seconde quand le PIC tourne | Toutes éteintes : +15 V du bus perdu. Une seule éteinte : ce BA n'est pas alimenté ou son PIC est arrêté (cas le plus fréquent) |
| LED « TÉLÉINFO » du BP | Fixe ou clignotante | Fixe : MCF vivant. LED verte du RJ45 : PHY vivant |
| Index 12 (`comm_faults`) | Bits 0x04 = SC940D (0x11), 0x08 = SC942C (0x12), 0x10 = SC941C (0x13) | Ne se met à jour qu'**après une commande** vers le BA : envoyer une commande d'éclairage (pas de volet) à chaque BA, puis relire `(index 12 & 0x1C)` |
| Composants visibles | TVS fendues ou noircies, perles, connecteurs J31/J1/J2, varistances des variateurs | Indique la porte d'entrée de la surtension |

Relever aussi, avant expiration des historiques, les horodatages disponibles (journaux du réseau local, supervision des sources autonomes, dernière commande BA réussie côté serveur) et les conserver dans le dossier privé de l'installation.

!!! tip "Voir ce qui passe réellement sur le bus"
    L'index 12 dit qu'un BA ne répond pas, mais pas pourquoi. L'[espion I2C passif](../debug/espion-i2c.md) montre, sans rien émettre, si le BA est absent (NACK d'adresse), s'il rejette des trames corrompues, ou si une ligne du bus est bloquée.

## E1 / E2 : isoler la carte fautive par débranchement

Le 230 V reste consigné ; le BP est sur l'alimentation de laboratoire flottante.

1. **Retirer entièrement** le câble de bus du BA suspect, des deux côtés. Ne laisser aucun bout de câble branché d'un seul côté.
2. Envoyer une commande à chacun des BA restants, relire l'index 12. S'ils répondent, le BA retiré tenait le bus.
3. Sinon, retirer le BA suivant, et ainsi de suite jusqu'au BP seul.
4. Rebrancher depuis le BP **un BA à la fois**, en mesurant au BP l'écart ΔV entre +5VS et chaque ligne au repos. La carte fautive est celle dont le raccordement fait croître cet écart de plus de 50 mV, ou empêche les autres BA d'acquitter.

| ΔV au repos (rail +5 V local − ligne) | Interprétation |
|---|---|
| ≤ 40 mV | Lignes libres. Si les BA ne répondent pas : NACK (translateur U19, PIC hors service) → oscilloscope |
| 40 mV à 0,5 V | Fuite de 50 µA à 0,6 mA : TVS fatiguée |
| Ligne entre 0,6 et ≈ 3 V | BA non alimenté qui se réalimente par ses diodes, ou forte fuite |
| Ligne ≈ 0 V | Court-circuit franc : TVS, U19, ou broches RC6/RC7 d'un PIC |

!!! danger "BREAKING — un BA non alimenté ne reste jamais raccordé au bus"
    Un BA privé d'alimentation se réalimente par ses lignes SDA/SCL et bloque tout le bus. Il est **débranché des deux côtés** tant qu'il n'est pas réparé. Exigence : `aux-box-interconnect` — *Déconnexion individuelle d'un BA*.

## Mesures à l'établi

### Fuite carte par carte et isolement (BP et chaque BA)

- **Isolement à 500 V continu**, carte nue : toutes les bornes 230 V reliées ensemble contre **toutes** les broches TBT reliées ensemble (BA : J1, J2, J3, ICSP ; BP : J3, J31, J56-3, blindage RJ45). Commencer par le SC941C (pièces d'eau), puis les deux autres BA et le BP.
    - > 100 MΩ : carte conforme ;
    - 10 à 100 MΩ : nettoyer, sécher, refaire l'essai ;
    - < 10 MΩ : **carte écartée**, pas de remise en service.
- **Inspection à la loupe** de la zone J1/J2 – K1 (et VR1 sur le SC940D) de chaque BA : un essai en continu ne révèle pas un amorçage en impulsion. Toute trace d'amorçage est consignée.
- **Fuite des écrêteurs, carte par carte** : BA alimenté seul sous 15,0 V par J1-4 (+) / J1-3 (−), câble de bus débranché ; écart entre le +5 V local et chaque ligne. Le +5 V varie de 4,83 à 5,03 V d'une carte à l'autre : la fuite se mesure toujours **en relatif, carte par carte**. D1/D2 sont remplacées si l'écart dépasse 100 mV (≈ 10 µA).

### BP (SC944D)

Hors tension, batterie débranchée :

| Mesure | Valeur saine |
|---|---|
| D33/D34 en mode diode (+ sur GND) | 0,55 à 0,70 V |
| Continuité L30, L32 / L31 | < 1 Ω / < 0,1 Ω |
| J32 (RJ45) : broches 1 ↔ 3 | ≈ 150 Ω |
| J32 : 8 contacts reliés contre GND, sous 500 V | > 100 MΩ |

Sous tension (alimentation flottante 22–24 V, rien sur J31) : +15VS ≈ 15,2 V, +5VS 4,83–5,03 V, +3V3S 3,3–3,4 V, BA_ALIM ≈ 15 V, **EN de U19 entre 3,6 et 4,4 V**, puis test fonctionnel de U19 dans les deux sens (une ligne mise à GND côté connecteur doit faire descendre JT10/JT11 sous 0,1 V, et réciproquement). À l'oscilloscope, à l'envoi d'une commande : START, 0x22, NACK, STOP à 50 kHz, niveau bas < 0,6 V.

### BA (SC940D, SC941C, SC942C)

Toujours comparer à un BA sain, dans la même polarité. **Commencer par l'alimentation**, avant l'I2C :

| Mesure | Valeur saine |
|---|---|
| Rail « +12V » (cathode de D3) ↔ GND | ≈ 0,8 kΩ |
| D3, D6 en mode diode ; U1 (VIN, SW, BOOST) ; FI1 | Pas de court-circuit |
| J1-1 (SDA) ↔ +5 V, puis J1-2 (SCL) ↔ +5 V | ≈ 10 kΩ |
| J1-1 ↔ J1-2 | ≈ 20 kΩ |
| Sous 15,0 V : +5 V après L2 | 4,83 à 5,03 V |

Test autonome : un maître I2C **5 V** sur J1-1/2/3 doit obtenir l'acquittement de l'adresse du BA (0x11, 0x12 ou 0x13).

## Réparation et programmation

- **Avant toute retouche lourde du BP**, sauvegarder sa flash par BDM.
- Remplacer les composants défaillants (TVS D33/D34 du BP en SMF5V0A-E3-08, U19 si son test échoue ; sur le BA : U1, C2, D6, D3, FI1 selon le diagnostic, varistances des variateurs SC943).

!!! danger "Interdiction de flasher un build non qualifié"
    - **BP** : seule l'image de production **`.S19` 099-37** (`essensys-board-SC944D/SC944D/Prog/099-37/`) peut être flashée. Jamais un nouveau build : le pilote I2C de production n'est pas reconstitué, et un rebuild réintroduit des attentes infinies sur le bus.
    - **BA** : seul le `.hex` **v1.7 du type** de la carte (pièces de vie, pièces d'eau, chambres), après lecture de l'EEPROM. Jamais le build `essensys-gcc`.
    - Un nouveau firmware n'est déployé qu'après qualification sur banc avec toute la suite de non-régression.

## Critères de réception

| Vérification | Critère |
|---|---|
| SDA/SCL au repos, tout branché, à J31 et au dernier BA | ΔV ≤ 40 mV par rapport au +5 V local |
| Écart statique de 0 V (ΔVg) entre J31-3 et J1-3 du dernier BA, relais monostables collés | ≤ 0,1 V : retouche 47 Ω admise. > 0,12 V : liaison 0 V équipotentielle (carte N2, ou renfort N1) posée avant remise en service |
| BA_ALIM au dernier BA | ≥ 14 V |
| Niveau bas BA → BP, mesuré au MCF | < 0,85 V |
| Niveau bas BP → BA, mesuré au PIC | < 1,2 V (mesure obligatoire) |
| Temps de montée de 0 à 3,45 V, au BA le plus éloigné | < 4 µs |
| Isolement | Essais 500 V réussis sur les trois BA et le BP |
| Ethernet | Aucun équipement relié au PE en cuivre sur le commutateur du BP |
| Fonctionnement | Une commande vers chaque BA réussit, `(index 12 & 0x1C)` revient à 0, aucun blocage pendant 24 h |
| Configurations | **Renvoyées pour tous les BA** : modifier chaque paramètre (modes des variateurs, temps d'extinction, temps des volets) puis revenir à sa valeur. Après un changement de PIC, corriger le mode des variateurs |

À la remise sous tension, l'électricien refait la mesure 0 V–PE en LoZ de l'étape E-1. Toutes les mesures sont consignées (dossier privé de l'installation) et l'intervention est tracée dans un ticket `Bug`.

## Relancer les BA sans ouvrir le coffret

Couper le disjoncteur secteur du BP pendant **au moins 13 s** (20 s pour la marge). Le BP passe sur batterie, coupe le +15 V des BA au bout d'environ 12 s, puis le rétablit environ 1 s après le retour du secteur.

Prérequis :

- **cavalier J58 fermé** (à vérifier visuellement : ouvert, le +15 V des BA reste permanent et la coupure est sans effet) ;
- **batterie du BP présente** ;
- **`Mode_Test` = 0**.

Effet de bord : les relais monostables retombent.

## Règles BREAKING

!!! danger "À appliquer sur tout le parc"
    1. **Un BA non alimenté ne reste pas raccordé au bus.** Son câble est retiré des deux côtés jusqu'à sa réparation.
    2. **Un BA préparé pour un module d'isolement (MIB)**, dont les écrêteurs de ligne sont déposés, **n'est jamais raccordé directement au bus**. Son connecteur côté isolé est d'une autre série, et son second connecteur de chaînage est neutralisé et étiqueté « ne pas raccorder sans module ». Exigence : `aux-box-interconnect` — *Module d'isolement pour BA déportés*.

Voir aussi le guide [Protection contre les surtensions](protection-surtensions.md).
