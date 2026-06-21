# Documentation Essensys

Bienvenue sur la documentation publique de l'écosystème **Essensys Domotique** :
architecture, installation gateway et guides utilisateur.

## Par où commencer ?

| Profil | Section |
|--------|---------|
| **Utilisateur** | [HTTPS local (`mon.essensys.local`)](install/https-local.md) |
| **Installateur CM5** | [Installation gateway](install/gateway-cm5.md) |
| **Installateur Raspberry Pi** | [Installation Raspberry Pi](install/raspberry-pi.md) |
| **Développeur / intégrateur** | [Architecture — vue d'ensemble](architecture/overview.md) |

## Architecture globale

![Architecture Essensys](architecture/img/architecture-globale.png)

## Écosystème

Essensys relie cartes embarquées (firmware legacy), gateway Raspberry Pi (Go/React),
portail cloud (`mon.essensys.fr`) et applications mobiles.

> Les sources canoniques restent sur GitHub (`essensys-hub`). Ce site est la facade
> publique hebergee sur `docs.essensys.fr`.
