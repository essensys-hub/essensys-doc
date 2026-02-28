# BP_MQX_ETH v2 — Firmware Local + Status Reel

**Statut** : Proposition  
**Auteur** : Essensys  
**Date** : 2026-01-21

## 1. Contexte et Problemes

Le firmware actuel (v37) du BP_MQX_ETH presente deux limitations majeures :

### 1.1 Resolution DNS via WAN

Le firmware resout `mon.essensys.fr` via un DNS public, alors que le serveur Go tourne sur un Raspberry Pi **sur le meme LAN**. Cela cree :

- Une dependance a la connectivite Internet
- Un point de defaillance externe (DNS public, route WAN)
- Une latence inutile (resolution DNS + routage externe)
- Un risque de panne complete si la box Internet tombe

```
Actuel (v37) :
BP_MQX_ETH → DNS public → mon.essensys.fr → IP WAN → NAT → Raspberry Pi (LAN)

Propose (v2) :
BP_MQX_ETH → AdGuard (LAN :53) → mon.essensys.local → Raspberry Pi (LAN direct)
```

### 1.2 Status Partiel de la Table d'Echange

Le serveur ne connait qu'un **sous-ensemble** de la table d'echange (~600 indices) :

| Etape | Limitation |
|-------|------------|
| `GET /api/serverinfos` | Le serveur demande au max **30 indices** (`uc_NB_MAX_INFOS_DEMANDEES_PAR_SERVEUR = 30`) |
| `POST /api/mystatus` | Le BP ne renvoie **que les indices demandes** |
| Actions (`/api/myactions`) | Le serveur envoie des ordres mais **ne recoit jamais de confirmation d'execution physique** |

Consequences :
- Le dashboard affiche l'**intention** (action envoyee) et non l'**etat reel** (relais physiquement active)
- Impossible de savoir si un volet est reellement en position
- Impossible de detecter un dysfonctionnement materiel (relais colle, BA deconnecte)
- La `TableReference.json` du support site ne reflete pas l'etat reel des objets

### 1.3 Pas de Retour d'Etat des Boitiers Auxiliaires (BA)

Le protocole I2C actuel entre le BP et les BA est **unidirectionnel en termes d'etat** :

| Commande I2C | Code | Direction | Contenu |
|--------------|------|-----------|---------|
| `C_FORCAGE_SORTIES` | 1 | BP → BA | Ordres lampes, variateurs, volets |
| `C_CONF_SORTIES` | 2 | BP → BA | Configuration TOR/gradateur |
| `C_TPS_EXTINCTION` | 3 | BP → BA | Temps d'extinction lampes |
| `C_TPS_ACTION` | 4 | BP → BA | Temps d'action volets |
| `C_ACTIONS` | 5 | BP → BA | Sauvegarde, blocage, allumage force |

La reponse I2C du BA ne contient que le **code de trame echo + CRC**, pas l'etat physique des sorties.

## 2. Proposition d'Architecture

### 2.1 Changement DNS : `mon.essensys.fr` → `mon.essensys.local`

#### Modification Firmware (SC944D)

**Fichier** : `Ethernet/www.h`

```c
// Avant (v37)
#define NOM_SERVEUR_ESSENSYS  "mon.essensys.fr"

// Apres (v2)
#define NOM_SERVEUR_ESSENSYS  "mon.essensys.local"
```

**Fichier** : `Ethernet/www.c`

```c
// Avant (v37)
char * c_EnteteTrameHost(void) {
    return "host: mon.essensys.fr\r\n";
}

// Apres (v2)
char * c_EnteteTrameHost(void) {
    return "host: mon.essensys.local\r\n";
}
```

#### Configuration AdGuard (cote serveur)

Ajouter un enregistrement DNS dans AdGuard Home pour que `mon.essensys.local` pointe vers le Raspberry Pi :

```yaml
# AdGuard DNS Rewrite
domain: mon.essensys.local
answer: 192.168.0.XXX  # IP du Raspberry Pi
```

#### Configuration DHCP

Configurer le DHCP de la box/routeur pour que le BP obtienne **AdGuard comme serveur DNS** :
- DNS primaire : IP du Raspberry Pi (AdGuard :53)
- DNS secondaire : aucun (forcer le passage par AdGuard)

