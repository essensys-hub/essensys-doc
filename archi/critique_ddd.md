# Autocritique Architecture Essensys — v2

Analyse critique croisee entre la documentation (`essensys-doc/archi/`), les skills, le code source et les projets Altium des 4 cartes.

Date : janvier 2026 (mise a jour)

> **Historique** : Cette autocritique remplace la v1 (janvier 2026). La v1 a identifie 14 services non documentes,
> des ports incorrects dans le skill, et l'absence de documentation du client legacy.
> Depuis, une refonte massive a ete effectuee. Ce document fait le point sur l'etat actuel.

---

## 1. Inventaire de la Documentation

### 1.1 Fichiers dans `archi/` (20 documents)

| Document | Lignes | Sujet | Etat |
|----------|--------|-------|------|
| `index.md` | 110 | Vue d'ensemble C4, contexte systeme | OK |
| `legacy-client.md` | 234 | Client embarque BP_MQX_ETH | OK |
| `legacy-client-security.md` | 162 | Auth HTTP, AES alarme, EEPROM | OK |
| `legacy-client-build.md` | 138 | CodeWarrior, makefile, S19 | OK |
| `legacy-client-protocols.md` | 186 | I2C, UART, SPI | **Erreur format I2C** |
| `legacy-client-config.md` | 158 | GPIO, peripheriques, parametres | OK |
| `legacy-client-deployment.md` | 148 | Bootloader, OTA, JTAG | **Erreur EEPROM vs Flash** |
| `legacy-client-testing.md` | 128 | EspionRS, debug GPIO, CRC | OK |
| `exchange-table.md` | 470 | Cartographie des indices | **Erreur taille (~600 vs 953)** |
| `domaines-fonctionnels.md` | 674 | 10 domaines metier detailles | OK |
| `containers.md` | 192 | 14 services Docker | OK |
| `bridge-pattern.md` | 248 | Anti-Corruption Layer Go | OK |
| `deployment.md` | 73 | Infra, Ansible, Docker Compose | **Sous-documente** |
| `diagrams.md` | 478 | 10 diagrammes Mermaid | **Erreur taille + PNG manquants** |
| `critique_ddd.md` | — | Ce document (autocritique) | — |
| `hardware-overview.md` | 175 | Vue d'ensemble 4 cartes | **Incoherence I2C** |
| `hardware-sc944d.md` | 309 | BP (MCF52259) complet | **Erreur version MQX** |
| `hardware-sc940d.md` | 169 | BA PDV (PIC16F946) | OK |
| `hardware-sc941c.md` | 187 | BA PDE (PIC16F946) | OK |
| `hardware-sc942c.md` | 198 | BA CHB (PIC16F946) | OK |

### 1.2 Fichiers dans `new_feature/` (4 documents)

| Document | Lignes | Sujet |
|----------|--------|-------|
| `firmware-v2-local-fullstatus.md` | 559 | Migration DNS local + status reel + autocritique |
| `firmware-ha-integration.md` | 551 | Integration Home Assistant MQTT |
| `firmware-http-modernisation.md` | 561 | HTTPS, mDNS, SSDP/UPnP |
| `errata-table-echange.md` | 152 | Liste des corrections ~600→953 indices |

### 1.3 Couverture globale

| Domaine | Couverture | Commentaire |
|---------|------------|-------------|
| Client legacy (firmware) | **95%** | 7 documents detailles, GPIO, protocoles, build |
| Table d'echange | **80%** | Cartographie faite mais taille erronee |
| Services backend | **90%** | 14/14 services documentes |
| Hardware electronique | **90%** | 4 cartes, BOM, schemas, diagrammes |
| Infrastructure deploiement | **50%** | Diagramme basique, roles Ansible partiels |
| Domaines fonctionnels | **95%** | 10 domaines couverts |
| CI/CD | **30%** | Mentionne mais pas detaille |
| Skills/References | **70%** | 3 skills, corrections en attente |

---

## 2. Erreurs Factuelles Identifiees

### 2.1 CRITIQUE — Taille de la Table d'Echange : ~600 vs 953 indices

