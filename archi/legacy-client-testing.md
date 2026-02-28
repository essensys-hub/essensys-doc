# Diagnostic et Debug du Client Legacy

Ce document decrit les outils de diagnostic et de test embarques dans le firmware BP_MQX_ETH.

## 1. EspionRS — Systeme de Debug Serie

EspionRS est un systeme de debug interactif accessible via le port UART 2 (serie). Il permet d'observer en temps reel l'etat interne du firmware, les erreurs de communication et les compteurs de performance.

### Configuration

| Parametre | Valeur |
|-----------|--------|
| Port serie | UART 2 (`ittyc:`) |
| Activation | Compile uniquement en mode `DEBUG` |
| Mot de passe | `"1256"` |
| Desactivation auto | 30 secondes d'inactivite |

### Architecture Logicielle

```
Terminal serie (PC / convertisseur USB-serie)
         │
         ▼
  ┌──────────────────┐
  │   EspionRS        │
  │                   │
  │  vd_EspionRS()    │ ← Menu principal (interactif)
  │       │           │
  │       ├─ Messages evenementiels
  │       ├─ Afficher espions
  │       ├─ RAZ espions
  │       └─ Actions debug
  │                   │
  │  vd_EspionRS_     │
  │  Printf()         │ ← Logging avec horodatage (toutes taches)
  └──────────────────┘
```

### Menus de Diagnostic

| Menu | Fonction | Donnees Affichees |
|------|----------|-------------------|
| Ecran | `vd_EspionRS_Afficher_Ecran()` | Erreurs com ecran, timeouts, trames |
| BA / I2C | `vd_EspionRS_Afficher_BA()` | Erreurs I2C, blocages, reinits, CRC |
| Alarme | `vd_EspionRS_Afficher_Alarme()` | Etat detecteurs, mode, compteurs |
| Chauffage | `vd_EspionRS_Afficher_Chauffage()` | Zones, modes, temperatures |
| RTC | `vd_EspionRS_Afficher_RTC()` | Date/heure systeme |
| Hardware | `vd_EspionRS_Afficher_Hard()` | GPIO, ADC, PWM, tensions |
| TeleInfo | `vd_EspionRS_Afficher_TeleInfo()` | Linky, puissance, index HP/HC |
| Ethernet | `vd_EspionRS_Afficher_Ethernet()` | Socket, HTTP, DHCP, DNS |

### Compteurs d'Erreurs

Chaque module maintient des compteurs d'erreurs consultables et remettables a zero via EspionRS :

| Module | Fonction RAZ | Compteurs |
|--------|-------------|-----------|
| Ecran | `vd_EspionRS_RAZ_Ecran()` | Timeouts, erreurs checksum, trames invalides |
| BA / I2C | `vd_EspionRS_RAZ_BA()` | Blocages bus, erreurs CRC, reinits |
| Alarme | `vd_EspionRS_RAZ_Alarme()` | Fausses alertes, erreurs detecteurs |
| Hard | `vd_EspionRS_RAZ_Hard()` | Erreurs ADC, PWM |
| TeleInfo | `vd_EspionRS_RAZ_TeleInfo()` | Timeouts Linky, erreurs parite |
| Ethernet | `vd_EspionRS_RAZ_Ethernet()` | Erreurs socket, timeouts HTTP |

### Logging Horodate

La fonction `vd_EspionRS_Printf()` ajoute automatiquement un horodatage a chaque message :

```
[HH:MM:SS] Tache: Message
```

La variante `vd_EspionRS_PrintfSansHorodatage()` permet d'ecrire des blocs multi-lignes sans prefix.

### Messages Categorises par Source

| Categorie | Taches concernees |
|-----------|-------------------|
| Messages evenementiels | Toutes taches (Main, Ecran, BA, TeleInfo, Ethernet) |
| Erreurs de communication | Ecran, BA, Ethernet |
| Activite periodique | Main (boucle principale), Ethernet (polling) |
| Alertes materielles | Main (ADC, GPIO), Hard |

## 2. Sorties Debug (GPIO)

5 broches GPIO sont dediees au debug hardware avec un oscilloscope ou analyseur logique :

| Signal | Broche | Usage Typique |
|--------|--------|---------------|
| `BP_O_DEBUG_J1` | TF6 | Marqueur debut/fin de tache |
| `BP_O_DEBUG_J2` | TF5 | Marqueur interruption I2C |
| `BP_O_DEBUG_J3` | TF4 | Marqueur communication ecran |
| `BP_O_DEBUG_J4` | TF3 | Marqueur Ethernet |
| `BP_O_DEBUG_J5` | TF2 | General |

Ces broches sont accessibles sur les connecteurs J1-J5 de la carte et permettent de mesurer les temps d'execution, la periodicite des taches et les conflits de synchronisation.

## 3. Verification d'Integrite

### CRC Firmware

| Zone | Fonction | Description |
|------|----------|-------------|
| Application courante | `us_CalculerCRCZoneApp()` | CRC-16 de la zone application en flash |
| Nouveau programme | `us_CalculerCRCZoneNew()` | CRC-16 de la zone OTA en EEPROM |
| Comparaison | `sc_CheckZoneNouveauProgramme()` | Validation avant reset |

### Auto-surveillance au Demarrage

La sequence d'initialisation (Main_task) effectue des verifications :

1. Lecture de la table d'echange depuis flash
2. Affichage des versions (BP_VERSION_SERVEUR, TABLE_ECHANGE)
3. Init hardware et verification des peripheriques SPI
4. Lecture et verification de l'adresse MAC, cle serveur, code alarme

### Surveillance en Fonctionnement

| Element surveille | Methode | Seuil / Condition |
|-------------------|---------|--------------------|
| Tension batterie | ADC (echantillonnage) | < 1500 pts (~10.5V) → coupure |
| Alimentation principale | GPIO AN0 | Perte secteur → mode secouru |
| Bus I2C | Compteur blocages | > 50 reinits → erreur |
| Communication ecran | Timeout | > 1500 ms → erreur |
| Communication Linky | Timeout | > 2s → perte TeleInfo |
| Connexion serveur | Timeout HTTP | Cable, DHCP, DNS, serveur |

## 4. Indicateurs d'Etat Ethernet

Le firmware maintient 4 indicateurs d'etat pour diagnostiquer les problemes reseau :

| Variable | Signification |
|----------|---------------|
| `uc_EtatEthernetCablePB` | Probleme cable Ethernet |
| `uc_EtatEthernetDHCPPB` | Probleme obtention adresse DHCP |
| `uc_EtatEthernetDNSPB` | Probleme resolution DNS |
| `uc_EtatEthernetServeurPB` | Probleme connexion serveur |

Ces indicateurs sont reportes au serveur via `/api/mystatus` et visibles dans le dashboard.

## 5. Limitations du Debug

| Limitation | Impact |
|------------|--------|
| EspionRS compile uniquement en mode DEBUG | Pas de debug en production |
| UART 2 partagee | Necessite acces physique au connecteur debug |
| Pas de logging persistant | Les messages sont perdus au reboot |
| Pas de remote debug | Impossible de debugger a distance |
| Pas de core dump | Pas de capture automatique en cas de crash |

## References Sources

- EspionRS : `client-essensys-legacy/C/EspionRS.c`, `H/EspionRS.h`
- GPIO debug : `client-essensys-legacy/H/application.h`
- CRC firmware : `client-essensys-legacy/Ethernet/Download.c`
- Surveillance : `client-essensys-legacy/H/global.h`
