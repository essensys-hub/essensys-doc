# Altium Designer Reference

## Altium File Types

| Extension | Type | Readable? | Content |
|-----------|------|-----------|---------|
| `.PrjPCB` | Project | Yes (INI) | Design hierarchy, document list, settings |
| `.PrjPCBStructure` | Structure | Yes (INI) | Hierarchy tree structure |
| `.OutJob` | Output Job | Yes (INI) | Manufacturing output definitions |
| `.SchDoc` | Schematic | No (binary) | Circuit schematics — use PDF exports |
| `.PcbDoc` | PCB Layout | No (binary) | Board layout — use Gerbers/STEP |
| `.SchLib` / `.SCHLIB` | Symbol Lib | No (binary) | Schematic symbols |
| `.PcbLib` | Footprint Lib | No (binary) | PCB footprints |
| `.IntLib` | Integrated Lib | No (binary) | Combined symbols + footprints |
| `.step` | 3D Model | Metadata only | Board/component 3D geometry |

## Gerber Layer Naming (Altium Default)

| Extension | Layer | Description |
|-----------|-------|-------------|
| `.GTL` | Top Copper | Signal layer 1 |
| `.G1` | Inner 1 | Signal/plane layer 2 |
| `.G2` | Inner 2 | Signal/plane layer 3 |
| `.GBL` | Bottom Copper | Signal layer N |
| `.GKO` | Keep-Out / Outline | Board contour / mechanical |
| `.GTS` | Top Solder Mask | Solder resist top |
| `.GBS` | Bottom Solder Mask | Solder resist bottom |
| `.GTP` | Top Paste | Stencil top |
| `.GBP` | Bottom Paste | Stencil bottom |
| `.GTO` | Top Overlay | Silkscreen top |
| `.GBO` | Bottom Overlay | Silkscreen bottom |
| `.GD1` | Drill Drawing | Drill guide layer |
| `.GG1` | Drill Guide | Drill guide layer |
| `.GM1`–`.GM32` | Mechanical | Mechanical/assembly layers |
| `.DRL` | Drill File | Excellon NC drill |
| `.DRR` | Drill Report | Hole size summary |
| `.LDP` | Drill Pairs | Layer pair definitions |
| `.apr` / `.APR_LIB` | Aperture | Gerber aperture definitions |
| `.RUL` | Design Rules | Export of PCB design rules |
| `.REP` | Report | General output report |

## BOM Analysis Checklist

When analyzing a BOM:

1. **Component count** — Total unique parts and total placements
2. **Category breakdown** — Passives, ICs, connectors, discretes, electromechanical
3. **Critical components** — Main MCU, regulators, PHY, crystals, protection devices
4. **Pricing** — Total BOM cost, most expensive components
5. **Availability risks** — Single-source components, obsolete parts
6. **Package variety** — 0402, 0603, 0805, 1206, SOT-23, QFP, BGA
7. **Voltage ratings** — Capacitor/resistor ratings vs. circuit requirements
8. **Temperature ratings** — Industrial (-40/+85°C) or commercial (0/+70°C)

## Schematic Review Checklist

When reviewing schematics (from PDF or assembly drawings):

1. **Power supply**
   - Input protection (TVS, fuse, reverse polarity)
   - Regulation topology (LDO, buck, boost)
   - Decoupling capacitors on all IC power pins
   - Power sequencing if multiple rails

2. **MCU section**
   - Crystal/oscillator and load capacitors
   - Reset circuit (supervisor, RC, or internal)
   - Debug/programming header (JTAG, SWD, BDM, ICSP)
   - Decoupling on VDD/VSS pins
   - Boot configuration pins

3. **Communication interfaces**
   - Ethernet: magnetics, PHY, termination, ESD protection
   - I2C: pull-up resistors (typical 4.7K for 100kHz, 2.2K for 400kHz)
   - UART: level shifting if needed (RS-232, RS-485)
   - SPI: chip select routing, clock integrity

4. **Protection**
   - ESD on external connectors (TVS diodes)
   - Overcurrent (fuses, PTC)
   - Reverse voltage (diode or MOSFET)
   - Surge protection on power input

5. **Connectors**
   - Pin assignments documented
   - Mating connectors specified
   - Wire gauge and current rating

## SC944D Schematic Hierarchy

From the `.PrjPCB` file, the SC944D has 22 schematic sheets:

| Order | Sheet | Functional Block |
|-------|-------|-----------------|
| 0 | Page_de_Garde | Title page |
| 1 | Alimentation_1-2 | Power supply (part 1) |
| 2 | Alimentation_2-2 | Power supply (part 2) |
| 3 | Chargeur_Batterie | Battery charger |
| 4 | Coeur | MCU (MCF52259) core |
| 5 | Ethernet | Ethernet PHY + magnetics |
| 6 | Liaison_IHM | Touchscreen UART interface |
| 7 | Arrosage | Irrigation (rain detect + valve) |
| 8 | Fil_Pilote_1-2 | Heating pilot wire (common) |
| 9 | Fil_Pilote_2-2 | Heating pilot wire (zone jour) |
| 10 | Machines_laver_2-2 | Washing machine (command) |
| 11 | Cumulus | Water heater relay |
| 12 | Porte_tableau | Panel door opening |
| 13 | Borniers | Terminal blocks |
| 14 | Detecteur_ouverture | Door/window opening detectors |
| 15 | Detecteurs_presence | Presence detectors (power + signal) |
| 16 | Liaison_Boitiers_Auxiliaires | I2C bus to auxiliary boards |
| 17 | Machines_laver_1-2 | Washing machine (leak detection) |
| 18 | Prises_de_Securite | Security outlets |
| 19 | Reserves_ETOR | Spare digital inputs |
| 20 | Sirenes | Sirens (power + command) |
| 21 | Teleinformation | Linky meter interface |

## Component Naming Convention (Essensys)

| Prefix | Type | Example |
|--------|------|---------|
| C | Capacitor | C4, C18 |
| R | Resistor | R1, R47 |
| D | Diode | D5, D14 |
| Q | Transistor | Q1, Q12 |
| U | IC | U1, U15 |
| J | Connector | J1, J12 |
| L | Inductor | L1 |
| F | Fuse | F1 |
| K | Relay | K1, K12 |
| T | Transformer | T1 |
| Y | Crystal | Y1 |
| LED | LED | LED1 |

## Documentation Templates

### Hardware Specification Template

```markdown
# [Board Name] — Hardware Specification

## 1. General
- **Board**: [Name] Rev [X]
- **Date**: [YYYY-MM-DD]
- **MCU**: [Part number]
- **Layers**: [N]
- **Dimensions**: [W × H mm]

## 2. Power Supply
| Rail | Voltage | Type | IC | Max Current |
|------|---------|------|-----|-------------|

## 3. Schematic Blocks
[Mermaid block diagram]

## 4. BOM Summary
| Category | Unique Parts | Total Qty | Cost |
|----------|-------------|-----------|------|

## 5. Connectors
| Ref | Type | Pins | Function |
|-----|------|------|----------|

## 6. Test Points
| TP | Net | Expected Value |
|----|-----|----------------|

## 7. Programming
| Interface | Connector | Pins |
|-----------|-----------|------|

## 8. Revision History
| Rev | Date | Changes |
|-----|------|---------|
```
