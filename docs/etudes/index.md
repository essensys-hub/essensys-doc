---
title: "Études"
description: "Études techniques Essensys : remplacement des cartes propriétaires de l'armoire par un matériel disponible, câblage de migration, modes dégradés, coût et feuille de route."
---

# Études

Cette section réunit des études techniques menées pour l'association. Chaque étude part de l'existant, propose une solution, la chiffre et dit ce qui reste à confirmer.

## Remplacement des cartes de l'armoire

L'armoire repose sur quatre cartes propriétaires : un boîtier principal (SC944D) et trois boîtiers auxiliaires. Après le coup de foudre du 9 août 2026 ([retour d'expérience](../retex/index.md)), deux d'entre eux ne répondent plus, et les composants d'origine se trouvent difficilement. Trois pistes ont été étudiées sur la même base : un câblage de migration commun, posé avant le choix, qui permet de basculer et de revenir en arrière.

| Étude | Principe | Matériel, par armoire |
|---|---|---|
| **[Revolution Pi](remplacement-armoire/revolution-pi.md)** | Un contrôleur industriel Linux, des modules d'entrées-sorties, des relais d'interface | environ 5 350 € HT |
| **[Arduino Opta](remplacement-armoire/arduino-opta.md)** | Quatre automates Opta répartis, avec extensions | environ 5 500 € HT |
| **[Raspberry Pi et Ethernet](remplacement-armoire/raspberry-pi-ethernet.md)** | Refonte maison : quatre cartes nœuds Pico 2 en Ethernet, un Pi de gestion | environ 3 090 € HT |

Les trois études partagent le même câblage de migration (répartiteur 230 V, jonctions des nappes, plan de bornage) et la même méthode : prix relevés en octobre 2026, simulation 3D indicative, implantation à confirmer au relevé de P0.
