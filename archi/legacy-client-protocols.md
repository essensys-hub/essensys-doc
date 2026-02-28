# Protocoles de Communication du Client Legacy

Ce document decrit les protocoles de communication internes du firmware BP_MQX_ETH : I2C avec les boitiers auxiliaires, UART avec l'ecran tactile et le compteur Linky, et SPI avec l'EEPROM.

## 1. Bus I2C - Boitiers Auxiliaires (BA)

### Configuration

| Parametre | Valeur |
|-----------|--------|
| Peripherique | `i2c0:` (mode polled) |
| Vitesse | 50 kHz |
| Adresse BP (maitre) | `0x10` |
| Adresse BA (esclaves) | `0x11` (PDV), `0x12` (CHB), `0x13` (PDE) |

### Les 3 Boitiers Auxiliaires

| Boitier | Adresse | Zone | Responsabilite |
|---------|---------|------|----------------|
| BA PDV | `0x11` | Salon, salle a manger | Eclairages + volets pieces de vie |
| BA CHB | `0x12` | Chambres | Eclairages + volets chambres |
| BA PDE | `0x13` | Pieces d'eau | Eclairages cuisine, SDB, WC |

### Format de Trame I2C

**Emission (BP → BA) :**
```
┌──────────┬──────────┬──────────┐
│ Octet 0  │ Octet 1  │ Octet 2  │
│ Code     │ CRC LSB  │ CRC MSB  │
│ trame    │          │          │
└──────────┴──────────┴──────────┘
```

**Reponse (BA → BP) :**
```
┌──────────┬──────────┬──────────┬──────────┬──────────┐
│ Octet 0  │ Octet 1  │ Octet 2  │ Octet 3  │ Octet 4  │
│ Code     │ Reponse  │ CRC      │ CRC      │ CRC      │
│ trame    │          │ retour   │ trame    │ trame    │
└──────────┴──────────┴──────────┴──────────┴──────────┘
```

- CRC : Calcule sur les 3 premiers octets de la reponse
- Tempo inter-transaction : 100 ms

### Gestion des Erreurs I2C

| Code erreur | Signification |
|-------------|---------------|
| `I2C_OK` | Succes |
| `ERREUR_REINIT` | Echec reinitialisation bus |
| `ERREUR_BLOCAGE` | Bus I2C bloque (SCL/SDA bas) |
| `ERREUR_EMISSION_DATA` | Echec envoi donnees |
| `ERREUR_CRC_REPONSE` | CRC de la reponse invalide |

**Mecanisme de recuperation :**
- Reinitialisation automatique du bus apres blocage
- Nombre max de tentatives : `uc_NB_REINIT_MAX = 50`
- Repetitions avant erreur : `uc_I2C_NB_REPETE_AV_ERREUR = 5`
- Repetitions max : `uc_I2C_NB_REPETE = 20`

### Synchronisation

La tache `Boitiers_task` (quantum 50 ms) est la seule a acceder au bus I2C. Elle recoit les ordres de la tache Main via une file de messages MQX :

```c
_pool_id message_pool;
_queue_id BA_qid;
LWEVENT_STRUCT lock_I2C;  // Semaphore protection bus
```

## 2. UART Ecran Tactile

### Configuration

| Parametre | Valeur |
|-----------|--------|
| Peripherique | `ittya:` (mode interruption) |
| Vitesse | 9600 bauds |
| Mode | Half-duplex avec gestion de direction |
| Buffer TX | 260 octets |
| Buffer RX | 342 octets |
| Timeout | 1500 ms (`us_ECRAN_TIME_OUT_ms`) |
| Broche direction | `BP_O_ECRAN_DIRECTION` (UA3) |

### Codes de Trame

| Code | Direction | Signification | Format |
|------|-----------|---------------|--------|
| `0x0F` | BP → Ecran | Synchronisation | `0x0F + checksum` |
| `0xF0` | BP → Ecran | Demande de statut | `0xF0 + checksum` |
| `0x55` | BP → Ecran | Lecture donnees discretes | `0x55 + N + [indices 16 bits] + checksum` |
| `0x5A` | BP → Ecran | Ecriture donnees discretes | `0x5A + N + [indice 16 bits + valeur] + checksum` |
| `0xA5` | BP → Ecran | Lecture bloc | `0xA5 + params + checksum` |
| `0xAA` | BP → Ecran | Ecriture bloc | `0xAA + params + checksum` |

### Checksum

Calcul XOR sur tous les octets de la trame sauf le dernier (qui contient le checksum) :

```c
unsigned char uc_fct_Calcul_CheckSum(unsigned char *buffer, unsigned short taille) {
    unsigned char xor = 0;
    for (int i = 0; i < taille - 1; i++) {
        xor ^= buffer[i];
    }
    return xor;
}
```

