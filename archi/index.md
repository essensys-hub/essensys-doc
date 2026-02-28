# Architecture du Systeme Essensys

Cette documentation decrit l'architecture logicielle et systeme de l'ecosysteme Essensys, en s'appuyant sur les principes du modele C4 (Context, Containers, Components, Code) et l'approche *Clean Architecture*.

## 1. Contexte du Systeme (System Context)

Le systeme Essensys est une solution domotique concue initialement autour de cartes materielles embarquees (BP_MQX_ETH). Le defi majeur de l'architecture actuelle est de moderniser l'acces et le controle de ce materiel "legacy" tout en assurant une retrocompatibilite totale.

### Objectif Principal

Fournir une interface de controle moderne, securisee et performante (via des dashboards web, mobile, ou messagerie WhatsApp) tout en dialoguant avec un parc materiel existant dont les capacites reseau et logiques (firmware C sur Coldfire MCF52259) sont figees.

### Diagramme de Contexte

```mermaid
C4Context
    title Diagramme de Contexte - Essensys (2026)

    Person(user, "Utilisateur Final", "Controle sa domotique via navigateur, mobile ou WhatsApp")
    Person(admin, "Administrateur", "Maintient et deploie le systeme")

    System(essensys, "Ecosysteme Essensys", "Gere le chauffage, les volets, l'eclairage, l'alarme et la securite")

    SystemExt(hardware, "Cartes BP_MQX_ETH", "Controleurs materiels embarques Coldfire MCF52259 / MQX RTOS")
    SystemExt(whatsapp, "WhatsApp", "Canal de notification et interaction via OpenClaw")
    SystemExt(homeassistant, "Home Assistant", "Integration domotique tierce via MQTT Discovery")
    SystemExt(linky, "Compteur Linky", "Teleinfo consommation electrique via UART")
    SystemExt(unifi, "UniFi Protect", "Cameras de surveillance IP")
    SystemExt(dockerhub, "Docker Hub", "Registry des images conteneurs")
    SystemExt(github, "GitHub Actions", "Pipeline CI/CD multi-architecture")

    Rel(user, essensys, "Consulte et commande", "HTTPS / WhatsApp")
    Rel(admin, essensys, "Supervise et deploie", "SSH / HTTPS / Control Plane")
    Rel(essensys, hardware, "Bridge les commandes via polling HTTP synchrone", "HTTP Port 80 / LAN")
    Rel(essensys, whatsapp, "Envoie les alertes et recoit les commandes", "API WhatsApp Web")
    Rel(essensys, homeassistant, "Publie les etats et recoit les commandes", "MQTT")
    Rel(hardware, linky, "Lit la consommation electrique", "UART 1200 bauds")
    Rel(essensys, unifi, "Recupere les snapshots cameras", "HTTPS")
    Rel(github, dockerhub, "Pousse les images ARM64/AMD64", "Docker Push")
    Rel(admin, github, "Pousse le code source", "Git Push")
```

## 2. Le Defi Central : le Client Legacy

L'ensemble de l'architecture Essensys existe pour une seule raison : **combler l'obsolescence d'un controleur materiel dont le firmware ne peut pas etre modifie**.

La carte BP_MQX_ETH impose des contraintes techniques severes :

| Contrainte | Impact sur l'architecture |
|-----------|--------------------------|
| JSON malformes (cles non-quotees) | Le backend Go doit normaliser chaque requete entrante |
| Content-Type ` ;charset=UTF-8` (espace avant `;`) | Header HTTP non-standard code en dur dans le firmware |
| Reponse HTTP en single-packet TCP | Le reverse proxy Nginx doit bufferiser chaque reponse |
| Code `201 Created` pour les POST | Le backend doit repondre 201 au lieu du 200 standard |
| Champ `_de67f` en premiere position JSON | L'ordre des cles JSON doit etre controle cote serveur |
| Port 80 obligatoire | Le backend doit ecouter sur le port 80 (pas configurable) |
| Polling synchrone toutes les 2 secondes | Pas de push, pas de WebSocket, pas d'evenements |
| Valeurs 8 bits (0-255) par indice | Toute l'information passe par une table d'echange d'octets |

Pour une analyse detaillee du client legacy, voir **[Le Client Embarque BP_MQX_ETH](legacy-client.md)**.

Pour comprendre comment le serveur comble ces lacunes, voir **[Le Pattern Bridge : du Legacy au Moderne](bridge-pattern.md)**.

## 3. La Table d'Echange : Coeur du Systeme

Le mecanisme central de communication est une **table d'echange** de ~600 octets en memoire, partagee entre le firmware et le serveur. Chaque indice represente un etat, une configuration ou une commande (lumiere, volet, chauffage, alarme). Cette table est la source de verite unique du systeme.

Pour la documentation complete, voir **[Table d'Echange - Reference Technique](exchange-table.md)**.

## 4. Piliers Architecturaux

Le systeme a ete modularise pour separer les responsabilites :

- **Presentation (Frontend)** : Application React/Vite qui traduit les indices opaques en concepts visuels (boutons, sliders, zones). Aucune logique metier embarquee.
- **Bridge (Backend)** : Composant Go unique dedie a la traduction entre les API web modernes (REST/JSON normalise) et les trames specifiques au materiel. Agit comme un Anti-Corruption Layer.
- **Intelligence (MCP + OpenClaw)** : Couche IA connectee via le Model Context Protocol pour permettre l'interaction en langage naturel et la reformulation des alertes.
- **Observabilite (Prometheus + Alertmanager)** : Stack de monitoring complet avec alertes relayees via WhatsApp.
- **Infrastructure Edge** : Nginx (LAN) et Traefik (WAN/SSL) pour le routage, plus AdGuard pour le DNS.
- **Deploiement as-Code** : Ansible pour la configuration, Docker Compose pour l'orchestration, GitHub Actions pour le CI/CD multi-architecture.

## 5. Navigation dans la Documentation

| Document | Contenu |
|----------|---------|
| **[Le Client Embarque BP_MQX_ETH](legacy-client.md)** | Hardware, RTOS, contraintes techniques, obsolescence |
| **[Table d'Echange - Reference Technique](exchange-table.md)** | Cartographie des ~600 indices, droits d'acces, scenarios, bitmasks |
| **[Architecture des Conteneurs (Services)](containers.md)** | Les 14 services deployes, leurs roles et interactions |
| **[Le Pattern Bridge : du Legacy au Moderne](bridge-pattern.md)** | Comment le backend Go comble l'obsolescence du client |
| **[Architecture de Deploiement](deployment.md)** | Ansible, Docker Compose, CI/CD, infrastructure |
| **[Autocritique Clean Architecture / DDD](critique_ddd.md)** | Analyse critique, score, recommandations |