**Statut** : Documente dans `new_feature/errata-table-echange.md` mais **non corrige** dans `archi/`.

L'errata liste 9 occurrences a corriger dans 6 fichiers :

| Fichier | Ligne(s) | Texte actuel | Correction |
|---------|----------|--------------|------------|
| `exchange-table.md` | ~21 | `~600 indices` | `953 indices` |
| `index.md` | 72 | `table d'echange de ~600 octets` | `953 octets` |
| `index.md` | 98 | `Cartographie des ~600 indices` | `953 indices` |
| `diagrams.md` | ~393 | `~600 octets` | `953 octets` |
| `critique_ddd.md` (ancienne) | multiples | `~600 indices` | `953 indices` |
| `README.md` | 25 | `Cartographie des ~600 indices` | `953 indices` |

> **Action** : Appliquer les corrections de `errata-table-echange.md` dans les 6 fichiers concernes.

### 2.2 CRITIQUE — Format de Trame I2C Incoherent

Trois documents decrivent le format I2C BP→BA differemment :

| Document | Format emission BP→BA |
|----------|----------------------|
| `legacy-client-protocols.md` | **3 octets** : Code + CRC LSB + CRC MSB |
| `hardware-overview.md` | **6 octets** : Code + Donnee1 + Donnee2 + Donnee3 + CRC LSB + CRC MSB |
| `firmware-v2-local-fullstatus.md` (autocritique 9.2) | **6 octets** confirmes par analyse du code `ba_i2c.c` |

L'analyse du code source (`ba_i2c.c`, `slavenode.c`) confirme que le format reel est **6 octets** :
- Octet 0 : Code commande
- Octets 1-3 : Donnees (3 octets)
- Octets 4-5 : CRC-16

> **Action** : Corriger `legacy-client-protocols.md` section "Format de Trame I2C" — le format emission est 6 octets, pas 3.

### 2.3 ERREUR — Version MQX Incoherente

| Document | Version MQX |
|----------|-------------|
| `legacy-client-build.md` | MQX **3.8** (issu du makefile) |
| `hardware-sc944d.md` | MQX RTOS **4.0** |
| Skill `mcf52259-mqx-skill-reference.md` | MQX RTOS **4.0** |

Le makefile du projet (`client-essensys-legacy`) reference MQX **3.8**. La version 4.0 dans le skill et `hardware-sc944d.md` est erronee.

> **Action** : Corriger `hardware-sc944d.md` et le skill — MQX 3.8 (pas 4.0).

### 2.4 ERREUR — CS2 SPI : "EEPROM" vs "Flash"

| Document | Description CS2 |
|----------|-----------------|
| `legacy-client-protocols.md` | `CS2 = EEPROM Soft (firmware OTA)` |
| `legacy-client-deployment.md` | `Zone nouveau programme (EEPROM SPI externe)` |
| `hardware-sc944d.md` | `CS2 = SST25VF016B (Flash SPI 2 Mbit)` |
| BOM SC944D | `SST25VF016B-50-4I-S2AF : Memoire Flash SPI` |

Le composant U28 (SST25VF016B) est bien une **Flash SPI**, pas une EEPROM. La terminologie "EEPROM" dans les anciens docs legacy vient probablement du firmware qui utilise cette memoire de facon similaire a une EEPROM (lecture/ecriture octet).

> **Action** : Remplacer "EEPROM SPI externe" par "Flash SPI externe (SST25VF016B)" dans `legacy-client-protocols.md` et `legacy-client-deployment.md`.

### 2.5 ERREUR — Chevauchement d'indices : Vacances / Arrosage

Dans `exchange-table.md` :
- Section 3.7 : Vacances = indices **354-363**
- Section 3.8 : Arrosage = indices **363-406**

L'indice **363** apparait dans les deux sections. Verifier dans le code source si c'est un chevauchement reel ou une erreur de documentation.

> **Action** : Verifier l'enum `Tbb_Donnees_Index` dans `TableEchange.h` pour l'indice 363.

---

## 3. Incoherences de Liens et References Croisees

### 3.1 Documents Legacy sans liens vers Hardware

