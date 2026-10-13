# Espion I2C passif

Le boîtier principal (BP, carte SC944D) commande les trois boîtiers auxiliaires (BA) par un **bus I2C** interne à l'armoire :

| Adresse | BA | Carte |
|---|---|---|
| `0x11` | pièces de vie | SC940D |
| `0x12` | chambres | SC942C |
| `0x13` | pièces d'eau | SC941C |

Quand une commande n'aboutit pas, la gateway ne peut pas dire pourquoi. Le BP acquitte l'action auprès de la gateway **avant** de l'envoyer au BA. Il l'abandonne ensuite sans prévenir si le BA ne répond pas.

L'espion I2C écoute ce bus **sans jamais y émettre**. Il distingue :

- un BA **absent** : il ne répond pas à son adresse ;
- une trame **rejetée** par le BA : CRC faux ;
- une ligne SDA ou SCL **bloquée** ;
- une commande **abandonnée** par le BP après plusieurs essais ;
- une commande **jamais émise**.

C'est l'outil qui a permis de comprendre une panne survenue après un remplacement de BP. La gateway voyait le BP et ses actions étaient acquittées, mais seul le BA pièces de vie répondait encore.

Sources, schémas et décodeur : dépôt [essensys-i2c-ba-sniffer](https://github.com/essensys-hub/essensys-i2c-ba-sniffer).

## Principe

<iframe src="../archify/espion-i2c.html?embed=1&amp;theme=light" title="Schéma d'architecture interactif : l'armoire, la sonde passive, l'analyseur, sigrok, le décodeur et la corrélation avec les journaux de la gateway" loading="lazy" style="width:100%;aspect-ratio:2048/1320;height:auto;border:0"></iframe>

[Ouvrir le diagramme en plein écran](archify/espion-i2c.html){ target="_blank" rel="noopener" }.

??? info "Image fixe du diagramme"
    ![Capture du schéma d'architecture. Dans le cadre « Armoire, 0 V TBTS jamais relié au PE », le BP SC944D envoie trames et réponses sur le bus I2C 50 kHz, relié aux BA 0x11 (ACK), 0x12 et 0x13 (NACK ?). Du bus part une liaison « écoute seule, 3 fils » vers la sonde passive, reliée à l'analyseur FX2. Dans le cadre « Hôte sur batterie, Wi-Fi seulement », l'analyseur envoie son flux brut à sigrok-cli et au décodeur essensys-i2c-sniff ; sigrok transmet ses annotations au décodeur, qui produit la capture. En bas, la gateway CM5 produit les journaux du backend ; leur export et la capture alimentent le rapport de corrélation.](archify/espion-i2c.png){ loading=lazy }

1. **La sonde** (3 fils : SDA, SCL, 0 V) relève les signaux du bus à travers des résistances et un tampon. Elle ne peut rien y injecter.
2. **L'analyseur logique** échantillonne SDA et SCL à 1 MHz au moins, soit 20 fois le débit du bus.
3. **sigrok** décode le protocole I2C : adresses, octets, ACK et NACK. Le décodeur Python lit le même flux pour repérer les lignes bloquées.
4. **Le décodeur Essensys** reconstitue chaque échange : code de trame, longueur, CRC-16, réponse du BA, lampes, volets et variateurs visés.
5. **La corrélation** rapproche les actions vues dans les journaux de la gateway (`Sending Actions`, `Action acknowledged`) des trames réellement observées sur le bus.

## Ce qu'il vous faut

| Élément | Remarque |
|---|---|
| Analyseur logique USB 8 voies à puce Cypress FX2 (CY7C68013A) | Clone « 24 MHz 8CH » pris en charge par le pilote sigrok `fx2lafw` |
| Raspberry Pi (3 ou plus récent) | Raspberry Pi OS. Ou un portable, à condition qu'il soit **sur batterie** |
| Batterie USB | Pour alimenter le Pi pendant la capture |
| Sonde passive à fabriquer | Voir ci-dessous : moins de 10 € de composants |
| Câble avec boîtier WR-MPC3 2×2 (Micro-Fit 3.0) | 3 contacts sertis seulement, côté BA |

## Sécurité

!!! danger "À lire avant tout branchement"
    - **Hors tension.** Le coffret contient du 230 V. Le branchement et le débranchement de la sonde se font **hors tension**, par une **personne habilitée** (NF C 18-510).
    - **Trois fils seulement : SDA, SCL, 0 V.** La broche 4 du connecteur des BA porte le **+15 V** : la sonde n'a pas de contact à cette position. Ne la raccordez jamais.
    - **Aucun pont de masse.** Le 0 V de l'armoire n'est jamais relié au PE. L'analyseur et le Pi doivent rester **isolés** pendant la capture : Pi sur batterie, en **Wi-Fi seulement**, sans câble Ethernet ni chargeur secteur, ou isolateur USB d'au moins 2,5 kV. Un hôte relié à la terre créerait exactement le chemin de courant décrit dans le [retour d'expérience foudre](../retex/foudre-2026/synthese.md).
    - **L'outil est strictement passif.** Il n'émet rien sur le bus et ne pilote pas l'armoire. Les commandes d'essai sont envoyées **par l'exploitant**, depuis l'interface habituelle.

## Fabriquer la sonde

La sonde tient sur une petite **plaque à pastilles**. Le tampon U1 (boîtier SC-70) et la protection D1 (SOT-23) se soudent sur des adaptateurs vers DIP et SIP.

![Schéma KiCad de la sonde : J1 vers le BA (contacts 1 SDA, 2 SCL, 3 0 V, position 4 vide), R1 et R2 de 1 kΩ en série, R3 et R4 de 1 MΩ vers le 0 V, protection D1 SP0502BAHT, tampon U1 74LVC2G17 alimenté en 3,3 V et découplé par C1, sorties SCL_OUT et SDA_OUT vers J2 et l'analyseur.](img/sonde-schema-kicad.png){ loading=lazy }

| Repère | Valeur | Rôle |
|---|---|---|
| J1 | Boîtier WR-MPC3 2×2, contacts 1, 2, 3 | Câble vers le connecteur J1 ou J2 du BA. **Position 4 vide** |
| R1, R2 | 1 kΩ | Résistances série : limitent le courant en cas d'erreur |
| R3, R4 | 1 MΩ | Rappel au 0 V quand la sonde est débranchée (5 µA sous 5 V) |
| D1 | SP0502BAHT | Protection contre les décharges électrostatiques, 5,5 V |
| U1 | 74LVC2G17 | Tampon : accepte 5,5 V en entrée sous 3,3 V d'alimentation |
| C1 | 100 nF | Découplage de U1 |
| J2 | Barrette 1×4 | 1 GND, 2 voie D0 (SCL), 3 voie D1 (SDA), 4 +3,3 V |

Le +3,3 V de U1 vient de l'analyseur s'il le fournit, sinon de la broche 1 du connecteur GPIO du Raspberry Pi. La sonde ne prend **ni pull-up ni alimentation** sur le bus.

![Câblage Fritzing : connecteur du BA à gauche, puis les résistances, D1, U1 et C1 sur la plaque, la barrette J2, l'analyseur FX2 (CH0 = SCL, CH1 = SDA, GND) et le Raspberry Pi sur batterie, dont la broche 1 fournit le 3,3 V. Les notes rappellent que la position 4 (+15 V) reste vide et que le Pi doit être sur batterie, en Wi-Fi seulement.](img/sonde-cablage-fritzing.png){ loading=lazy }

**Contrôles avant la première utilisation :**

1. À l'ohmmètre, **aucune continuité** entre la position 4 du boîtier J1 et un fil de la sonde.
2. Entre J1-1 et J1-3, puis entre J1-2 et J1-3 : environ **1 MΩ** (R1 + R3, puis R2 + R4). Une valeur très faible signale un court-circuit à corriger.
3. Sonde alimentée en 3,3 V et non raccordée : D0 et D1 au niveau bas (rappel par R3 et R4).

Les sources (KiCad, Fritzing, nomenclature) sont dans le dossier [`hardware/`](https://github.com/essensys-hub/essensys-i2c-ba-sniffer/tree/main/hardware) du dépôt.

## Installer le logiciel

Sur le Raspberry Pi :

```bash
sudo apt install sigrok-cli sigrok-firmware-fx2lafw python3-pip
pip install git+https://github.com/essensys-hub/essensys-i2c-ba-sniffer
```

Analyseur branché en USB, vérifiez qu'il est reconnu :

```bash
sigrok-cli --scan
essensys-i2c-sniff --version
```

## Mode opératoire

1. **Préparer l'hôte.** Pi sur batterie, Wi-Fi connecté, aucun câble Ethernet ni chargeur. Analyseur en USB sur le Pi, sonde reliée à l'analyseur (D0 = SCL, D1 = SDA, GND).
2. **Raccorder la sonde, armoire hors tension** (personne habilitée). Brancher J1 de la sonde sur le connecteur **libre** du BA en bout de chaîne. Remettre sous tension.
3. **Lancer la capture**, en gardant aussi le flux brut pour pouvoir le rejouer :

    ```bash
    essensys-i2c-sniff live --raw-out capture.bin
    ```

4. **Envoyer une commande d'essai vers chaque BA**, une à la fois, depuis l'interface habituelle : une lampe des pièces de vie, une des chambres, une des pièces d'eau. Notez l'heure.

    !!! note "Un seul essai par clic"
        Le BP n'envoie un ordre à un BA que quand une valeur change. Il le répète une vingtaine de fois en cas d'échec, puis l'abandonne. Sur un BA déjà en défaut, chaque nouveau clic ne déclenche plus qu'**une seule** tentative. Cliquez une fois, puis lisez la capture.

5. **Arrêter la capture** avec Ctrl+C. Pour la rejouer en NDJSON :

    ```bash
    essensys-i2c-sniff replay capture.bin --format ndjson > capture.ndjson
    ```

6. **Corréler avec la gateway.** Exportez les journaux du backend depuis la gateway, en lecture seule, puis rapprochez-les de la capture :

    ```bash
    ssh <gateway> 'docker logs --since 30m essensys-backend' > backend.log
    essensys-i2c-sniff correlate --capture capture.ndjson --backend-log backend.log
    ```

7. **Débrancher la sonde, armoire hors tension.**

## Lire une capture

Exemple sur le cas réel qui a motivé l'outil : le BA pièces de vie répond, les deux autres sont muets.

```text
session replay:capture.bin — 1000000 Hz — essensys-i2c-sniff 0.1.0 (lecture seule)
       1.005 ms  0x11 pièces de vie — FORCAGE_SORTIES — lampe 0 → ON (commande observée) — trame reçue et validée CRC par le BA
     104.295 ms  0x12 chambres — NACK d'adresse — BA absent (n° 1)
     204.505 ms  0x13 pièces d'eau — NACK d'adresse — BA absent (n° 1)
```

| Ce que vous voyez | Diagnostic | Action suivante |
|---|---|---|
| `trame reçue et validée CRC par le BA` | Le BA a reçu l'ordre intact | Si rien ne bouge : sortie, câblage du bornier, relais ou configuration (mode du variateur, temps du volet) |
| `NACK d'adresse — BA absent` | Le BA ne répond pas à son adresse : non alimenté, processeur arrêté, étage I2C détruit, ou mauvais firmware (adresse différente) | Voyant ÉTAT du BA, +15 V à son bornier, puis [remise en service après surtension](../install/remise-en-service-surtension.md) |
| `rejet côté BA : écho CRC 0x0000` | Le BA a reçu une trame corrompue et l'a rejetée | Parasites ou niveaux dégradés sur le bus : mesurer à l'oscilloscope |
| `SDA (ou SCL) bloquée au niveau bas` | Une carte maintient la ligne basse | Isoler les BA un à un, hors tension |
| `[répétition n]` puis `commande probablement abandonnée` | Le BP a épuisé ses essais | Comme un BA absent |
| Aucune trame vers le BA après votre clic | Le BP n'a rien envoyé : la valeur n'a pas changé, ou ses essais sont déjà épuisés | Vérifier la commande côté gateway, puis cliquer sur une autre sortie |

Exemples de défauts :

```text
       1.005 ms  0x11 pièces de vie — FORCAGE_SORTIES — lampe 0 → ON (commande observée) — rejet côté BA : écho CRC 0x0000 : le BA a rejeté le CRC
               ⚠ CRC de requête invalide (attendu 0xA017, reçu 0xA0E8) : le BA rejettera la trame
       1.005 ms  0x13 pièces d'eau — NACK d'adresse — BA absent (n° 1)
     101.215 ms  0x13 pièces d'eau — NACK d'adresse — BA absent (n° 2) — [répétition 1]
     201.425 ms  0x13 pièces d'eau — NACK d'adresse — BA absent (n° 3) — [répétition 2]
    2201.425 ms  0x13 — ⚠ commande probablement abandonnée par le maître, jamais reçue par le BA (3 tentative(s))
```

!!! warning "Ce que l'outil ne prouve pas"
    Une trame « validée CRC » prouve que le BA a **reçu** l'ordre. Elle ne prouve pas que la lampe s'est allumée : le protocole ne renvoie jamais l'état physique des sorties. De même, « Action acknowledged » dans les journaux de la gateway veut seulement dire que le **BP** a reçu l'action.

## Corrélation avec la gateway

```text
décalage d'horloge retenu : +0.0 s (automatique)
2026-10-13 11:22:01  action …0001 → 0x11 : transmise au BA (trame validée CRC ; la commutation physique n'est pas prouvée)
2026-10-13 11:22:01  action …0002 → 0x12 : acquittée par le BP, non reçue par le BA (NACK d'adresse)
2026-10-13 11:22:01  action …0003 → 0x13 : acquittée par le BP, non reçue par le BA (NACK d'adresse)
```

L'outil déduit le BA visé des index de la table d'échange : scénario 605 à 622, configuration 494 à 589.

Le décalage d'horloge entre le Pi et la gateway est estimé automatiquement. Vous pouvez aussi le fixer avec `--offset`. L'outil ne se connecte jamais à la gateway : il lit le fichier exporté.

## Limites

- **Pas de mesure électrique.** Un analyseur logique ne voit ni les niveaux de tension, ni les temps de montée, ni les parasites brefs : il faut un oscilloscope.
- **Pas de surveillance permanente.** C'est un outil d'intervention ponctuelle. La surveillance permanente du bus est le rôle du [module ESP32 de la carte N2](../install/module-n2-esp32.md).
- **État inféré.** L'option `--state` reconstruit l'état **commandé** depuis le début de la capture. Les sorties jamais commandées restent « inconnues ».
- **Ordre des bits de la trame ACTIONS** : il reste à confirmer sur une capture réelle.

## Références

- Dépôt [essensys-i2c-ba-sniffer](https://github.com/essensys-hub/essensys-i2c-ba-sniffer) : décodeur, corpus de captures de référence, schémas KiCad et Fritzing.
- Feature `i2c-ba-sniffer-2026-10-009`, ticket [essensys-hub/essensys-feature-lifecycle#29](https://github.com/essensys-hub/essensys-feature-lifecycle/issues/29).
- [Ajouter ou remplacer un BP](../install/ajout-bp.md) · [Remise en service après surtension](../install/remise-en-service-surtension.md) · [Table d'échange](../architecture/exchange-table.md).