Alternative : configurer une IP DNS fixe dans le firmware si le DHCP de la box ne peut pas etre modifie.

#### Impact sur les Autres Composants

| Composant | Impact | Action |
|-----------|--------|--------|
| Backend Go | Aucun | Le backend ecoute sur :80, independant du nom DNS |
| Nginx | Ajouter `server_name mon.essensys.local` | Configuration Nginx |
| Traefik | Aucun (WAN uniquement) | — |
| Frontend | Aucun | Le frontend utilise des URLs relatives |
| EEPROM | Aucun | La cle serveur reste dans EEPROM, independante du DNS |

### 2.2 Status Reel Complet — Strategie en 3 Niveaux

#### Niveau 1 : Envoyer Toute la Table d'Echange (modification BP)

Plutot que d'attendre la liste des indices du serveur, le BP envoie **toute la table modifiee** a chaque cycle.

**Approche par delta** : Ne transmettre que les indices qui ont change depuis le dernier `POST /api/mystatus` reussi.

```c
// Pseudo-code v2 — mystatus avec delta
for (us_i = 0; us_i < Nb_Tbb_Donnees; us_i++) {
    if (Tb_Echange[us_i] != Tb_EchangePrecedentEnvoye[us_i]) {
        // Ajouter {k: us_i, v: Tb_Echange[us_i]} au JSON
        uc_NbChangements++;
    }
}
// Apres envoi reussi (201 Created) :
memcpy(Tb_EchangePrecedentEnvoye, Tb_Echange, Nb_Tbb_Donnees);
```

**Contrainte memoire** : `Tb_EchangePrecedentEnvoye` = ~600 octets supplementaires en RAM. Faisable car le MCF52259 a de la marge sur les 3000 octets de stack Ethernet.

**Contrainte TCP single-packet** : Si trop de deltas, fractionner en plusieurs cycles de polling (max ~30 indices par trame pour rester dans un seul paquet TCP).

```
Cycle 1: POST /api/mystatus → indices 0-29 modifies
Cycle 2: POST /api/mystatus → indices 30-59 modifies
...
Cycle N: POST /api/mystatus → derniers indices modifies
```

**Compatibilite ascendante** : Le serveur continue de renvoyer la liste `infos` dans `/api/serverinfos`, mais le firmware v2 l'ignore et envoie les deltas a la place.

#### Niveau 2 : Nouveau Endpoint `/api/myfullstatus` (modification Backend Go)

Creer un nouvel endpoint pour recevoir le dump complet :

```
POST /api/myfullstatus HTTP/1.1
Content-type: application/json ;charset=UTF-8
Authorization: Basic <cle>

{"version":"V38","full":true,"ek":[{k:0,v:"37"},{k:1,v:"30"},...,{k:599,v:"0"}]}
```

Le backend Go stocke l'integralite dans Redis :

```
HSET essensys:client:{mac}:exchange:full {indice} {valeur}
```

Le frontend peut alors lire l'etat reel de **chaque** indice de la `TableReference.json`.

#### Niveau 3 : Retour d'Etat des Boitiers Auxiliaires (modification BA + BP)

Ajouter une **nouvelle commande I2C** aux firmwares BA (SC940, SC941C, SC942C) :

```c
// Nouveau code de trame (a ajouter dans slavenode.c)
enum enum_CODE_TRAMES {
    C_FORCAGE_SORTIES = 1,
    C_CONF_SORTIES,
    C_TPS_EXTINCTION,
    C_TPS_ACTION,
    C_ACTIONS,
    C_LIRE_ETAT = 6    // NOUVEAU : lecture etat physique
};
```

**Format de la reponse I2C pour `C_LIRE_ETAT`** :

```
┌──────────┬──────────┬──────────┬──────────┬──────────┬──────────┬──────────┐
│ Octet 0  │ Octet 1  │ Octet 2  │ Octet 3  │ Octet 4  │ Octet 5  │ Octet 6  │
│ Code (6) │ Lampes   │ Lampes   │ Volets   │ Volets   │ Varia-   │ Varia-   │
│          │ LSB      │ MSB      │ LSB      │ MSB      │ teurs    │ teurs    │
└──────────┴──────────┴──────────┴──────────┴──────────┴──────────┴──────────┘
  + CRC16 (2 octets)
```

