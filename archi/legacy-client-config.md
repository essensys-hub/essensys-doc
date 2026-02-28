# Configuration Hardware et GPIO du Client Legacy

Ce document decrit le mapping GPIO complet, la configuration des peripheriques et les parametres systeme du firmware BP_MQX_ETH.

## 1. Mapping GPIO Complet

### Entrees Numeriques (DIN)

| Signal | Broche MCF52259 | Fonction |
|--------|-----------------|----------|
| `BP_I_OUVERTURE_SIRENE_INTERIEURE` | AS2 | Detection ouverture capot sirene interieure |
| `BP_I_OUVERTURE_SIRENE_EXTERIEURE` | TE5 | Detection ouverture capot sirene exterieure |
| `BP_I_OUVERTURE_PANNEAU_DOMOTIQUE` | AN7 | Detection ouverture panneau domotique |
| `BP_I_DETECT_OUV` | TF0 | Detecteur ouverture porte (alarme) |
| `BP_I_DETECT_PRES1` | TE7 | Detecteur presence 1 (alarme) |
| `BP_I_DETECT_PRES2` | TE6 | Detecteur presence 2 (alarme) |
| `BP_I_PLUIE` | DD3 | Detecteur de pluie (suspend arrosage) |
| `BP_I_SECTEUR_SYNCHRO` | NQ7 | IT primaire : synchronisation secteur (fil pilote) |
| `BP_I_SECTEUR_ETAT_ALIM_PRINCIPALE` | AN0 | Etat alimentation principale (perte secteur) |
| `BP_I_DIN_VITESSE_VENT` | TA3 | Anemometre (impulsions GPT) |
| `BP_I_NEW_INPUT_D5` | TH3 | Entree supplementaire V2 (2016) |
| `BP_I_NEW_INPUT_D6` | TH4 | Entree supplementaire V2 (2016) |
| `BP_I_NEW_INPUT_D7` | TH5 | Entree supplementaire V2 (2016) |

### Sorties Numeriques (DOUT)

| Signal | Broche MCF52259 | Fonction |
|--------|-----------------|----------|
| `BP_O_SIRENE_EXTERIEURE` | TC0 | Commande sirene exterieure |
| `BP_O_15VSP_ALIM_BA` | TE2 | Alimentation 15V boitiers auxiliaires |
| `BP_O_UC_LED_ETAT_BP` | TE0 | LED etat du boitier principal |
| `BP_O_UC_BATT_CTRL` | TE1 | Controle batterie de secours |
| `BP_O_VANNE_ARROSAGE` | DD7 | Commande electrovanne arrosage |
| `BP_O_PRISE_SECURITE` | DD4 | Coupure prise securite |
| `BP_O_MACHINE_A_LAVER` | DD6 | Coupure lave-linge/lave-vaisselle (fuite) |
| `BP_O_CUMULUS` | DD5 | Commande ballon eau chaude |
| `BP_O_FP_ZJ` | TA0 | Fil pilote zone jour |
| `BP_O_FP_ZN` | DD0 | Fil pilote zone nuit |
| `BP_O_FP_SDB1` | DD1 | Fil pilote salle de bain 1 |
| `BP_O_FP_SDB2` | DD2 | Fil pilote salle de bain 2 |
| `BP_O_TELEINF_LED` | TC3 | LED activite TeleInfo |
| `BP_O_ECRAN_DIRECTION` | UA3 | Direction half-duplex ecran |
| `BP_O_DEBUG_J1` | TF6 | Sortie debug 1 |
| `BP_O_DEBUG_J2` | TF5 | Sortie debug 2 |
| `BP_O_DEBUG_J3` | TF4 | Sortie debug 3 |
| `BP_O_DEBUG_J4` | TF3 | Sortie debug 4 |
| `BP_O_DEBUG_J5` | TF2 | Sortie debug 5 |

### PWM

| Signal | Canal | Fonction |
|--------|-------|----------|
| `BP_OPWM_SIRENE` | Canal 4 | Pilotage sirene interieure |

Niveaux PWM :
| Constante | Duty (%) | Volume |
|-----------|----------|--------|
| `uc_BUZ_TFORT` | 0% | Pleine puissance |
| `uc_BUZ_FORT` | 25% | Fort |
| `uc_BUZ_MOYEN` | 50% | Moyen |
| `uc_BUZ_FAIBLE` | 75% | Faible |
| `uc_BUZ_STOP` | 100% | Arret |

Durees :
- Sirene interieure : 300 secondes (5 min)
- Sirene exterieure : 180 secondes (3 min)

### ADC

| Canal | Signal | Fonction |
|-------|--------|----------|
| AIN0 | `VBAT` | Tension batterie de secours |
| AIN5 | `FUITE1` | Sonde fuite lave-linge |
| AIN6 | `FUITE2` | Sonde fuite lave-vaisselle |

## 2. Configuration des Peripheriques

### UART