### Donnees Transmises a l'Ecran

| Donnee | Type |
|--------|------|
| Date/heure | jour, mois, annee, heure, minute |
| Chauffage | Etat des 4 zones (ZJ, ZN, Zsdb1, Zsdb2) |
| Alarme | Mode, suivi, compte a rebours, detection, fraude |
| Alertes | Fuites, pluie, delestage |

### Synchronisation

Protection par semaphore leger :
```c
LWSEM_STRUCT st_LW_lock_screen;
```

## 3. UART TeleInfo (Compteur Linky)

### Configuration

| Parametre | Valeur |
|-----------|--------|
| Peripherique | `ittyb:` (mode interruption) |
| Vitesse | 1200 bauds |
| Bits de donnees | 7 bits |
| Parite | Paire |
| Timer polling | 100 ms (`us_TIMER_TELEINFO_ms`) |
| Timeout global | 2 secondes (`us_TELEINFO_TIME_OUT = 20 × 100ms`) |

### Donnees Extraites

| Etiquette | Timeout | Description |
|-----------|---------|-------------|
| Option tarifaire | 2s | Type d'abonnement |
| Periode tarifaire | 2s | HP/HC en cours |
| Puissance apparente (PAPP) | 2s | Watts (LSB + MSB sur 2 indices) |
| Index HCHC | 2s | Compteur heures creuses |
| Index HCHP | 2s | Compteur heures pleines |

### Stockage dans la Table d'Echange

La puissance apparente depasse 255, elle est stockee en 2 indices :
```c
TeleInf_PAPP_LSB  // Octet bas
TeleInf_PAPP_MSB  // Octet haut
// Valeur reelle = MSB × 256 + LSB
```

## 4. SPI EEPROM

### Configuration

| Parametre | Valeur |
|-----------|--------|
| Vitesse | 500 kHz |
| Mode | Mode 0 (CPOL=0, CPHA=0) |
| Endianness | Big endian |

### Chip Selects

| CS | Broche | EEPROM | Contenu |
|----|--------|--------|---------|
| CS0 | QS3 | EEPROM Adresse MAC | MAC (6 octets), cle serveur (16 octets), code alarme (2 octets) |
| CS2 | QS5 | EEPROM Soft | Firmware OTA (zone nouveau programme) |

### Commandes

| Commande | Code | Format |
|----------|------|--------|
| READ | `0x03` | `0x03 + adresse(1 octet) + donnees...` |
| WRITE ENABLE | `0x06` | `0x06` (avant chaque ecriture) |
| WRITE | `0x02` | `0x02 + adresse(1 octet) + donnees...` |

Delai post-ecriture : 5 ms minimum.

## 5. Synthese des Interfaces

```
┌─────────────────────────────────────────────────────────┐
│                    BP_MQX_ETH                           │
│                                                         │
│  ┌─────────┐   I2C 50kHz    ┌──────────────────────┐   │
│  │Boitiers │◄──────────────►│ BA PDV (0x11)        │   │
│  │ task    │               │ BA CHB (0x12)        │   │
│  │         │               │ BA PDE (0x13)        │   │
│  └─────────┘               └──────────────────────┘   │
│                                                         │
│  ┌─────────┐   UART 9600    ┌──────────────────────┐   │
│  │ Ecran   │◄──────────────►│ Ecran tactile        │   │
│  │ task    │  half-duplex   │ (proprietaire)       │   │
│  └─────────┘               └──────────────────────┘   │
│                                                         │
│  ┌─────────┐   UART 1200    ┌──────────────────────┐   │
│  │TeleInfo │◄──────────────│ Compteur Linky       │   │
│  │ task    │  7 bits paire  │                      │   │
│  └─────────┘               └──────────────────────┘   │
│                                                         │
│  ┌─────────┐   SPI 500kHz   ┌──────────────────────┐   │
│  │ Main    │◄──────────────►│ EEPROM MAC (CS0)     │   │
│  │ task    │               │ EEPROM Soft (CS2)    │   │
│  └─────────┘               └──────────────────────┘   │
│                                                         │
│  ┌─────────┐   TCP/IP       ┌──────────────────────┐   │
│  │Ethernet │◄──────────────►│ Serveur Essensys     │   │
│  │ task    │  Port 80       │ (mon.essensys.fr)    │   │
│  └─────────┘               └──────────────────────┘   │
└─────────────────────────────────────────────────────────┘
```

## References Sources

- I2C : `client-essensys-legacy/C/ba_i2c.c`
- Ecran : `client-essensys-legacy/C/Ecran.c`
- TeleInfo : `client-essensys-legacy/C/TeleInfo.c`
- SPI : `client-essensys-legacy/C/Eepromspi.c`
- Configuration bus : `client-essensys-legacy/H/application.h`
