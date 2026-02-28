# Securite du Client Embarque BP_MQX_ETH

Ce document decrit les mecanismes de securite implementes dans le firmware legacy : authentification HTTP, chiffrement des ordres d'alarme, et stockage des secrets en EEPROM SPI.

## 1. Authentification HTTP (Basic Auth)

Le firmware utilise HTTP Basic Authentication pour s'identifier aupres du serveur.

### Chaine de Generation de la Cle

```
uc_Cle_Acces_Distance[16]  (16 octets bruts, stockes en EEPROM SPI)
         │
         ▼
Conversion hexadecimale → chaine ASCII de 32 caracteres
         │
         ▼
     Hash MD5 (RFC 1321)
         │
         ▼
Formatage "16premierschiffres:16dernierschiffres" (33 caracteres)
         │
         ▼
    Encodage Base64
         │
         ▼
c_MatriculeCryptee[46]  (cle finale pour le header HTTP)
```

### Header HTTP Genere

```http
Authorization: Basic <c_MatriculeCryptee>
Accept: application/json,application/xhtml1+xml,application/xml;q=0.9,*/*;q=0.8
host: mon.essensys.fr
Cache-Control: max-age=0
Accept-Charset: ISO-8859-1,utf-8;q=0.7,*;q=0.3
Content-type: application/json ;charset=UTF-8
```

### Fonctions Cles

| Fonction | Fichier | Role |
|----------|---------|------|
| `cryptage()` | `Ethernet/Cryptage.c` | Generation complete de `c_MatriculeCryptee` |
| `c_EnteteTrameAuthorisation()` | `Ethernet/www.c` | Retourne `"Authorization: Basic "` |
| `c_EnteteTrameMatricule()` | `Ethernet/www.c` | Retourne `c_MatriculeCryptee` |

### Limitations

- Pas de TLS : la communication HTTP est en clair sur le LAN (RTCS ne supporte pas TLS)
- La cle Base64 est calculee une seule fois au demarrage et reutilisee indefiniment
- MD5 est considere cryptographiquement faible (collisions connues)

## 2. Chiffrement des Ordres Alarme (AES/Rijndael)

Les ordres de changement de code alarme sont chiffres en AES-CBC pour proteger le code d'acces.

### Algorithme

| Parametre | Valeur |
|-----------|--------|
| Algorithme | Rijndael (AES) |
| Mode | CBC (Cipher Block Chaining) |
| Taille bloc | 128 bits (16 octets) |
| Taille cle | 256 bits (32 octets) |
| IV | 8 premiers octets du hash MD5 de la cle serveur |

### Flux de Dechiffrement

```
Trame serveur (valeurs separees par ";")
         │
         ▼
  UnParceAES() → Parse en structure stAESParse
         │
         ▼
  sc_AnalyseOrdreAlarmeServeur()
         │
         ▼
  block_decrypt(MODE_CBC, cle, IV) → code alarme en clair
         │
         ▼
  Stockage en EEPROM SPI (2 octets : LSB + MSB)
```

### Fonctions Cles

| Fonction | Fichier | Role |
|----------|---------|------|
| `UnParceAES()` | `Ethernet/Cryptage.c` | Parse la trame AES (separateur `;`) |
| `sc_AnalyseOrdreAlarmeServeur()` | `Ethernet/www.c` | Dechiffrement AES-CBC du code alarme |
| `sc_TraitementAlarme()` | `Ethernet/www.c` | Traitement complet de l'ordre alarme |
| `rijndael_setup()` | `Ethernet/Cryptagerijndael_mode.c` | Initialisation du contexte AES |
| `block_decrypt()` | `Ethernet/Cryptagerijndael_mode.c` | Dechiffrement multi-blocs |

### Derivation de la Cle de Dechiffrement

La cle de dechiffrement alarme (`c_CleDecryptageAlarme[46]`) est derivee du meme MD5 que l'authentification :

```
MD5(cle_serveur_hex) → digest[16]
  └─ 8 premiers octets → c_CleDecryptageAlarme (IV pour AES-CBC)
```

## 3. Stockage des Secrets en EEPROM SPI

### Cartographie EEPROM

| Adresse | Taille | Contenu |
|---------|--------|---------|
| `0x00` | 16 octets | Cle serveur (`uc_Cle_Acces_Distance`) |
| `0x10` (apres cle) | 2 octets | Code alarme (LSB + MSB) |
| `0xFA` | 6 octets | Adresse MAC Ethernet |

### Configuration SPI

| Parametre | Valeur |
|-----------|--------|
| Vitesse | 500 kHz |
| Mode | Mode 0 (CPOL=0, CPHA=0) |
| Endianness | Big endian |
| CS EEPROM MAC | `MCF5XXX_QSPI_QDR_QSPI_CS0` |
| CS EEPROM Soft | `MCF5XXX_QSPI_QDR_QSPI_CS2` |

### Commandes EEPROM

| Commande | Code | Usage |
|----------|------|-------|
| READ | `0x03` | Lecture : `0x03 + adresse + donnees` |
| WRITE ENABLE | `0x06` | Activation ecriture |
| WRITE | `0x02` | Ecriture : `0x02 + adresse + donnees` |

Delai apres ecriture : 5 ms minimum.

### Fonctions Cles

| Fonction | Fichier | Role |
|----------|---------|------|
| `vd_ReadAdresseMac()` | `C/EepromAdresseMac.c` | Lit 6 octets a l'adresse `0xFA` |
| `vd_ReadCleServeur()` | `C/EepromAdresseMac.c` | Lit 16 octets a l'adresse `0x00` |
| `vd_ReadCodeAlarme()` | `C/EepromAdresseMac.c` | Lit 2 octets apres la cle serveur |
| `vd_UpdateCleServeurDansEEPROM()` | `C/EepromAdresseMac.c` | Mise a jour cle si modifiee |
| `vd_UpdateCodeAlarmeDansEEPROM()` | `C/EepromAdresseMac.c` | Mise a jour code alarme si modifie |
| `vd_SpiOpen()` | `C/Eepromspi.c` | Configuration port SPI |

## 4. Synthese des Risques

| Risque | Severite | Mitigation |
|--------|----------|------------|
| Communication HTTP en clair | Elevee | Gateway Raspberry Pi en relais local (LAN uniquement) |
| MD5 pour authentification | Moyenne | Cle unique par armoire, pas d'interception facile sur LAN |
| Cle serveur fixe en EEPROM | Moyenne | Modifiable par le serveur via `vd_UpdateCleServeurDansEEPROM()` |
| Code alarme en 2 octets | Faible | Chiffre en AES-CBC pendant le transport |
| Pas de rotation de cles | Moyenne | Architecture Gateway compense cote serveur |

## References Sources

- Authentification : `client-essensys-legacy/Ethernet/Cryptage.c`
- MD5 : `client-essensys-legacy/Ethernet/Cryptagemd5.c`
- AES/Rijndael : `client-essensys-legacy/Ethernet/Cryptagerijndael_mode.c`
- Headers HTTP : `client-essensys-legacy/Ethernet/www.c`
- EEPROM SPI : `client-essensys-legacy/C/Eepromspi.c`, `C/EepromAdresseMac.c`