| Port | Peripherique MQX | Vitesse | Mode | Fonction |
|------|-------------------|---------|------|----------|
| UART 0 | `ittya:` | 9600 bauds | Interruption, half-duplex | Ecran tactile |
| UART 1 | `ittyb:` | 1200 bauds | Interruption, 7 bits, parite paire | Compteur Linky |
| UART 2 | `ittyc:` | 9600+ | Debug | EspionRS (diagnostic) |

### I2C

| Port | Peripherique MQX | Vitesse | Mode | Fonction |
|------|-------------------|---------|------|----------|
| I2C 0 | `i2c0:` | 50 kHz | Polled, maitre | Communication BA |

### SPI

| CS | Broche | Vitesse | Fonction |
|----|--------|---------|----------|
| CS0 | QS3 | 500 kHz | EEPROM adresse MAC |
| CS2 | QS5 | 500 kHz | EEPROM soft (firmware OTA) |

## 3. Parametres Systeme

### Gestion Batterie de Secours

| Parametre | Valeur | Description |
|-----------|--------|-------------|
| `us_VBAT_MIN_pts` | 1500 (~10.5V) | Seuil minimum batterie (points ADC) |
| `us_VBAT_MIN_DISPLAY_pts` | 1600 | Seuil affichage alerte batterie |
| `uc_TEMPO_AVANT_COUPURE_sec` | 10 | Delai avant coupure sur batterie |
| `uc_VBAT_NB_ECHANTILLONS` | 7 | Nombre d'echantillons pour moyenne |
| `uc_TEMPO_AVANT_MODE_SECOURU_sec` | 10 | Delai avant passage en mode secouru |
| `uc_TEMPO_AVANT_SUPP_MODE_SECOURU_sec` | 5 | Delai avant sortie mode secouru |

### Alarme

| Parametre | Valeur | Description |
|-----------|--------|-------------|
| `us_TIMER_ALARME_CADENCEMENT_ms` | 1000 | Cadence de traitement alarme |
| `uc_DUREE_PROCEDURE_RENTREE_SORTIE_Sec` | 45 | Duree de la procedure entree/sortie |
| `uc_DUREE_ENTREE_ALARME_A_1_50ms` | 8 (400 ms) | Filtrage anti-rebond detecteurs |

### Chauffage (Fil Pilote)

6 modes disponibles pour chacune des 4 zones :

| Mode | Signification |
|------|---------------|
| OFF | Arret complet |
| CONFORT | Temperature de confort |
| ECO | Temperature economique |
| ECO_PLUS | Temperature tres economique |
| ECO_PLUS_PLUS | Temperature minimale |
| HORS_GEL | Protection hors gel |

| Parametre | Valeur | Description |
|-----------|--------|-------------|
| `uc_NB_IT_MODE_HG_FORCE` | 50 (500 ms) | Duree impulsion hors gel force |

### Diagnostic (EspionRS)

| Parametre | Valeur | Description |
|-----------|--------|-------------|
| `uc_ESPION_MOT_PASSE_ACTIVATION` | `"1256"` | Mot de passe d'activation du debug |
| `uc_TEMPO_DESACTIVATION_AUTO_sec` | 30 | Desactivation automatique apres inactivite |

## 4. Sequence d'Initialisation du Main

```
Main_task() — Boot (priorite 8, auto-start)
  │
  ├─ _time_delay(500)               Attente stabilisation alimentation
  │
  ├─ vd_EspionRS_Init()             Init debug serie (si DEBUG)
  │
  ├─ vd_TableEchangeLireEnFlash()   Charge la table d'echange depuis flash
  │
  ├─ Affichage versions             BP_VERSION_SERVEUR, TABLE_ECHANGE
  │
  ├─ vd_InitVariablesGlobales()     Init variables globales
  │
  ├─ vd_InitHard()                  Init GPIO, ADC, PWM, I/O
  │
  ├─ vd_SpiOpen()                   Ouvre le port SPI
  │
  ├─ vd_ReadAdresseMac()            Lit MAC depuis EEPROM (0xFA, 6 octets)
  │
  ├─ vd_ReadCleServeur()            Lit cle serveur (0x00, 16 octets)
  │
  ├─ vd_ReadCodeAlarme()            Lit code alarme (2 octets)
  │
  ├─ _time_delay(1000)              Attente stabilisation
  │
  ├─ Activation BP_O_UC_BATT_CTRL   Active controle batterie
  │
  ├─ Activation BP_O_15VSP_ALIM_BA  Active alimentation boitiers auxiliaires
  │
  ├─ _time_delay(100)               Stabilisation entrees
  │
  └─ Boucle principale              Chauffage, alarme, scenarios, fil pilote,
                                     arrosage, delestage, date/heure
```

## References Sources

- Mapping GPIO : `client-essensys-legacy/H/application.h`
- Parametres systeme : `client-essensys-legacy/H/global.h`
- Fonctions hardware : `client-essensys-legacy/H/Hard.h`
- Sequence init : `client-essensys-legacy/C/main.c`