**Implementation cote BA** (dans `slavenode.c`) :

```c
case C_LIRE_ETAT:
    RXByteCount = 1;  // Pas de donnees entrantes
    // Preparer la reponse avec l'etat reel
    TxBuf.b[0] = C_LIRE_ETAT;
    TxBuf.b[1] = (us_SortiesRelais & 0xFF);        // Lampes LSB
    TxBuf.b[2] = ((us_SortiesRelais >> 8) & 0xFF);  // Lampes MSB
    TxBuf.b[3] = (us_EtatVolets & 0xFF);            // Volets LSB
    TxBuf.b[4] = ((us_EtatVolets >> 8) & 0xFF);     // Volets MSB
    TxBuf.b[5] = st_Variateur[0].uc_ValeurCourante; // Variateur 1
    TxBuf.b[6] = st_Variateur[1].uc_ValeurCourante; // Variateur 2
    SensBufCount = 9;  // 7 data + 2 CRC
    break;
```

**Implementation cote BP** (dans `ba.c` ou `ba_i2c.c`) :

```c
// Interroger chaque BA toutes les N secondes
for (uc_BA = 0; uc_BA < 3; uc_BA++) {
    sl_fct_write_polled(I2C_BUS_ADDRESS_BA + uc_BA,
                        C_LIRE_ETAT, &reponse, &erreur);
    if (erreur == I2C_OK) {
        // Stocker dans la table d'echange aux indices dedies
        Tb_Echange[ETAT_REEL_BA_BASE + uc_BA * ETAT_REEL_BA_SIZE + 0] = reponse.lampes_lsb;
        Tb_Echange[ETAT_REEL_BA_BASE + uc_BA * ETAT_REEL_BA_SIZE + 1] = reponse.lampes_msb;
        // ...
    }
}
```

## 3. Cartographie des Cartes

### 3.1 SC944D — Boitier Principal (BP)

| Caracteristique | Valeur |
|-----------------|--------|
| MCU | Freescale MCF52259 (ColdFire V2, 32 bits, 80 MHz) |
| OS | MQX RTOS 4.0 |
| Memoire | 512 Ko Flash + RAM interne |
| Communication | Ethernet (RTCS), I2C maitre, UART ×3, SPI |
| Role | Coordinateur central, pont Ethernet ↔ I2C |
| Firmware actuel | v37 (`us_BP_VERSION_SERVEUR`) |
| Sources | `essensys-board-SC944D/SC944D/Prog/099-37/BP_MQX_ETH/` |

### 3.2 SC940D — Boitier Auxiliaire PDV (Pieces de Vie)

| Caracteristique | Valeur |
|-----------------|--------|
| MCU | PIC16F946 (8 bits, Microchip) |
| OS | Bare metal (super loop) |
| Communication | I2C esclave (adresse `0x11`) |
| Entrees TOR | 5 |
| Lampes | 5 (relais monostables) |
| Variateurs | 3 |
| Volets | 6 (12 relais bistables) |
| Sources | `essensys-board-SC940/SC940D/Prog/code_ba/source/` |

### 3.3 SC941C — Boitier Auxiliaire PDE (Pieces d'Eau)

| Caracteristique | Valeur |
|-----------------|--------|
| MCU | PIC16F946 (8 bits, Microchip) |
| OS | Bare metal (super loop) |
| Communication | I2C esclave (adresse `0x13`) |
| Entrees TOR | 13 |
| Lampes | 13 (relais monostables) |
| Variateurs | 1 |
| Volets | 4 (8 relais bistables) |
| Sources | `essensys-board-SC941C/SC941C/Prog/code_ba/source/` |

### 3.4 SC942C — Boitier Auxiliaire CHB (Chambres)

| Caracteristique | Valeur |
|-----------------|--------|
| MCU | PIC16F946 (8 bits, Microchip) |
| OS | Bare metal (super loop) |
| Communication | I2C esclave (adresse `0x12`) |
| Entrees TOR | 7 |
| Lampes | 7 (relais monostables) |
| Variateurs | 4 |
| Volets | 5 (10 relais bistables) |
| Sources | `essensys-board-SC942C/SC942C/Prog/code_ba/source/` |

