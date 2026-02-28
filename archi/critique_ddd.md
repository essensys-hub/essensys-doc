# Autocritique Architecture Essensys

Analyse critique croisée entre la documentation (`essensys-doc/archi/`), les skills (`essensys-backend-reference-orders`, `software-architecture`) et le code source réel de l'ensemble des dépôts.

Date : janvier 2026

> **Note** : Cette autocritique a servi de base à la refonte complète de la documentation architecture.
> Les corrections majeures ont été appliquées dans les documents suivants :
> - **[index.md](index.md)** — Diagramme C4 complet avec tous les acteurs et systèmes externes
> - **[legacy-client.md](legacy-client.md)** — Documentation détaillée du client BP_MQX_ETH et de ses contraintes
> - **[exchange-table.md](exchange-table.md)** — Cartographie exhaustive des ~600 indices de la table d'échange
> - **[containers.md](containers.md)** — Les 14 services réels avec descriptions complètes et corrections
> - **[bridge-pattern.md](bridge-pattern.md)** — Explication du pattern Anti-Corruption Layer du backend Go

---

## 1. Couverture documentaire vs réalité déployée

### Services documentés dans `containers.md`

| Service | Documenté | Déployé | Écart |
|---------|-----------|---------|-------|
| Traefik Gateway | Oui | Oui | - |
| Nginx interne | Oui | Oui | - |
| Frontend React | Oui | Oui | - |
| Support Portal | Oui (Next.js) | Oui (React/Vite) | **Tech stack faux** |
| Backend Go | Oui | Oui | - |
| Control Plane | Oui (vague) | Oui | **Sous-documenté** |
| Redis | Oui | Oui | - |
| Mosquitto | Oui | Oui | - |
| MCP Server | **Non** | Oui (port 8083) | **Absent de la doc** |
| AdGuard Home | **Non** | Oui | **Absent de la doc** |
| Prometheus | **Non** | Oui (port 9092) | **Absent de la doc** |
| Alertmanager | **Non** | Oui (port 9093) | **Absent de la doc** |
| Node Exporter | **Non** | Oui (port 9100) | **Absent de la doc** |
| OpenClaw | **Non** | Oui (port 18789) | **Absent de la doc** |

**Verdict** : La documentation `containers.md` ne couvre que **8 services sur 14 déployés**. Six composants critiques (monitoring, IA, DNS, MCP) sont invisibles dans l'architecture documentée.

### Rôles Ansible documentés vs existants

| Rôle | Dans `docs/roles.md` | Dans le playbook | Écart |
|------|---------------------|------------------|-------|
| `raspberry_common` | Oui | Oui | - |
| `raspberry_docker` | **Non** | Oui | Absent de la doc |
| `raspberry_mosquitto` | **Non** | Oui | Absent de la doc |
| `raspberry_redis` | **Non** | Oui | Absent de la doc |
| `raspberry_backend` | Oui | Oui | - |
| `raspberry_mcp` | **Non** | Oui | Absent de la doc |
| `raspberry_frontend` | Oui | Oui | - |
| `raspberry_nginx` | Oui | Oui | - |
| `raspberry_traefik` | Oui | Oui | - |
| `raspberry_control_plane` | **Non** | Oui | Absent de la doc |
| `raspberry_adguard` | Oui | Oui | - |
| `raspberry_prometheus` | **Non** | Oui | Absent de la doc |
| `raspberry_openclaw` | **Non** | Oui | Absent de la doc |
| `raspberry_compose` | **Non** | Oui | Absent de la doc |
| `raspberry_monitor` | Oui | Oui | - |
| `raspberry_logrotate` | Oui | Oui | - |
| `raspberry_push_status` | Oui | Oui | - |
| `raspberry_caddy` | **Non** | Non (optionnel) | Non documenté |
| `raspberry_homeassistant` | **Non** | Non (optionnel) | Non documenté |
| `raspberry_github_runner` | **Non** | Non (optionnel) | Non documenté |

