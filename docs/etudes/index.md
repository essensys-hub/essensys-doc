---
title: "Études"
description: "Études techniques Essensys : remplacement des cartes de l'armoire après la foudre de 2026, exigence de résilience, architecture V2 « filaire d'abord », conseil d'autocritique, banc de développement et études V1 figées."
---

# Études

Cette section réunit des études techniques menées pour l'association. Chaque étude part de l'existant, propose une solution, la chiffre et dit ce qui reste à confirmer.

## Remplacement des cartes de l'armoire

L'armoire repose sur quatre cartes propriétaires : un boîtier principal (SC944D) et trois boîtiers auxiliaires. Après le coup de foudre du 9 août 2026 ([retour d'expérience](../retex/index.md)), deux d'entre eux ne répondent plus, et les composants d'origine se trouvent difficilement.

L'étude a connu deux versions. Les trois études V1 remplaçaient les cartes par d'autres calculateurs. Le 21 octobre 2026, une exigence nouvelle les a remises en cause : si le contrôleur grille, les boutons muraux doivent toujours commander leurs lumières et leurs volets, en filaire. La V2 y répond.

!!! tip "Commencer ici"
    **[Répondre à l'exigence de résilience](resilience.md)** : l'exigence née de la foudre, pourquoi les V1 n'y répondaient pas, l'architecture retenue, ce qu'elle coûte et comment on la prouvera.

### V2 : filaire d'abord, domotique en dérivation (recommandée)

| Page | Contenu |
| --- | --- |
| **[Étude V2 « filaire d'abord »](remplacement-armoire/v2/filaire-d-abord.md)** | Chaque bouton commande son circuit sans calculateur ; la domotique s'ajoute en parallèle et peut s'arrêter sans rien couper. Couche filaire seule ≈ 3 450 à 3 950 € HT, avec une couche domotique complète ≈ 6 450 à 7 850 € HT |
| [Conseil d'autocritique](remplacement-armoire/v2/conseil.md) | La question, la méthode et le verdict du 21 octobre 2026 : accords, désaccords, angles morts, recommandation |
| [Autocritique des études V1](remplacement-armoire/v2/autocritique-v1.md) | Ce que le conseil reproche à chaque étude V1, et ce que la V2 en garde |
| [Banc deux lumières](banc-deux-lumieres.md) | Le banc de développement de la V2 : implantation sur rail DIN, liste des fils, télérupteur Finder contre Eltako ES12Z |
| [Sections de câbles](remplacement-armoire/v2/sections-de-cables.md) | Rigide, souple et embouts : quelle section pour chaque liaison de l'armoire |

### V1 : trois études figées le 21 octobre 2026

Ces études restent publiées telles quelles, pour l'historique et pour ce que la V2 en reprend : câblage de migration, repiquage des phases, relais de couplage.

| Étude | Principe | Matériel, par armoire | Verdict du conseil |
| --- | --- | --- | --- |
| [Revolution Pi](remplacement-armoire/revolution-pi.md) | Un contrôleur industriel Linux, des modules d'entrées-sorties, des relais d'interface | environ 5 450 € HT | Transformer : la Connect 5 reste candidate pour la couche domotique |
| [Arduino Opta](remplacement-armoire/arduino-opta.md) | Quatre automates Opta répartis, avec extensions | environ 5 600 € HT | Abandonner ; garder le fusible par zone |
| [Raspberry Pi et Ethernet](remplacement-armoire/raspberry-pi-ethernet.md) | Refonte maison : quatre cartes nœuds Pico 2 en Ethernet, un Pi de gestion | environ 3 160 € HT | Abandonner les cartes ; garder l'isolement des entrées, le relais de garde et le battement de cœur |

Les trois études V1 partagent le même câblage de migration (répartiteur 230 V, blocs de phase Wago pour repiquer une phase sur plusieurs relais, jonctions des nappes, plan de bornage), que la V2 garde. Leurs prix ont été relevés en octobre 2026 ; leurs simulations 3D sont indicatives.