### 3.5 Firmware BA Partage

Les 3 cartes BA partagent le **meme code source**. La difference est le type de boitier selectionne dans `hard.h` :

```c
// hard.h — Selection du type
#define TYPE_PIECES_DE_VIE   // SC940 → I2C 0x11
#define TYPE_CHAMBRES        // SC942 → I2C 0x12
#define TYPE_PIECES_D_EAU    // SC941 → I2C 0x13
```

Le protocole I2C, les commandes et la logique applicative (variateurs, volets, anti-rebond) sont identiques.

## 4. Plan de Migration

### Phase 1 : DNS Local (risque minimal)

| Etape | Composant | Modification |
|-------|-----------|-------------|
| 1.1 | AdGuard | Ajouter `mon.essensys.local → IP Raspberry Pi` |
| 1.2 | Nginx | Ajouter `server_name mon.essensys.local` |
| 1.3 | Firmware BP | Changer `NOM_SERVEUR_ESSENSYS` + `c_EnteteTrameHost()` |
| 1.4 | DHCP | Configurer DNS = IP AdGuard |
| 1.5 | Test | Valider le polling HTTP en LAN direct |

**Rollback** : Remettre `mon.essensys.fr` dans le firmware (flash JTAG).

### Phase 2 : Status Complet via Delta (firmware BP uniquement)

| Etape | Composant | Modification |
|-------|-----------|-------------|
| 2.1 | Firmware BP | Ajouter `Tb_EchangePrecedentEnvoye[]` + logique delta |
| 2.2 | Firmware BP | Modifier `sc_JsonPostServerInformation()` pour envoyer les deltas |
| 2.3 | Backend Go | Ajouter endpoint `POST /api/myfullstatus` |
| 2.4 | Backend Go | Stocker le full status dans Redis |
| 2.5 | Frontend | Afficher l'etat reel depuis Redis via API |
| 2.6 | TableReference | Enrichir avec mapping indice → objet physique |

### Phase 3 : Retour d'Etat des BA (firmware BA + BP)

| Etape | Composant | Modification |
|-------|-----------|-------------|
| 3.1 | Firmware BA | Ajouter `C_LIRE_ETAT` dans `slavenode.c` (SC940, SC941C, SC942C) |
| 3.2 | Firmware BP | Ajouter interrogation cyclique des BA |
| 3.3 | Firmware BP | Stocker les reponses dans `Tb_Echange[]` (indices dedies) |
| 3.4 | Backend Go | Exposer les indices d'etat reel dans l'API |
| 3.5 | Frontend | Afficher etat physique confirme vs. etat commande |

**Attention** : La Phase 3 necessite un acces physique aux 3 cartes BA pour flasher le nouveau firmware PIC16F946 via programmeur ICSP (Microchip).

## 5. Impact sur la TableReference

### Nouveaux Indices Proposes

| Plage | Contenu | Description |
|-------|---------|-------------|
| 600-609 | Etat reel BA PDV (0x11) | Lampes, volets, variateurs confirmes |
| 610-619 | Etat reel BA CHB (0x12) | Lampes, volets, variateurs confirmes |
| 620-629 | Etat reel BA PDE (0x13) | Lampes, volets, variateurs confirmes |
| 630 | Etat connectivite BA | Bitmask: bit 0=PDV OK, bit 1=CHB OK, bit 2=PDE OK |

### Distinction Action vs. Etat

| Concept | Exemple | Indice actuel | Indice etat reel |
|---------|---------|---------------|------------------|
| Lampe salon commandee | "Allumer salon" | 619 (bit = 1) | 600 (bit = 1 si relais ON) |
| Volet chambre commande | "Ouvrir volet CH1" | Scenario | 612 (position confirmee) |
| Variateur cuisine | "Gradateur 75%" | 494+ | 620 (valeur courante) |

Cela permet au frontend d'afficher :
- **Etat commande** : ce que l'utilisateur a demande
- **Etat reel** : ce que le materiel confirme
- **Ecart** : alerte si commande ≠ reel (materiel defaillant)

