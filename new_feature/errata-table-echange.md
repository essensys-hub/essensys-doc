# Errata — Taille de la Table d'Echange

**Statut** : Corrections a appliquer  
**Date** : 2026-01-21  
**Origine** : Autocritique de [firmware-v2-local-fullstatus.md](firmware-v2-local-fullstatus.md), point 9.1

---

## Constat

La documentation dans `archi/` mentionne systematiquement "~600 indices" ou "~600 octets" pour la taille de la table d'echange `Tb_Echange[]`. Le calcul detaille de l'enum `Tbb_Donnees_Index` dans `client-essensys-legacy/H/TableEchange.h` donne en realite **953 indices**.

Le decompte de l'enum inclut des plages etendues (scenarios 590+, eclairages 605-622, I/O BA, variateurs 800+, anemometre 939-940, adresses MAC 947-952) qui depassent largement les 600 indices initialement estimes.

---

## Corrections a Appliquer dans `archi/`

### 1. `archi/exchange-table.md` (ligne 21)

**Actuel** :
```
- La taille totale est definie par l'enum `Nb_Tbb_Donnees` (~600 indices)
```

**Corrige** :
```
- La taille totale est definie par l'enum `Nb_Tbb_Donnees` (953 indices)
```

### 2. `archi/index.md` (ligne 72)

**Actuel** :
```
Le mecanisme central de communication est une **table d'echange** de ~600 octets en memoire
```

**Corrige** :
```
Le mecanisme central de communication est une **table d'echange** de 953 octets en memoire
```

### 3. `archi/index.md` (ligne 98)

**Actuel** :
```
| **[Table d'Echange - Reference Technique](exchange-table.md)** | Cartographie des ~600 indices, droits d'acces, scenarios, bitmasks |
```

**Corrige** :
```
| **[Table d'Echange - Reference Technique](exchange-table.md)** | Cartographie des 953 indices, droits d'acces, scenarios, bitmasks |
```

### 4. `archi/diagrams.md` (ligne 393 et 399)

**Actuel** :
```
Organisation de la table d'echange en memoire (~600 octets).
```
```text
subgraph Table["Tb_Echange[] — ~600 octets (unsigned char)"]
```

**Corrige** :
```
Organisation de la table d'echange en memoire (953 octets).
```
```text
subgraph Table["Tb_Echange[] — 953 octets (unsigned char)"]
```

### 5. `archi/img/mmd/table-echange-structure.mmd` (ligne 2)

**Actuel** :
```text
subgraph Table["Tb_Echange[] — ~600 octets (unsigned char)"]
```

**Corrige** :
```text
subgraph Table["Tb_Echange[] — 953 octets (unsigned char)"]
```

### 6. `archi/critique_ddd.md` (lignes 11 et 259)

**Actuel** :
```
> - **[exchange-table.md](exchange-table.md)** — Cartographie exhaustive des ~600 indices de la table d'echange
```
```
- ~~**Documenter la table d'echange**~~ → **Fait** : [exchange-table.md](exchange-table.md) avec cartographie exhaustive des ~600 indices
```

**Corrige** :
```
> - **[exchange-table.md](exchange-table.md)** — Cartographie exhaustive des 953 indices de la table d'echange
```
```
- ~~**Documenter la table d'echange**~~ → **Fait** : [exchange-table.md](exchange-table.md) avec cartographie exhaustive des 953 indices
```

### 7. `README.md` (ligne 25)

**Actuel** :
```
| [Table d'Echange](archi/exchange-table.md) | Cartographie des ~600 indices, droits d'acces, bitmasks, Flash |
```

**Corrige** :
```
| [Table d'Echange](archi/exchange-table.md) | Cartographie des 953 indices, droits d'acces, bitmasks, Flash |
```

---

## Resume

| Fichier | Occurrences | Correction |
|---------|-------------|------------|
| `archi/exchange-table.md` | 1 | `~600 indices` → `953 indices` |
| `archi/index.md` | 2 | `~600 octets` → `953 octets`, `~600 indices` → `953 indices` |
| `archi/diagrams.md` | 2 | `~600 octets` → `953 octets` (texte + diagramme Mermaid) |
| `archi/img/mmd/table-echange-structure.mmd` | 1 | `~600 octets` → `953 octets` |
| `archi/critique_ddd.md` | 2 | `~600 indices` → `953 indices` |
| `README.md` | 1 | `~600 indices` → `953 indices` |
| **Total** | **9 occurrences** | |

---

## Source de la Correction

Le decompte exact de l'enum `Tbb_Donnees_Index` dans `H/TableEchange.h` :

| Plage | Mnemonique | Nombre |
|-------|-----------|--------|
| 0-9 | Versions, Date/Heure | 10 |
| 10-12 | Status, Alerte, Information | 3 |
| 13-99 | Configuration systeme | 87 |
| 100-348 | Planning horaire (7 jours × 24h × ...) | 249 |
| 349-353 | Chauffage modes (4 zones + cumulus) | 5 |
| 354-440 | I/O, securite, detecteurs | 87 |
| 441-494 | Capteurs, fuites, compteurs | 54 |
| 495-589 | Variateurs, timers, configuration BA | 95 |
| 590-622 | Scenarios + eclairages + volets | 33 |
| 623-799 | I/O BA, configuration sorties | 177 |
| 800-938 | Variateurs courbe, configuration avancee | 139 |
| 939-940 | Anemometre (seuil + vitesse) | 2 |
| 941-946 | Arrosage, divers | 6 |
| 947-952 | Adresses MAC (6 octets) | 6 |
| **Total** | `Nb_Tbb_Donnees` | **953** |