**Verdict** : Sur 17 rôles actifs, seulement 9 sont documentés. 8 rôles non documentés dont des composants critiques (MCP, Prometheus, Control Plane, Compose).

---

## 2. Critique du skill `essensys-backend-reference-orders`

### Points forts

1. **Flux d'ordre correct** : Le flux `POST /api/admin/inject` → `ActionService.AddAction()` → Redis `essensys:global:actions` → `GET /api/myactions` → `POST /api/done/{guid}` est **exactement conforme** au code source (`internal/core/action_service.go`, `internal/api/handlers.go`).

2. **Règle du bloc complet 590+605..622** : Le code source confirme l'existence de `GenerateCompleteBlock()` dans `action_service.go` qui expand automatiquement les indices 605-622 quand un ordre scénario est envoyé. La règle documentée est **techniquement exacte**.

3. **Diagnostic Redis pertinent** : Les commandes `LLEN/LRANGE essensys:global:actions` correspondent aux clés réelles utilisées par `RedisStore.EnqueueAction()`.

### Points faibles et erreurs

1. **Port backend incorrect** : Le skill mentionne `curl -s http://127.0.0.1:7070/api/myactions` (port 7070). Or le code source montre que le backend écoute sur **port 80 par défaut** (`SERVER_PORT=80`). Le port 7070 est un ancien default ou une confusion. Le code log même un warning si le port n'est pas 80 (contrainte firmware BP_MQX_ETH).

2. **MCP `send_order` incomplètement documenté** : Le skill mentionne que MCP pousse directement dans Redis sans normalisation. C'est **partiellement faux** : le code MCP (`cmd/mcp-server/main.go`) implémente aussi l'auto-expansion du bloc 590+605..622 dans l'outil `send_order`. La normalisation existe côté MCP. Le vrai risque est `set_exchange_value` qui écrit directement dans la table d'échange sans passer par la queue d'actions.

3. **Absence de mention des endpoints web** : Le skill ignore `POST /api/web/actions` (endpoint utilisé par le frontend React) et ne mentionne que `POST /api/admin/inject`. Les deux chemins passent par `ActionService` mais avec des middlewares d'auth différents.

4. **Pas de mention MQTT** : Le backend accepte aussi des ordres via MQTT (`internal/mqtt/handlers.go` → `CommandHandler.HandleCommand()`), ce qui est un 4e point d'entrée pour les actions non documenté dans le skill.

5. **`systemctl is-active essensys-backend essensys-mcp` est faux** : Le backend et le MCP tournent dans des conteneurs Docker, pas comme services systemd. La commande correcte serait `docker ps | grep essensys-backend` ou `docker inspect essensys-backend`.

### Corrections recommandées