Les 6 documents `legacy-client-*.md` ne contiennent **aucun lien** vers les nouvelles pages hardware (`hardware-overview.md`, `hardware-sc944d.md`, etc.). Les lecteurs qui arrivent par le legacy n'ont aucun chemin vers la documentation electronique.

> **Action** : Ajouter dans `legacy-client.md` section 1 un lien vers `hardware-overview.md` et `hardware-sc944d.md`.
> Ajouter dans `legacy-client-config.md` un lien vers `hardware-sc944d.md` pour le mapping GPIO.
> Ajouter dans `legacy-client-protocols.md` un lien vers `hardware-overview.md` pour le bus I2C.

### 3.2 Documents Hardware sans liens vers Security/Deployment/Testing

`hardware-sc944d.md` section 10 reference 4 documents legacy mais omet :
- `legacy-client-security.md`
- `legacy-client-deployment.md`
- `legacy-client-testing.md`

> **Action** : Completer la section 10 de `hardware-sc944d.md` avec les 3 liens manquants.

### 3.3 Images PNG Manquantes dans `diagrams.md`

`diagrams.md` reference 8 images PNG dans `archi/img/` :
- `architecture-globale.png`
- `flux-bouton-relais.png`
- `flux-alertes-whatsapp.png`
- `conteneurs-c4.png`
- `pattern-bridge.png`
- `table-echange-structure.png`
- `deploiement-infra.png`
- `4-points-entree.png`

**Etat** : Les PNG existent-ils ? Les diagrammes sont aussi en Mermaid (`.mmd`). Si GitHub rend le Mermaid nativement, les PNG sont optionnels.

> **Action** : Verifier si les PNG sont generes. Sinon, soit les generer, soit supprimer les references `![](img/...)` au profit du rendu Mermaid natif.

### 3.4 Documents Legacy sans liens internes

Les 6 sous-documents (`legacy-client-security.md`, `-build.md`, `-protocols.md`, `-config.md`, `-deployment.md`, `-testing.md`) n'ont **aucun lien entre eux** ni vers le document parent `legacy-client.md`. Un lecteur qui arrive directement sur `legacy-client-security.md` n'a aucun moyen de naviguer vers les autres sous-documents.

> **Action** : Ajouter un bandeau de navigation en haut de chaque sous-document :
> ```markdown
> > Retour : [Client Embarque BP_MQX_ETH](legacy-client.md) | Voir aussi : [Securite](legacy-client-security.md) | [Build](legacy-client-build.md) | [Protocoles](legacy-client-protocols.md) | [GPIO](legacy-client-config.md) | [OTA](legacy-client-deployment.md) | [Debug](legacy-client-testing.md)
> ```

---

## 4. Contenu Manquant ou Sous-Documente

### 4.1 Deployment (`deployment.md`) — 73 lignes seulement

