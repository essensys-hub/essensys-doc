# Errata — Indices Absolus des Parametres de Scenario (+8) et Temps d'Action des Volets

**Statut** : Corrections appliquees  
**Date** : 2026-06-11  
**Fichiers corriges** : `archi/exchange-table.md`, `archi/domaines-fonctionnels.md`

---

## Constat 1 — Decalage de +8 sur les indices absolus du Scenario 1

La documentation utilisait une base **600** pour les indices absolus des parametres du Scenario 1, alors que l'enum `Tbb_Donnees_Index` du firmware place `Scenario1` a l'indice **592**. Tous les indices absolus de la section 4 d'`exchange-table.md` (et les exemples JSON de `domaines-fonctionnels.md`) etaient donc decales de **+8**.

### Verification croisee (3 sources independantes)

| Parametre | Doc (avant) | Reel | Confirme par |
|-----------|-------------|------|--------------|
| `Scenario_Alarme_ON` | 601 | **593** | MCP_DEVICE_INDEX_REFERENCE.md (backend) |
| `Allumer_CHB_LSB` | 621 | **613** | Exemple MCP "chevet petite chambre 3" (k=613, v=64) |
| `OuvrirVolets_PDV` | 625 | **617** | table_reference.json (Home Assistant) + backend |
| `FermerVolets_PDE` | 630 | **622** | table_reference.json (Home Assistant) |
| `Scenario_Securite` | 631 | **623** | MCP_DEVICE_INDEX_REFERENCE.md |
| `Scenario_Machines` | 632 | **624** | MCP_DEVICE_INDEX_REFERENCE.md |

Le "bloc complet 605-622" documente en section 6 etait, lui, correct — il correspond aux offsets 13-30 de `enumScenario` (Eteindre 605-610, Allumer 611-616, Volets 617-622). C'est la section 4 qui etait incoherente avec lui.

### Mapping corrige (base 592)

| Offset | Indices abs | Parametres |
|--------|-------------|------------|
| 0 | 592 | Confirme_Scenario |
| 1 | 593 | Alarme_ON |
| 2-12 | 594-604 | AlarmeConfig (11) |
| 13-18 | 605-610 | Eteindre lumieres (PDV/CHB/PDE, LSB/MSB) |
| 19-24 | 611-616 | Allumer lumieres |
| 25-27 | 617-619 | Ouvrir volets (PDV/CHB/PDE) |
| 28-30 | 620-622 | Fermer volets |
| 31-32 | 623-624 | Securite prises / Machines |
| 33-36 | 625-628 | Chauffage (zj/zn/zsb1/zsb2) |
| 37 | 629 | Cumulus |
| 38-40 | 630-632 | Reveil reglage / Reveil ON / Efface |

Scenario2 commence a 633 (= 592 + 41), coherent avec la section 3.15.

---

## Constat 2 — Temps d'action des volets non detailles

La section 3.14 d'`exchange-table.md` donnait des plages approximatives (`~566-573`...) sans le mapping par volet ni la semantique. Ajouts :

- Indices exacts confirmes : `Volets_PDV_Temps` 566-573, `Volets_CHB_Temps` 574-581, `Volets_PDE_Temps` 582-589 (droits `RWS`)
- Tableau indice par volet (566=salon 1 ... 585=store terrasse)
- Semantique : **un seul temps par volet** (1-255 s) pour les deux sens = duree de maintien du relais, decompte par la BA (`uc_StopVolet()`)
- Valeur 0 = defaut firmware BA : 120 s (volet), 255 s (store)
- Propagation BP → BA par I2C sur changement, persistance Flash (BP) + EEPROM 0x002A+n (BA)
- Reglage direct par le serveur (`{"k": 566, "v": "25"}`), sans bloc complet scenario

---

## Sources

- Firmware BP : `essensys-board-SC944D/SC944D/Prog/099-37/BP_MQX_ETH/H/TableEchange.h` (enums `Tbb_Donnees_Index`, `enumScenario`), `C/ba.c`
- Firmware BA : `essensys-gcc/ba/source/traitement.c`, `slavenode.c`, `constantes.h`, `main.c` (mapping EEPROM)
- Backend : `essensys-server-backend/docs/MCP_DEVICE_INDEX_REFERENCE.md`
- Home Assistant : `essensys-homeassitant/custom_components/essensys/table_reference.json`