## 6. Diagramme de Flux (v2)

```mermaid
sequenceDiagram
    participant BA as Boitiers Auxiliaires<br/>(PIC16F946)
    participant BP as BP_MQX_ETH<br/>(MCF52259)
    participant AG as AdGuard DNS<br/>(Raspberry Pi)
    participant BE as Backend Go<br/>(Raspberry Pi)
    participant R as Redis
    participant FE as Frontend React

    Note over BP: Boot — Init MQX RTOS

    BP->>AG: DNS mon.essensys.local
    AG-->>BP: 192.168.0.XXX (LAN direct)

    BP->>BE: GET /api/serverinfos
    BE-->>BP: 200 OK

    loop Toutes les 2 secondes
        BP->>BA: I2C C_LIRE_ETAT (code 6)
        BA-->>BP: Lampes + Volets + Variateurs (etat reel)
        BP->>BP: Stocker etat reel dans Tb_Echange[600+]

        BP->>BP: Calculer delta vs precedent envoi
        BP->>BE: POST /api/myfullstatus (delta)
        BE->>R: HSET essensys:client:{mac}:exchange:full
        BE-->>BP: 201 Created

        BP->>BE: GET /api/myactions
        BE-->>BP: Actions a executer

        opt Actions recues
            BP->>BA: I2C C_FORCAGE_SORTIES
            BP->>BE: POST /api/done/{guid}
        end
    end

    FE->>BE: GET /api/status/full
    BE->>R: HGETALL essensys:client:{mac}:exchange:full
    BE-->>FE: Etat reel complet
    Note over FE: Affiche etat reel<br/>+ detection ecarts
```

## 7. Risques et Mitigations

| Risque | Probabilite | Impact | Mitigation |
|--------|-------------|--------|------------|
| Flash firmware BA echoue | Faible | Eleve | Tester sur un BA avant deploiement generalise |
| Trame I2C trop longue | Faible | Moyen | Limiter la reponse `C_LIRE_ETAT` a 9 octets (7 data + 2 CRC) |
| Delta trop volumineux pour single-packet | Moyenne | Moyen | Fractionner en cycles de 30 indices max |
| `mon.essensys.local` non resolu | Faible | Eleve | Configurer AdGuard + fallback IP fixe dans firmware |
| Memoire insuffisante MCF52259 | Faible | Eleve | `Tb_EchangePrecedentEnvoye` = +600 octets, stack Ethernet a 3000 |
| Incompatibilite backend ancien | Nulle | — | Nouvel endpoint `/api/myfullstatus`, l'ancien reste fonctionnel |

## 8. Prerequis

| Prerequis | Disponibilite |
|-----------|---------------|
| Programmeur JTAG/BDM (P&E Micro) | Pour flasher le BP (MCF52259) |
| Programmeur ICSP (PICkit 3/4) | Pour flasher les 3 BA (PIC16F946) |
| CodeWarrior pour Coldfire | Compilation BP |
| MPLAB X + XC8 | Compilation BA |
| Acces physique aux 4 cartes | Deploiement firmware |
| AdGuard configure | Resolution DNS locale |

## References Sources

| Composant | Chemin |
|-----------|--------|
| BP firmware | `essensys-board-SC944D/SC944D/Prog/099-37/BP_MQX_ETH/` |
| BP legacy | `client-essensys-legacy/` (C/, H/, Ethernet/) |
| BA PDV (SC940) | `essensys-board-SC940/SC940D/Prog/code_ba/source/` |
| BA PDE (SC941C) | `essensys-board-SC941C/SC941C/Prog/code_ba/source/` |
| BA CHB (SC942C) | `essensys-board-SC942C/SC942C/Prog/code_ba/source/` |
| DNS serveur | `mon.essensys.fr` → `www.h` ligne 41 |
| Host header | `mon.essensys.fr` → `www.c` `c_EnteteTrameHost()` |
| Table d'echange | `H/TableEchange.h` → `enum Tbb_Donnees_Index` (~600 indices) |
| Commandes I2C BA | `slavenode.c` → `enum enum_CODE_TRAMES` (codes 1-5) |
| Protocole HTTP | `Ethernet/www.c` → `sc_DialogueAvecServeur()` |
