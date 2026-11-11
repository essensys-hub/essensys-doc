# Sauvegarde du firmware du BP

Cette page décrit comment lire et sauvegarder le firmware du boîtier principal (BP, carte SC944D, processeur MCF52259) **sans CodeWarrior ni pod P&E**, avec un Raspberry Pi Pico branché sur le connecteur de debug **J33**.

L'outil est **en lecture seule** : il n'efface et n'écrit jamais la flash. Il fait partie de la feature `bdm-firmware-backup-2026-11-005`. Sources : dépôt [essensys-bdm-programmer](https://github.com/essensys-hub/essensys-bdm-programmer), commande `bdm-backup` et dossier `firmware/pico/`.

!!! danger "Sur une carte de banc uniquement"
    Contrairement à l'[espion I2C](espion-i2c.md), cet outil **pilote le processeur** : il le remet à zéro, l'arrête pendant la lecture, puis le relance. Le BP ne fait rien d'autre pendant ce temps (environ 18 minutes).

    - Jamais sur une armoire en service.
    - Carte posée sur table, alimentée par une alimentation de laboratoire.
    - Après la sauvegarde, couper et remettre l'alimentation du BP si son redémarrage n'est pas certain.

## Ce que contient la sauvegarde

La flash interne fait 512 Ko (`0x00000` à `0x7FFFF`) :

| Zone | Adresses | Contenu |
|---|---|---|
| Bootloader | `0x00000` - `0x02FFF` | identique dans toutes les versions archivées |
| Champ de sécurité CFM | `0x00400` - `0x00417` | `0x00` partout, comme dans les images officielles |
| En-tête de l'application | `0x03000` - `0x03009` | CRC, version, saut vers l'application |
| Application | `0x03000` - `0x7DFFF` | le firmware (version 37 = 099-37) |
| `Tb_Echange` | `0x7E000` - `0x7EFFF` | réglages propres à la carte |
| Réserve | `0x7F000` - `0x7FFFF` | vierge |

!!! warning "Données de la carte"
    La zone `Tb_Echange` contient les réglages de l'installation. Une sauvegarde ne doit **jamais** être versionnée dans un dépôt : l'outil refuse d'écrire dans un dossier suivi par Git, et range les fichiers par défaut dans `~/essensys-backups`.

La sauvegarde ne couvre pas la flash SPI externe (OTA) ni l'EEPROM SPI (adresse MAC, clé serveur, code d'alarme).

## Matériel

- Un Raspberry Pi Pico (RP2040) sous MicroPython 1.24 ou plus récent, et son câble USB.
- Une breadboard et des fils Dupont femelle vers le connecteur J33 (barrette mâle 2 × 5, pas de 2,54 mm).
- Facultatif mais très utile : un analyseur logique 8 voies 24 MHz (puce FX2, compatible sigrok) pour voir les signaux.
- Une alimentation de laboratoire pour le BP.

Le jumper **JC1** doit être monté : il met J33 en mode BDM. Sans lui, J33 est en mode JTAG.

## Câblage J33 vers Pico

| J33 | Signal | Sur la carte | Pico | Broche physique |
|---|---|---|---|---|
| 1 | TCLK | — | non relié | — |
| 2 | BKPT | tirage 10 kΩ (R104) | GP5 | 7 |
| 3 | DSO | tirage 10 kΩ (R103) | GP4 | 6 |
| 4 | DSI | R188 non montée | GP3 | 5 |
| 5 | ALLPST | — | GP7 | 10 |
| 6 | DSCLK | tirage 10 kΩ (R105) | GP2 | 4 |
| 7 | +3V3S | lecture seule | **GP26** | **31** |
| 8 | RESET | tirage 10 kΩ (R106) | GP6 | 9 |
| 9 et 10 | GND | — | GND | 3 et 8 |

!!! tip "Pièges rencontrés"
    - **Le +3V3S va sur GP26** (entrée analogique), pas sur GP8 comme l'indiquait l'ancien guide : l'outil mesure la tension et refuse d'agir hors de 3,0 à 3,6 V.
    - **Les broches 10 et 11 du Pico sont voisines** : il est facile de déplacer ALLPST au lieu du +3V3S.
    - **Un Pico en mode BOOTSEL tire RESET vers la masse** et bloque le BP. Si le Mac voit un volume `RPI-RP2`, réinstaller MicroPython avant tout essai.

## Câblage de l'analyseur logique

Les pinces se posent côté J33, en parallèle des fils du Pico. Ne pas brancher la broche **PWR** de l'analyseur.

| Analyseur | sigrok | J33 | Signal |
|---|---|---|---|
| CH1 | D0 | 6 | DSCLK |
| CH2 | D1 | 4 | DSI |
| CH3 | D2 | 3 | DSO |
| CH4 | D3 | 5 | ALLPST |
| CH5 | D4 | 2 | BKPT |
| CH6 | D5 | 8 | RESET |
| CH7 | D6 | 1 | TCLK (horloge du processeur en mode BDM) |
| CH8 | D7 | 7 | +3V3S |
| GND | — | 9 | GND |

## Procédure

1. BP hors tension : poser le câblage, vérifier JC1.
2. Copier l'agent sur le Pico (une seule fois) :

    ```bash
    uvx mpremote connect /dev/cu.usbmodemXXXX cp firmware/pico/bdm_protocol.py firmware/pico/bdm_agent.py :
    ```

3. Alimenter le BP, puis lancer la sauvegarde :

    ```bash
    bdm-backup --port /dev/cu.usbmodemXXXX --serial <nom-de-la-carte>
    ```

4. L'outil vérifie le +3V3S, arrête le processeur, lit le registre CSR, lit deux fois les 512 Ko et compare les SHA-256, puis relance le processeur.
5. Il écrit quatre fichiers : `.bin` (image brute), `.s19` (Motorola S-record), `.sha256` et `.json` (CRC, version, CSR, zone CFM).
6. Copier la sauvegarde hors de l'ordinateur (support chiffré).

## Vérifier une sauvegarde

- Le CRC-16 (MODBUS) recalculé sur `0x3002` - `0x7DFFF` doit être égal au CRC stocké en `0x3000`.
- La version en `0x3002` doit correspondre au firmware attendu (`0x0025` pour 099-37).
- Pour un firmware archivé, comparer avec l'image `…elf_BOOT_CRC.S19` du dépôt `essensys-board-SC944D` : bootloader, CFM et application doivent être identiques à l'octet près.

## Résultats du 11 novembre 2026

Premier essai sur une carte de banc en firmware 099-37 :

- lien BDM établi à 25 kHz, CSR `0x01900000` ;
- deux lectures de 512 Ko identiques, en 17 min 45 s ;
- CRC recalculé `0x438D`, égal au CRC stocké ;
- **identique à l'octet près** à l'image archivée `099-37 …elf_BOOT_CRC.S19` (bootloader, CFM, application) ;
- 1 743 octets non vierges entre `0x2000` et `0x2FFF`, absents des images archivées : origine encore inconnue.

Les premiers essais BDM ont échoué (DSO toujours à 0) tant que le Pico était dans un état incohérent. Après réinstallation de MicroPython, le lien a fonctionné du premier coup, ce que l'analyseur logique a confirmé.

## Limites connues

- Après la relance (commande GO), ALLPST reste haut : le redémarrage du BP n'est pas confirmé par l'outil.
- L'identification du processeur se limite à un registre CSR plausible.
- Pas d'affichage de la progression pendant la sauvegarde.