C'est le document le plus court du dossier `archi/`. Il manque :
- Detail des 17 roles Ansible (9 documentes sur 17 actifs)
- Configuration Docker Compose (variables d'environnement, volumes, reseaux)
- Flux CI/CD complet (GitHub Actions → Docker Hub → Control Plane update)
- Procedure de rollback
- Mecanisme d'update via le Control Plane

> **Action** : Enrichir `deployment.md` avec les roles Ansible manquants, le Docker Compose, et le flux CI/CD.

### 4.2 Glossaire Technique Absent

Malgre la cartographie de la table d'echange, il n'existe pas de glossaire qui traduise les termes firmware en concepts metier :
- `myactions` = file d'attente des ordres a executer
- `mystatus` = etat actuel de la table d'echange
- `serverinfos` = informations serveur (date, config)
- `_de67f` = champ d'authentification MD5
- `ExchangeKV{K: 613, V: "64"}` = "allumer chevet petite chambre 3"

> **Action** : Creer `glossaire.md` ou integrer dans `exchange-table.md` une section "Glossaire API Legacy".

### 4.3 Diagramme de Reseau LAN/WAN Absent

Aucun document ne montre le routage reseau complet :
- Traefik (WAN, HTTPS, Let's Encrypt)
- Nginx (LAN, port 80, proxy vers backend/MCP/CP/Prometheus)
- AdGuard (DNS, rewrite `mon.essensys.fr`)
- Firewall / NAT du routeur

> **Action** : Ajouter un diagramme de reseau dans `deployment.md` ou `diagrams.md`.

### 4.4 Pas de Documentation des Tests

Il n'existe aucun document sur les tests :
- Tests unitaires backend Go
- Tests d'integration (Redis, MQTT)
- Tests firmware (si applicables)
- Tests frontend (si applicables)
- Procedure de validation avant deploiement

> **Action** : Si des tests existent dans les depots, les documenter. Sinon, le signaler comme dette technique.

---

## 5. Critique du Skill `essensys-backend-reference-orders`

### 5.1 Corrections Appliquees depuis la v1

| Point | v1 (ancienne critique) | Etat actuel |
|-------|------------------------|-------------|
| Port backend 7070 vs 80 | Identifie | **Fait** |
| `systemctl` vs `docker` | Identifie | **Fait** |
| MCP `send_order` mal decrit | Identifie | **Fait** |
| Endpoints web non mentionnes | Identifie | **Fait** |
| MQTT non mentionne | Identifie | **Fait** |

### 5.2 Cles Redis — Documentees

**Fait** : Les 4 patterns de cles Redis sont maintenant documentes dans le skill SKILL.md et reference.md (`essensys:global:actions`, `essensys:client:{id}:exchange`, `essensys:client:{id}:connected`, `essensys:client:{id}:authinfo`).

---

## 6. Critique Clean Architecture / DDD

### 6.1 Ce qui a Progresse

| Aspect | Score v1 | Score v2 | Progres |
|--------|----------|----------|---------|
| Documentation legacy | 0% | 95% | +95% |
| Documentation hardware | 0% | 90% | +90% |
| Couverture services | 57% | 100% | +43% |
| Cartographie table echange | 0% | 80% | +80% |
| Domaines fonctionnels | 50% | 95% | +45% |

### 6.2 Ce qui Reste Problematique (Code)

Ces points necessitent du **refactoring code**, pas de la documentation :

1. **MCP Server viole le Repository Pattern** : Client Redis direct au lieu de `data.Store`
2. **God Object `action_service.go`** : Normalisation + generation + fusion + enqueue + MQTT + GUID dans un seul fichier
3. **Nommage generique** : `handlers.go`, `handlers_web.go`, `handlers_unifi.go` dans le meme package `api/`
4. **Control Plane duplique Redis** : Acces direct a Redis sans passer par l'API backend
5. **Ubiquitous Language absent** : Indices opaques (613, 64) sans semantique metier dans le code

---

## 7. Score Global Mis a Jour

| Critere | Score v1 (jan 2026) | Score apres refonte doc | Score actuel (jan 2026 v2) | Evolution |
|---------|---------------------|-------------------------|---------------------------|-----------|
| Separation macro (C4 conteneurs) | 7/10 | 9/10 | **9/10** | — |
| Separation micro (Clean Architecture) | 5/10 | 5/10 | **5/10** | — |
| Ubiquitous Language (DDD) | 3/10 | 5/10 | **5/10** | — |
| Couverture doc vs realite | 4/10 | 8/10 | **8.5/10** | +0.5 (hardware) |
| Infrastructure as Code | 8/10 | 8/10 | **8/10** | — |
| Skill backend/orders | 6/10 | 6/10 | **8/10** | +2 (P3 corrige) |
| Documentation hardware | — | — | **9/10** | Nouveau |
| Observabilite | 7/10 | 8/10 | **8/10** | — |
| Coherence interne des docs | — | — | **6/10** | Nouveau (erreurs factuelles) |
| Resilience CI/CD | 6/10 | 6/10 | **7/10** | +1 (P4 deployment enrichi) |

**Score moyen : 7.65/10** (+0.6 vs 7.05 apres P1/P2)

Les gains viennent de :
- P1/P2 : Toutes les erreurs factuelles corrigees + liens croises ajoutes
- P3 : Skill backend entierement mis a jour (ports, Docker, Redis, points d'entree)
- P4 : `deployment.md` enrichi (roles Ansible, Compose, CI/CD), glossaire API, diagramme reseau

Les freins restants sont :
- Le refactoring code (P5) : God Object, nommage, Redis direct dans MCP
- L'absence de tests documentes
- Les PNG non generes (Mermaid est la source de verite)

---

## 8. Plan d'Actions Priorise

### Priorite 1 — Corrections Factuelles (documentation uniquement)

| # | Action | Fichier(s) | Effort |
|---|--------|------------|--------|
| 1.1 | ~~Corriger ~600 → 953 indices~~ | `exchange-table.md`, `index.md`, `diagrams.md`, `README.md` | **Fait** |
| 1.2 | ~~Corriger format I2C (3→6 octets)~~ | `legacy-client-protocols.md` | **Fait** |
| 1.3 | ~~Corriger MQX 4.0 → 3.8~~ | `hardware-sc944d.md` | **Fait** |
| 1.4 | ~~Corriger "EEPROM" → "Flash SPI"~~ | `legacy-client-protocols.md`, `legacy-client-deployment.md` | **Fait** |
| 1.5 | ~~Corriger indice Vacances 354-363 → 354-362~~ | `exchange-table.md` | **Fait** |

### Priorite 2 — Liens Croises et Navigation

| # | Action | Fichier(s) | Effort |
|---|--------|------------|--------|
| 2.1 | ~~Ajouter liens hardware dans `legacy-client.md`~~ | `legacy-client.md` | **Fait** |
| 2.2 | ~~Ajouter liens legacy manquants dans `hardware-sc944d.md`~~ | `hardware-sc944d.md` | **Fait** |
| 2.3 | ~~Ajouter bandeau navigation dans 6 sous-docs legacy~~ | 6 fichiers | **Fait** |
| 2.4 | ~~Ajouter liens hardware dans `legacy-client-config.md` et `-protocols.md`~~ | 2 fichiers | **Fait** |

### Priorite 3 — Skill Backend

| # | Action | Fichier(s) | Effort |
|---|--------|------------|--------|
| 3.1 | ~~Port 7070 → 80~~ | Skill SKILL.md | **Fait** |
| 3.2 | ~~systemctl → docker~~ | Skill SKILL.md | **Fait** |
| 3.3 | ~~Ajouter cles Redis manquantes~~ | Skill reference.md | **Fait** |
| 3.4 | ~~Documenter les 4 points d'entree~~ | Skill SKILL.md | **Fait** |
| 3.5 | ~~Corriger description MCP~~ | Skill SKILL.md | **Fait** |

### Priorite 4 — Enrichissement Documentation

| # | Action | Fichier(s) | Effort |
|---|--------|------------|--------|
| 4.1 | ~~Enrichir `deployment.md` (Ansible, Compose, CI/CD)~~ | `deployment.md` | **Fait** |
| 4.2 | ~~Creer glossaire API Legacy~~ | `exchange-table.md` (section 9) | **Fait** |
| 4.3 | ~~Ajouter diagramme reseau LAN/WAN~~ | `diagrams.md` (section 11) | **Fait** |
| 4.4 | ~~Clarifier PNG manquants~~ | `diagrams.md` (note en-tete) | **Fait** |

### Priorite 5 — Refactoring Code (hors documentation)

| # | Action | Depot | Effort |
|---|--------|-------|--------|
| 5.1 | Unifier acces Redis (MCP → data.Store) | `essensys-server-backend` | 2-4h |
| 5.2 | Decouvrir `action_service.go` (God Object) | `essensys-server-backend` | 4-8h |
| 5.3 | Renommer handlers par domaine | `essensys-server-backend` | 2-4h |
| 5.4 | Introduire Ubiquitous Language | Tous | Progressif |

---

## References

- Ancienne critique v1 : commit `0f05e24` et anterieurs
- Errata table d'echange : [`new_feature/errata-table-echange.md`](../new_feature/errata-table-echange.md)
- Autocritique firmware v2 : [`new_feature/firmware-v2-local-fullstatus.md`](../new_feature/firmware-v2-local-fullstatus.md) (section 9)
- Documentation hardware : [`hardware-overview.md`](hardware-overview.md)
