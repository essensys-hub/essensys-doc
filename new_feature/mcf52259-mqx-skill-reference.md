# Skill Expert MCF52259 / MQX RTOS / CodeWarrior

Reference de documentation technique pour la programmation du firmware BP_MQX_ETH sur Freescale (NXP) ColdFire MCF52259 avec MQX RTOS et CodeWarrior IDE.

## 1. Documentation Officielle NXP (PDFs)

### MCU — MCF52259

| Document | Lien | Contenu |
|----------|------|---------|
| **MCF52259 Reference Manual** | [MCF52259RM.pdf](https://nxp.com/docs/en/reference-manual/MCF52259RM.pdf) | Reference complete : registres, peripheriques (I2C, SPI, UART, GPIO, ADC, Timer, Ethernet FEC, USB, CAN), interruptions, DMA. **Document principal pour la programmation registres.** |
| **MCF52259 Datasheet** | [Alldatasheet](https://www.alldatasheet.com/datasheet-pdf/pdf/357119/FREESCALE/MCF52259CAG80.html) | Specifications electriques, pinout, timing, packages (46 pages) |
| **MCF52259 Errata** | [MCF52259DE.pdf](https://nxp.com/docs/en/errata/MCF52259DE.pdf) | Bugs silicium connus et workarounds |
| **M52259EVB User Manual** | [M52259EVBUM.pdf](https://nxp.com/docs/en/user-guide/M52259EVBUM.pdf) | Carte d'evaluation, schemas, connecteurs, jumpers |
| **TWR-MCF5225X Schematic** | [TWR-MCF5225X-SCH.pdf](https://www.nxp.com/downloads/en/schematics/TWR-MCF5225X-SCH.pdf) | Schema electrique carte Tower |

### Architecture ColdFire V2

| Document | Lien | Contenu |
|----------|------|---------|
| **ColdFire V2 Architecture** | [V2CFUMAD.pdf](https://nxp.com/docs/en/reference-manual/V2CFUMAD.pdf) | Jeu d'instructions, pipeline, registres, modes d'adressage, exceptions |
| **ColdFire IP Fact Sheet** | [COLDFIREIPLCFS.pdf](https://nxp.com/docs/en/fact-sheet/COLDFIREIPLCFS.pdf) | Resume architecture : 16 registres 32 bits, EMAC, BDM debug |

**Caracteristiques cles ColdFire V2 :**
- Instructions de 16, 32 ou 48 bits (RISC variable-length)
- Double pipeline decouplee 2 etages (IFP + OEP) avec FIFO
- 16 registres generaux 32 bits (D0-D7 data, A0-A7 address)
- Enhanced MAC (EMAC) : 4 accumulateurs 40 bits
- Background Debug Module (BDM) pour JTAG
- Jusqu'a 166 MHz (80 MHz sur MCF52259)

### MQX RTOS

| Document | Lien | Contenu |
|----------|------|---------|
| **MQX RTOS Reference Manual** | [Yumpu (438 pages)](https://www.yumpu.com/en/document/view/15317073/freescale-mqxtm-rtos-reference-manual) | **API complete** : taches, mutex, semaphores legers, files de messages, gestion memoire, timers |
| **MQX Getting Started** | [FSL_MQX_getting_started.pdf](https://nxp.com/docs/en/user-guide/FSL_MQX_getting_started.pdf) | Installation, configuration `user_config.h`, build des librairies, portage |
| **MQX Support User Guide** | [MQX_Support_User_Guide.pdf](https://nxp.com/docs/en/user-guide/MQX_Support_User_Guide.pdf) | Support, packages, documentation disponible |
| **MQX 4.0.1 Release Notes** | [FSL_MQX_release_notes.pdf](https://nxp.com/docs/en/supporting-information/FSL_MQX_release_notes.pdf) | Changements version 4.0.1 |
| **MQX Fact Sheet** | [MQXFS.pdf](https://nxp.com/docs/en/fact-sheet/MQXFS.pdf) | Resume : 6-8 Ko ROM, preemptif, multi-threading temps reel |
| **Writing Your First MQX App** | [AN3905.pdf](https://nxp.com/docs/en/application-note/AN3905.pdf) | Tutorial : installation, creation projet, premiere application |

### Stack Reseau RTCS (TCP/IP)

| Document | Lien | Contenu |
|----------|------|---------|
| **Small Footprint ColdFire TCP/IP** | [AN3507.pdf](https://nxp.com/docs/en/application-note/AN3507.pdf) | Stack TCP/IP configurable : HTTP, TCP/UDP, TFTP, DNS, DHCP. Flash: 33-45 Ko, RAM: 12-16 Ko |
| **RTCS Product Page** | [NXP MQXRTCS](https://nxp.com/design/design-center/software/embedded-software/mqx-software-solutions/mqx-tcp-ip:MQXRTCS) | Overview RTCS avec IPv6 |

### Drivers I2C sous MQX

| Document | Lien | Contenu |
|----------|------|---------|
| **I2C Driver Interrupt/Blocking** | [AN4652.pdf](https://nxp.com/docs/en/application-note/AN4652.pdf) | Driver I2C base interruptions avec mecanisme bloquant : master/slave, API simplifiee |
| **I2C on ColdFire+ and Kinetis** | [AN4342.pdf](https://nxp.com/docs/en/application-note/AN4342.pdf) | Guide I2C : specs, SMBus, exemples code |
| **MCFxxxx ColdFire I2C Driver** | [eCos Doc](https://doc.ecoscentric.com/ref/devs-i2c-m68k-mcfxxxx.html) | Driver ColdFire I2C : mode polled et interrupt, pas de DMA/FIFO |

### CodeWarrior IDE

| Document | Lien | Contenu |
|----------|------|---------|
| **CodeWarrior ColdFire V7.0 Quick Start** | [CodeWarrior_DevStudio.pdf](https://nxp.com/docs/en/quick-reference-guide/CodeWarrior_DevStudio.pdf) | Installation, licence Special Edition (128 Ko C), creation projet, simulateur |
| **CodeWarrior ColdFire V6.3 Targeting Manual** | [Unicamp PDF](https://dca.fee.unicamp.br/ftp/docs/ea079/manuais/CodeWarriorForColdFireV6.3.pdf) | Manuel complet : editeur, compilateur, linker, debugger |
| **CodeWarrior V7.2 (Classic IDE)** | [NXP Product Page](https://nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-legacy/codewarrior-development-studio-for-coldfire-architectures-classic-ide-v7-2:CW-COLDFIRE) | Page produit officielle, telechargement |
| **Flash Programmer (AN3859)** | [AN3859.pdf](https://nxp.com/docs/en/application-note/AN3859.pdf) | Ajout de devices au Flash Programmer, fichiers XML, algorithmes flash |
| **EWL Library Changes (TN268)** | [TN268.pdf](https://nxp.com/docs/en/application-note/TN268.pdf) | Remplacement MSL par EWL en V7.2, reduction memoire I/O |
| **TWR-MCF5225X Lab** | [TWRMCF52259LAB1.pdf](https://nxp.com/docs/en/supporting-information/TWRMCF52259LAB1.pdf) | Lab pratique : build MQX, GPIO, serial console, debug |

## 2. API MQX — Resume Rapide

### Gestion des Taches

```c
// Declaration des taches (template)
TASK_TEMPLATE_STRUCT MQX_template_list[] = {
    {TASK_ID, Task_func, stack_size, priority, "name", flags, time_slice},
    {0}  // terminateur
};

// Flags
MQX_AUTO_START_TASK  // Demarre automatiquement
MQX_TIME_SLICE_TASK  // Partage de temps avec meme priorite

// Fonctions
_task_create(proc, template_index, param);  // Cree une tache
_time_delay(ms);                            // Suspend la tache courante
_time_get(&time_struct);                    // Lit l'heure systeme
```

### Mutex

```c
MUTEX_STRUCT mutex;
MUTEX_ATTR_STRUCT attr;

_mutatr_init(&attr);
_mutex_init(&mutex, &attr);
_mutex_lock(&mutex);
// ... section critique ...
_mutex_unlock(&mutex);
```

### Semaphores Legers (Lightweight)

```c
LWSEM_STRUCT sem;
_lwsem_create(&sem, initial_count);
_lwsem_wait(&sem);    // Bloquant
_lwsem_post(&sem);    // Libere
```

### Files de Messages

```c
// Creation
_pool_id pool = _msgpool_create(msg_size, num_msgs, grow_num, grow_limit);
_queue_id qid = _msgq_open(queue_number, max_msgs);

// Envoi / Reception
msg_ptr = _msg_alloc(pool);
msg_ptr->HEADER.TARGET_QID = target_qid;
_msgq_send(msg_ptr);

msg_ptr = _msgq_receive(qid, timeout_ms);
_msg_free(msg_ptr);
```

### Events (Lightweight)

```c
LWEVENT_STRUCT event;
_lwevent_create(&event, 0);
_lwevent_set(&event, bit_mask);
_lwevent_wait_ticks(&event, bit_mask, all_bits, timeout);
_lwevent_clear(&event, bit_mask);
```

### I/O Subsystem

```c
// Ouverture peripherique
MQX_FILE_PTR fd = fopen("i2c0:", NULL);
MQX_FILE_PTR fd = fopen("ittya:", NULL);  // UART interrupt mode

// Configuration
ioctl(fd, IO_IOCTL_I2C_SET_BAUD, &baud);
ioctl(fd, IO_IOCTL_SERIAL_SET_BAUD, &baud);

// Lecture / Ecriture
read(fd, buffer, size);
write(fd, buffer, size);
fclose(fd);
```

### GPIO

```c
LWGPIO_STRUCT pin;
lwgpio_init(&pin, GPIO_PORT_TE | GPIO_PIN0, LWGPIO_DIR_OUTPUT, LWGPIO_VALUE_LOW);
lwgpio_set_functionality(&pin, BSP_LED1_MUX_GPIO);
lwgpio_set_value(&pin, LWGPIO_VALUE_HIGH);
lwgpio_toggle_value(&pin);
uint_32 val = lwgpio_get_value(&pin);
```

## 3. Peripheriques MCF52259 — Resume Registres

### I2C (Inter-IC Bus)

| Registre | Adresse | Bits Cles |
|----------|---------|-----------|
| I2ADR | Base+0x00 | Adresse esclave (7 bits) |
| I2FDR | Base+0x04 | Diviseur de frequence |
| I2CR | Base+0x08 | IEN, IIEN, MSTA, MTX, TXAK, RSTA |
| I2SR | Base+0x0C | ICF, IAAS, IBB, IAL, SRW, IIF, RXAK |
| I2DR | Base+0x10 | Registre donnees (lecture/ecriture) |

### SPI (QSPI)

| Registre | Description |
|----------|-------------|
| QMR | Mode : maitre/esclave, CPOL, CPHA, baud rate |
| QDLYR | Delais entre transferts |
| QIR | Interruptions et flags |
| QAR | Pointeur RAM interne (commandes/data) |
| QDR | Donnees RAM interne |
| QWR | Controle execution |

### UART

| Registre | Description |
|----------|-------------|
| UMR1/UMR2 | Mode (bits, parite, stop) |
| USR | Status (RXRDY, TXRDY, OE, PE, FE) |
| UCR | Commande (enable TX/RX, reset) |
| URB/UTB | Buffer reception / transmission |
| UACR | Controle auxiliaire |
| UISR/UIMR | Interruptions |

### GPIO

| Registre | Description |
|----------|-------------|
| PORTx | Lecture etat (x = A, B, C, D, E, F, G, H, ...) |
| DDRx | Direction (0 = entree, 1 = sortie) |
| SETx | Set bits a 1 |
| CLRx | Clear bits a 0 |
| PxxPAR | Multiplexage fonction (GPIO vs peripherique) |

### Timer (PIT — Periodic Interrupt Timer)

| Registre | Description |
|----------|-------------|
| PCSR | Controle et status |
| PMR | Modulo (periode) |
| PCNTR | Compteur courant |

## 4. Configuration Memoire

### MCF52259 Memory Map

| Zone | Adresse | Taille | Usage |
|------|---------|--------|-------|
| Flash interne | 0x00000000 | 512 Ko | Programme + bootloader + table d'echange |
| SRAM interne | 0x20000000 | 64 Ko | Stack, variables, buffers |
| Peripheriques | 0x40000000+ | — | Registres I/O mappes en memoire |
| Flash config | 0x0007E000 | 4 Ko | Secteur table d'echange (sauvegarde) |

### Empreinte Memoire MQX

| Composant | Flash | RAM |
|-----------|-------|-----|
| Kernel MQX | ~6-8 Ko | ~2-4 Ko |
| Stack RTCS (TCP/IP) | ~35-45 Ko | ~12-16 Ko |
| BSP + drivers | ~10-15 Ko | ~2-3 Ko |
| Application BP_MQX_ETH | ~200+ Ko | ~30+ Ko |
| **Total estime** | **~280 Ko / 512 Ko** | **~50 Ko / 64 Ko** |

## 5. Environnement de Developpement

### Installation CodeWarrior

| Prerequis | Valeur |
|-----------|--------|
| OS | Windows XP / Vista / 7 (32 bits) |
| CPU | Pentium 1 GHz minimum |
| RAM | 512 Mo min, 1 Go recommande |
| Disque | 2 Go |
| Licence | Special Edition (gratuite, limitee a 128 Ko de C pour V2/V3/V4) |
| Version recommandee | V7.2 Classic IDE |

### Programmation / Debug

| Methode | Outil | Connecteur |
|---------|-------|------------|
| JTAG/BDM | P&E Micro USB BDM | Connecteur BDM 26 broches |
| OSBDM | USB integre sur carte Tower | Mini-B USB (J17) |
| Flash Programmer | Integre dans CodeWarrior | Via BDM/OSBDM |

### Build du Firmware

```
1. Ouvrir CodeWarrior V7.2
2. File → Open → BP_MQX_ETH.mcp
3. Selectionner target "Int_Flash_Debug" ou "Int_Flash_Release"
4. F7 (Make) → compile et link
5. Sortie : BP_MQX_ETH.elf (debug) + BP_MQX_ETH.elf.s19 (flash)
6. Flash Programmer → Erase + Program → Flash interne
7. Debug → Run (F5)
```

## 6. Liens Communaute et Support

| Ressource | Lien |
|-----------|------|
| **NXP Community — MQX** | [community.nxp.com/t5/MQX-Software-Solutions](https://community.nxp.com/t5/MQX-Software-Solutions/ct-p/mqx-solutions) |
| **NXP MQX Product Page** | [nxp.com/MQX](https://nxp.com/design/design-center/software/embedded-software/mqx-software-solutions) |
| **CodeWarrior Downloads** | [NXP CW-COLDFIRE](https://nxp.com/design/design-center/software/development-software/codewarrior-development-tools/codewarrior-legacy/codewarrior-development-studio-for-coldfire-architectures-classic-ide-v7-2:CW-COLDFIRE) |
| **MCF52259 Product Page** | [NXP MCF52259](https://nxp.com/products/processors-and-microcontrollers/additional-mpu-mcus-architectures/coldfire-702) |

## References Sources

- MCF52259RM Rev.4 (mars 2011) — Reference manual principal
- V2CFUMAD — Architecture ColdFire V2 (jeu d'instructions)
- CodeWarrior DevStudio V7.0-7.2 — IDE, compilateur, linker, debugger
- MQX RTOS Reference Manual (438 pages) — API complete
- AN3507 — Stack TCP/IP ColdFire (RTCS)
- AN4652, AN4342 — Drivers I2C sous MQX
- AN3905 — Premier projet MQX
