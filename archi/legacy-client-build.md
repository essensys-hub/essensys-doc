# Build et Toolchain du Client Legacy

Ce document decrit le processus de compilation, la toolchain et le flashing du firmware BP_MQX_ETH.

## 1. Toolchain

| Composant | Version / Details |
|-----------|-------------------|
| IDE | CodeWarrior pour Coldfire (Metrowerks) |
| Linker | `mwldmcf` (Metrowerks Linker Coldfire) |
| Burner | `burner.exe` (HC08ToolsEnv) pour format S19 |
| RTOS | MQX 3.8 (Freescale/NXP) |
| Architecture | Coldfire V2 MCF52259 (32 bits RISC, 80 MHz) |
| BSP | `m52259evb` (Board Support Package) |

### Variables d'Environnement Requises

| Variable | Role |
|----------|------|
| `GNU_Make_Install_DirEnv` | Chemin vers GNU Make |
| `CF_ToolsDirEnv` | Chemin vers les outils Coldfire |
| `HC08ToolsEnv` | Chemin vers burner et outils S19 |

## 2. Structure du Projet

```
client-essensys-legacy/
├── C/                          # Sources C applicatives
│   ├── main.c                  # Point d'entree + init MQX
│   ├── Alarme.c                # Module alarme
│   ├── Chauffage.c             # Module chauffage (4 zones)
│   ├── Arrosage.c              # Module arrosage
│   ├── Scenario.c              # Scenarios domotiques
│   ├── Ecran.c                 # Communication ecran tactile
│   ├── ba_i2c.c                # Communication I2C boitiers auxiliaires
│   ├── EspionRS.c              # Debug serie (diagnostic)
│   ├── Eepromspi.c             # Driver SPI EEPROM
│   ├── EepromAdresseMac.c      # Lecture MAC, cle, code alarme
│   └── bootloader.c            # Bootloader minimal
│
├── H/                          # Headers
│   ├── application.h           # Config hardware, GPIO, constantes
│   ├── Hard.h                  # Interface fonctions materielles
│   ├── global.h                # Variables globales, versions, parametres
│   └── EspionRS.h              # Interface debug
│
├── Ethernet/                   # Stack reseau et protocoles
│   ├── www.c                   # Protocole HTTP legacy
│   ├── GestionSocket.c/.h      # Gestion sockets TCP
│   ├── Json.c                  # Parser JSON (non-standard)
│   ├── Download.c              # Telechargement firmware OTA
│   ├── Cryptage.c              # Generation cle auth
│   ├── Cryptagemd5.c           # Implementation MD5
│   └── Cryptagerijndael_mode.c # Implementation AES/Rijndael
│
├── m52259evb_Int_Flash_Debug/  # Configuration build
│   ├── makefile                # Makefile principal
│   ├── makefile.local          # Configuration locale
│   ├── sources.mk              # Liste des sources
│   ├── objects.mk              # Liste des objets
│   └── subdir.mk              # Sous-repertoires
│
├── docs/                       # Documentation embarquee
│
└── BP_MQX_ETH_..._.launch     # Configuration de lancement (JTAG/BDM)
```

## 3. Configurations de Build

### Debug (Int_Flash_Debug)

| Parametre | Valeur |
|-----------|--------|
| Cible | `BP_MQX_ETH.elf` |
| Linker script | `$(BSP)/intflash.lcf` |
| Optimisation | Aucune (debug) |
| Symboles debug | Oui |
| Sortie S19 | `BP_MQX_ETH.elf.s19` |

### Targets du Makefile

| Target | Commande | Role |
|--------|----------|------|
| `BP_MQX_ETH.elf` | `mwldmcf` | Link final en executable ELF |
| `BP_MQX_ETH.elf.s19` | `burner.exe` | Conversion ELF → S19 pour programmation |
| `clean` | `rm -rf` | Nettoyage des fichiers generes |

### Includes du Makefile

Le makefile inclut automatiquement :
- `sources.mk` : Liste de tous les fichiers sources
- `subdir.mk` : Regles pour le repertoire racine
- `Ethernet/subdir.mk` : Regles pour les sources reseau
- `C/subdir.mk` : Regles pour les sources applicatives
- `objects.mk` : Liste des fichiers objets

## 4. Sections Memoire Speciales

Le bootloader utilise des sections absolues pour placer du code a des adresses fixes :

| Section | Contenu | Usage |
|---------|---------|-------|
| `.APP_JUMP` | Code assembleur de saut vers `__boot` | Vecteur de demarrage application |
| `.APP_CRC` | CRC de l'application (defaut: `0x0102`) | Verification integrite firmware |
| `.APP_VERSION` | `us_BP_VERSION_SERVEUR` (actuellement: 37) | Version reportee au serveur |

## 5. Versions du Firmware

| Constante | Valeur | Role |
|-----------|--------|------|
| `uc_VERSION_BP_SOFT_SAVE` | 99 | Version du format de sauvegarde |
| `us_BP_VERSION_SERVEUR` | 37 | Version reportee au serveur via `/api/mystatus` |
| `uc_VERSION_TABLE_ECHANGE` | 30 | Version de la table d'echange |

## 6. Flashing du Firmware

### Methode JTAG/BDM (acces physique)

1. Connecter le programmeur BDM (P&E Micro) a la carte
2. Ouvrir la configuration `.launch` dans CodeWarrior
3. Flasher `BP_MQX_ETH.elf` via le debugger
4. Le bootloader verifie le CRC avant de lancer l'application

### Methode OTA (via serveur)

Le firmware supporte le telechargement OTA via HTTP :

1. Le serveur envoie le fichier S19 via `/api/download`
2. `Download.c` parse les lignes S19 (format Motorola)
3. Chaque ligne est ecrite en EEPROM SPI (zone "nouveau programme")
4. Verification CRC de la zone complete
5. Demande de reset pour appliquer la mise a jour

### Format S19

| Type | Signification |
|------|---------------|
| `S0` | Header (ignore) |
| `S3` | Donnees avec adresse 32 bits (traite) |
| `S7` | End record (ignore) |

Structure d'une ligne S3 : `S3 LL AAAAAAAA DD...DD CC`
- `LL` : Longueur (octets a partir de LL)
- `AAAAAAAA` : Adresse 32 bits
- `DD` : Donnees
- `CC` : Checksum (complement a 1 de la somme)

## 7. Statut d'Obsolescence

| Composant | Statut |
|-----------|--------|
| CodeWarrior | Plus supporte, derniere version ~2015 |
| MQX RTOS | Abandonne par NXP |
| Coldfire V2 | Architecture discontinuee |
| `mwldmcf` | Linker proprietaire Metrowerks, plus maintenu |

La compilation du firmware necessite un environnement de developpement historique qui n'est plus distribue.

## References Sources

- Makefile principal : `client-essensys-legacy/m52259evb_Int_Flash_Debug/makefile`
- Bootloader : `client-essensys-legacy/C/bootloader.c`
- Telechargement OTA : `client-essensys-legacy/Ethernet/Download.c`
- Configuration launch : `client-essensys-legacy/BP_MQX_ETH_m52259evb_Int_Flash_Debug_PEBDM.launch`
