# MCF52259 / MQX RTOS / CodeWarrior Expert Skill

This skill provides expert guidance for embedded firmware development on the Freescale (NXP) ColdFire MCF52259 microcontroller with MQX RTOS 3.8 and CodeWarrior IDE.

## Target Platform

- **MCU**: Freescale MCF52259 — ColdFire V2 core, 32 bits RISC, 80 MHz
- **Memory**: 512 Ko Flash interne + 64 Ko SRAM
- **OS**: MQX RTOS 3.8 (preemptif, time-slice, 5 taches)
- **IDE**: CodeWarrior for ColdFire Architectures V7.2 (Classic IDE)
- **Linker**: `mwldmcf` (Metrowerks)
- **Debugger**: P&E Micro BDM / OSBDM via JTAG

## Key Documentation (PDFs)

Always refer to these official documents when answering questions:

| Document | URL |
|----------|-----|
| MCF52259 Reference Manual (registres, peripheriques) | https://nxp.com/docs/en/reference-manual/MCF52259RM.pdf |
| ColdFire V2 Architecture (jeu d'instructions) | https://nxp.com/docs/en/reference-manual/V2CFUMAD.pdf |
| MQX RTOS Reference Manual (API) | https://www.yumpu.com/en/document/view/15317073/freescale-mqxtm-rtos-reference-manual |
| MQX Getting Started | https://nxp.com/docs/en/user-guide/FSL_MQX_getting_started.pdf |
| RTCS TCP/IP Stack (AN3507) | https://nxp.com/docs/en/application-note/AN3507.pdf |
| I2C Driver (AN4652) | https://nxp.com/docs/en/application-note/AN4652.pdf |
| CodeWarrior Quick Start | https://nxp.com/docs/en/quick-reference-guide/CodeWarrior_DevStudio.pdf |
| Flash Programmer (AN3859) | https://nxp.com/docs/en/application-note/AN3859.pdf |
| First MQX App (AN3905) | https://nxp.com/docs/en/application-note/AN3905.pdf |

## Project Context — BP_MQX_ETH (Essensys)

The firmware runs on the BP_MQX_ETH board (custom SC944D), a home automation controller that:

- Communicates with a Go backend server via HTTP polling every 2 seconds (port 80)
- Manages 3 auxiliary boards (BA) via I2C master (addresses 0x11, 0x12, 0x13)
- Controls a touchscreen via UART 0 (9600 baud)
- Reads Linky meter via UART 1 (1200 baud, 7 bits, even parity)
- Stores MAC, server key and alarm code in SPI EEPROM (25AA02E48T, CS0)
- Stores OTA firmware in external SPI Flash (SST25VF016B, 2 Mbit, CS2)
- Maintains a 953-byte exchange table (`Tb_Echange[Nb_Tbb_Donnees]`) as single source of truth
- Persists selected indices to internal Flash sector 0x7E000 (CRC-16 protected)

### MQX Task Architecture

```c
TASK_TEMPLATE_STRUCT MQX_template_list[] = {
    {MAIN_TASK,   Main_task,      1596, 8, "Main",     MQX_AUTO_START_TASK},
    {ECRAN_TASK,  Ecran_task,     1500, 8, "Ecran",    MQX_TIME_SLICE_TASK, 50},
    {BA_TASK,     Boitiers_task,  1796, 8, "I2C",      MQX_TIME_SLICE_TASK, 50},
    {TELE_TASK,   TeleInfo_task,  1396, 8, "TeleInf",  MQX_TIME_SLICE_TASK, 30},
    {ETH_TASK,    Ethernet_task,  3000, 8, "Ethernet", MQX_TIME_SLICE_TASK, 50},
};
```

All tasks run at priority 8 with time-slicing. Total stack: ~9288 bytes.

### Critical Firmware Constraints (immutable)

These are hardcoded in the firmware and the backend server MUST conform:

1. **Malformed JSON**: Keys are NOT quoted (`{k:613,v:"1"}` instead of `{"k":613,"v":"1"}`)
2. **Content-Type**: Must be exactly `application/json ;charset=UTF-8` (space before semicolon)
3. **Single-packet TCP**: HTTP response must fit in one `recv()` call
4. **HTTP 201 for POST**: All POST endpoints must return `201 Created`
5. **`_de67f` first**: The `_de67f` field must be the first key in action responses
6. **Port 80 only**: Firmware connects only to port 80
7. **8-bit values**: Each exchange table index is `unsigned char` (0-255)

### Source Code Structure

```
client-essensys-legacy/
├── C/          # Application: main, alarme, chauffage, ecran, I2C, etc.
├── H/          # Headers: application.h, global.h, TableEchange.h, etc.
├── Ethernet/   # Network: www.c, GestionSocket.c, Json.c, Download.c, Cryptage*.c
└── m52259evb_Int_Flash_Debug/  # Build: makefile, subdir.mk
```

## Coding Rules for This Platform

### Memory Constraints
- Flash: 512 Ko total, ~280 Ko used — be conservative with string literals and const data
- RAM: 64 Ko total, ~50 Ko used — avoid dynamic allocation, use MQX message pools
- Stack per task: 1396-3000 bytes — avoid deep recursion and large local arrays

### C Style
- Use Metrowerks/CW C89/C99 syntax
- All variables must be declared at function/block start (no mid-block declarations)
- Use `unsigned char`, `unsigned short`, `unsigned long` (not stdint types unless MQX typedef)
- Prefix conventions: `uc_` (unsigned char), `us_` (unsigned short), `ul_` (unsigned long), `vd_` (void function), `sc_` (signed char return), `sl_` (signed long), `st_` (struct)

### MQX Patterns
- Use `_time_delay(ms)` for cooperative yielding (all tasks same priority)
- Use mutex for shared data (exchange table zones)
- Use message queues for inter-task commands (Main → BA)
- Use lightweight semaphores (`LWSEM`) for simple synchronization
- Always check return codes from MQX API calls

### I2C Communication
- Use polled mode I2C via `sl_fct_write_polled()`
- Protect bus access with `LWEVENT_STRUCT lock_I2C`
- CRC-16 on all I2C frames
- 100ms delay between transactions
- Max reinit attempts: 50 (`uc_NB_REINIT_MAX`)

### HTTP Communication
- Build HTTP manually with `sprintf` + `strcat` into `c_EthernetBufferTX`
- Authentication: `Authorization: Basic <c_MatriculeCryptee>` (MD5 + Base64 of server key)
- Socket timeout: 10 seconds
- Close socket after each request/response cycle

## Documentation Essensys

Detailed architecture documentation is available in `essensys-doc/archi/`:

| Document | Content |
|----------|---------|
| `legacy-client.md` | Overview: 5 tasks, HTTP constraints, exchange table |
| `legacy-client-build.md` | Makefile, toolchain, build structure, versions |
| `legacy-client-deployment.md` | Bootloader, OTA, Flash layout, S19 format |
| `legacy-client-config.md` | GPIO mapping (MCU pin ↔ firmware constant ↔ function) |
| `legacy-client-protocols.md` | I2C frames (6 bytes TX, 5 bytes RX), CRC-16, SPI chip selects |
| `legacy-client-security.md` | MD5, Base64, AES/Rijndael-CBC, EEPROM secrets |
| `legacy-client-testing.md` | EspionRS debug system |
| `hardware-sc944d.md` | SC944D board: schematic blocks, BOM, MCU peripherals |
| `exchange-table.md` | 953 indices: mapping, rights, persistence, glossary |

## When to Use

Activate this skill when:
- Writing or modifying firmware code for MCF52259 / MQX RTOS
- Debugging I2C, UART, SPI, GPIO, Ethernet issues on ColdFire
- Configuring CodeWarrior projects, makefiles, linker scripts
- Working with the exchange table (`Tb_Echange[]`, 953 indices)
- Implementing new I2C commands for auxiliary boards
- Modifying HTTP protocol or server communication
- Understanding MQX RTOS task scheduling, synchronization
- Flashing firmware via JTAG/BDM or OTA (S19 format)
- Planning migration from CodeWarrior to GCC (see `essensys-gcc/prompt.md`)