```diff
## Procedure de diagnostic rapide

1. Verifier services:
-   - `systemctl is-active essensys-backend essensys-mcp`
+   - `docker ps --format "table {{.Names}}\t{{.Status}}" | grep -E "backend|mcp"`
2. Verifier queue Redis:
   - `redis-cli LLEN essensys:global:actions`
   - `redis-cli LRANGE essensys:global:actions 0 2`
3. Verifier reponse backend:
-   - `curl -s http://127.0.0.1:7070/api/myactions`
+   - `curl -s http://127.0.0.1:80/api/myactions`
4. Comparer payload web vs payload MCP.
+5. Verifier via Control Plane:
+   - `curl -s http://127.0.0.1:9100/api/redis/actions`
```

---

## 3. Critique de la documentation architecture (C4 / Clean Architecture)

### 3.1 Diagramme de contexte (`index.md`)

**Problème** : Le diagramme ne montre que 2 acteurs (Utilisateur, Administrateur) et 1 système externe (BP_MQX_ETH). Il manque :

- **OpenClaw / WhatsApp** : L'utilisateur interagit aussi via messagerie (alertes WhatsApp)
- **Home Assistant** : Le broker MQTT est intégré avec HA via discovery
- **Prometheus/Alertmanager** : Surveillance automatisée avec alertes
- **AdGuard** : DNS et filtrage publicitaire
- **UniFi Protect** : Caméras de surveillance intégrées dans le frontend et le backend
- **Docker Hub** : Registry pour les images (CI/CD)
- **GitHub Actions** : Pipeline de build

**Le diagramme reflète l'architecture de 2024, pas celle de 2026.**

### 3.2 Diagramme de conteneurs (`containers.md`)

**Problèmes majeurs** :

1. **Support Portal décrit comme "Next.js/React"** : Le code source montre que c'est **React/Vite** (frontend) + **Go/Chi** (backend). Il n'y a aucune trace de Next.js dans le projet.

2. **MCP totalement absent** : Le MCP Server est un composant critique qui sert de pont entre les agents IA (OpenClaw) et le système domotique. Il n'apparaît nulle part dans le diagramme.

3. **Le Control Plane est mal décrit** : Présenté comme "Metrics/Admin" et "Surveillance du système". En réalité, c'est un véritable **panneau de contrôle opérationnel** avec :
   - Gestion des conteneurs Docker (restart, update, rollback)
   - Gestion Redis complète (exchange table, actions, backup/restore)
   - Proxy Prometheus et Alertmanager
   - Logs en temps réel via WebSocket
   - Audit trail SQLite
   - UI React complète avec 11 pages

4. **Flux de données incomplet** : Le diagramme montre `controlplane → backend` ("Lit la télémétrie") mais en réalité le Control Plane accède directement à Redis, Docker, Prometheus et Alertmanager — il ne passe pas par le backend.

5. **Traefik → Nginx → Backend** : Le flux `traefik → frontend` et `traefik → nginx → backend` est simplifié. En réalité :
   - Traefik gère le WAN (HTTPS, Let's Encrypt)
   - Nginx gère le LAN (port 80) avec proxy vers backend, MCP, Control Plane, Prometheus, Alertmanager, OpenClaw
   - Les deux coexistent avec des responsabilités distinctes

### 3.3 Architecture de déploiement (`deployment.md`)

**Problèmes** :

1. **Diagramme de déploiement incomplet** : Ne montre que 5 conteneurs Docker (Traefik, Backend, Frontend, Redis, Mosquitto). Il en manque 7 (MCP, Control Plane, AdGuard, Prometheus, Alertmanager, Node Exporter, OpenClaw).

2. **Services non-dockérisés mal décrits** : Mentionne "Ansible" et "Systemd" mais ne détaille pas les services systemd réels :
   - `essensys-mqtt-debug.service` (monitoring MQTT)
   - `essensys-push-status.timer` (push status périodique)
   - `logrotate` (rotation des logs)

3. **Docker Compose non mentionné** : Tout est orchestré via `docker compose` depuis le rôle `raspberry_compose`. Le document parle de "conteneurs" individuels alors que c'est un stack Compose unifié.

4. **Cycle de vie incomplet** : Le cycle CI/CD mentionne GitHub Actions et les images Docker, mais ne documente pas :
   - Le build multi-architecture (ARM64/AMD64 via QEMU)
   - Le cache GHA
   - Le push vers Docker Hub (`essensyshub/`)
   - Le mécanisme d'update via le Control Plane

---

## 4. Critique Clean Architecture / DDD (mise à jour)

### Ce qui a progressé (vs critique initiale)

1. **Repository Pattern implémenté** : L'interface `data.Store` avec `RedisStore`, `MemoryStore`, `DatabaseStore` montre une abstraction correcte de la couche données. La critique initiale sur le "couplage fort avec l'infrastructure" est **partiellement résolue** côté backend principal.

2. **Séparation des couches visible** :
   - `internal/models/` → Entités du domaine
   - `internal/core/` → Logique métier (`ActionService`, `StatusService`)
   - `internal/data/` → Persistance abstraite
   - `internal/api/` → Handlers HTTP
   - `internal/mqtt/` → Intégration externe

### Ce qui reste problématique

1. **MCP Server viole le Repository Pattern** : Le serveur MCP (`cmd/mcp-server/main.go`) utilise directement `go-redis/redis/v8` au lieu de passer par l'interface `data.Store`. Il y a donc **deux clients Redis indépendants** dans le même projet Go, avec des risques de divergence de schéma.

2. **Pas d'Ubiquitous Language** : Malgré la critique initiale, le vocabulaire reste technique :
   - `myactions`, `mystatus`, `serverinfos` → héritage firmware, pas de traduction métier
   - `ExchangeKV{K: 613, V: "64"}` → aucune sémantique (qu'est-ce que 613 ? qu'est-ce que 64 ?)
   - Le skill `reference.md` est le seul endroit qui tente de documenter ce mapping, mais de manière incomplète

3. **God Object latent dans `action_service.go`** : Ce fichier gère :
   - La normalisation des ordres
   - La génération du bloc complet 605-622
   - La fusion bitwise
   - L'enqueue Redis
   - La publication MQTT
   - La gestion des GUIDs
   
   C'est exactement le scénario "God Object" anticipé dans la critique initiale.

4. **Nommage générique persistant** : `handlers.go`, `handlers_web.go`, `handlers_unifi.go` dans le même package `api/` montre un découpage par méthode technique plutôt que par domaine métier.

5. **Control Plane duplique des responsabilités** : Le Control Plane accède directement à Redis pour lire/écrire la table d'échange et gérer les actions. C'est une duplication de la logique du backend sans passer par son API. Deux chemins d'accès aux mêmes données Redis = risque de désynchronisation.

---

## 5. Incohérences techniques concrètes

### 5.1 Ports

| Service | Doc / Config | Code réel | Cohérent |
|---------|-------------|-----------|----------|
| Backend | 7070 (skill) | 80 (code) | **Non** |
| MCP | 8083 (ansible) | 8080 (code default) | **Paramétré** |
| Control Plane | 9100 (compose) | 9100 (code) | Oui |
| Prometheus | 9092 (compose) | 9092 (control plane) | Oui |
| Alertmanager | 9093 (compose) | 9093 (control plane) | Oui |
| OpenClaw | 18789 (ansible) | 8080 (default image) | **À vérifier** |

### 5.2 Images Docker

| Service | Image | Multi-arch ARM64 | Vérifiable |
|---------|-------|-----------------|------------|
| Backend | essensyshub/essensys-server-backend | Oui (workflow) | Oui |
| Frontend | essensyshub/essensys-nginx | Oui (custom) | Oui |
| Control Plane | essensyshub/essensys-control-plane | Oui (workflow) | Oui |
| MCP | essensyshub/essensys-server-backend (mcp-server) | Oui | Oui |
| OpenClaw | coollabsio/openclaw | **Non vérifié** | **Risque ARM64** |

### 5.3 Clés Redis

Les clés Redis documentées dans le skill vs le code :

| Pattern | Skill | Code backend | Code MCP | Code CP |
|---------|-------|-------------|----------|---------|
| `essensys:global:actions` | Oui | Oui | Oui | Oui |
| `essensys:client:{id}:exchange` | Non | Oui | Oui | Oui |
| `essensys:client:{id}:connected` | Non | Oui | Non | Oui |
| `essensys:client:{id}:authinfo` | Non | Oui | Non | Oui |

**Le skill ne documente qu'une seule clé Redis sur quatre patterns utilisés.**

---

## 6. Recommandations prioritaires

### Priorité 1 — Documentation critique ✅ Résolu

1. ~~**Mettre à jour `containers.md`**~~ → **Fait** : [containers.md](containers.md) documente les 14 services avec descriptions complètes
2. **Corriger le skill `reference.md`** : Port 80 (pas 7070), commandes Docker (pas systemd), documenter les 4 patterns de clés Redis *(en attente)*
3. ~~**Corriger "Next.js"**~~ → **Fait** : [containers.md](containers.md) décrit correctement le Support Portal comme React/Vite + Go/Chi

### Priorité 1 bis — Documentation legacy ✅ Résolu

- ~~**Documenter le client BP_MQX_ETH**~~ → **Fait** : [legacy-client.md](legacy-client.md)
- ~~**Documenter la table d'échange**~~ → **Fait** : [exchange-table.md](exchange-table.md) avec cartographie exhaustive des ~600 indices
- ~~**Documenter le pattern bridge**~~ → **Fait** : [bridge-pattern.md](bridge-pattern.md)

### Priorité 2 — Cohérence architecturale (partiellement résolu)

4. **Unifier l'accès Redis** : Le MCP Server devrait utiliser l'interface `data.Store` du backend au lieu d'un client Redis direct *(en attente — refactoring code)*
5. ~~**Documenter les 4 points d'entrée des ordres**~~ → **Fait** : Documenté dans [bridge-pattern.md](bridge-pattern.md) section 4 et [exchange-table.md](exchange-table.md) section 8
6. ~~**Créer un glossaire technique**~~ → **Partiellement fait** : [exchange-table.md](exchange-table.md) mappe chaque index vers un concept métier. Un glossaire dédié reste souhaitable.

### Priorité 3 — Évolution (en attente)

7. **Documenter les rôles Ansible manquants** (10 rôles non documentés)
8. **Décrire le flux CI/CD complet** (GitHub Actions → Docker Hub → Control Plane update)
9. **Documenter les rôles optionnels** (Caddy, Home Assistant, GitHub Runner)
10. **Ajouter un diagramme de flux réseau** montrant les interactions LAN/WAN entre Nginx, Traefik, et les services

---

## 7. Score global

### Score initial (avant refonte doc — janvier 2026)

| Critère | Note | Commentaire |
|---------|------|-------------|
| Séparation macro (C4 conteneurs) | 7/10 | Bonne, mais 6 services non documentés |
| Séparation micro (Clean Architecture) | 5/10 | Repository pattern présent mais pas universel, God Object latent |
| Ubiquitous Language (DDD) | 3/10 | Vocabulaire technique dominant, indices opaques |
| Couverture doc vs réalité | 4/10 | 57% des services documentés, ports incorrects dans le skill |
| Infrastructure as Code | 8/10 | Ansible bien structuré, Docker Compose unifié, CI/CD fonctionnel |
| Skill backend/orders | 6/10 | Flux correct mais port faux, MCP mal décrit, systemd au lieu de Docker |
| Observabilité | 7/10 | Prometheus + Alertmanager + OpenClaw, mais non documentés |
| Résilience CI/CD | 6/10 | Build multi-arch très lent (QEMU), pas de cross-compile natif Go |

**Score moyen initial : 5.75/10**

### Score après refonte documentation (janvier 2026)

| Critère | Note | Commentaire |
|---------|------|-------------|
| Séparation macro (C4 conteneurs) | **9/10** | 14/14 services documentés dans `containers.md` |
| Séparation micro (Clean Architecture) | 5/10 | Inchangé — nécessite du refactoring code |
| Ubiquitous Language (DDD) | **5/10** | `exchange-table.md` mappe les indices vers des concepts métier |
| Couverture doc vs réalité | **8/10** | 100% des services documentés, table d'échange cartographiée |
| Infrastructure as Code | 8/10 | Inchangé |
| Skill backend/orders | 6/10 | Inchangé — le skill n'a pas été mis à jour |
| Observabilité | **8/10** | Stack documentée dans `containers.md` et `bridge-pattern.md` |
| Résilience CI/CD | 6/10 | Inchangé |

**Score moyen après refonte : 6.88/10** (+1.13 points)

Les principaux gains proviennent de la documentation : 6 services ajoutés, table d'échange cartographiée, contraintes legacy détaillées, pattern bridge explicité. Les axes d'amélioration restants sont principalement du **refactoring code** (God Object, MCP Redis direct, Ubiquitous Language).
