---
title: "Régler l'extinction automatique des lumières"
description: "Régler le délai d'extinction automatique de six lumières (Dressing, WC 1, WC 2, Service, Annexe 1, Annexe 2) depuis le portail ou l'application, sans passer devant l'armoire."
---

# Régler l'extinction automatique des lumières

Six lumières de l'armoire peuvent s'éteindre toute seules après un délai. Ce délai se règle depuis le portail (cloud ou local) et depuis les applications Android et iPhone, sans être devant l'armoire.

!!! info "Réservé à l'administrateur"
    Le réglage est proposé seulement à l'administrateur de l'armoire. Un utilisateur simple ne voit ni le menu « Temporisations » ni le réglage dans la fiche d'une lumière. Le contrôle est aussi fait par le serveur : masquer le menu n'est pas la protection.

## Les six lumières

| Lumière | Zone |
| --- | --- |
| Dressing | Pièces de vie |
| WC 1 | Pièces d'eau |
| WC 2 | Pièces d'eau |
| Service (buanderie) | Pièces d'eau |
| Annexe 1 | Pièces d'eau |
| Annexe 2 | Pièces d'eau |

Les autres lumières n'ont pas de délai réglable. Les numéros de case de la table d'échange correspondants (521, 555, 556, 557, 561, 562) sont décrits dans la page [Table d'échange](../architecture/exchange-table.md).

## Deux façons de régler

1. **Le menu « Temporisations »** liste les six lumières avec leur délai actuel. Choisissez une lumière et réglez-la.
2. **La fiche de la lumière** : ouvrez la lumière concernée, le même réglage s'y trouve. La valeur affichée est la même que dans le menu.

## Les valeurs

| Choix | Effet |
| --- | --- |
| 15 min, 30 min, 1 h | La lumière s'éteint après ce délai |
| Jamais | La lumière reste allumée (valeur 0) |
| Autre | Une valeur libre de 1 à 255 minutes (par exemple 7 min) |

Une valeur hors de 1 à 255 est refusée. Si le délai n'a jamais été lu depuis l'armoire, il s'affiche « inconnu » et non « jamais ». Après un envoi, la valeur est relue quelques secondes plus tard pour confirmer qu'elle est bien prise en compte.

Le boîtier de la lumière compte un peu plus court que l'horloge : il applique `minutes × 60 × 0,994` secondes, soit environ 894 secondes pour 15 minutes.

## Limite de l'écran de l'armoire

L'écran tactile de l'armoire propose uniquement 15 min, 30 min, 1 h et Jamais. Une valeur libre comme 7 min est acceptée par la lumière mais n'est cochée sur aucune case de l'écran. Si vous validez l'écran de réglage pour cette lumière, il peut remplacer la valeur libre par l'un de ses quatre choix. Ce comportement est en cours de vérification sur un banc de test ; en attendant, préférez les quatre valeurs de l'écran si quelqu'un règle aussi l'armoire à la main.

## Si ça ne marche pas

- Le menu n'apparaît pas : le compte n'est pas administrateur de l'armoire.
- Le réglage est refusé : vérifiez que la valeur est entre 0 et 255 et que l'armoire est en ligne.
- Pour les clés de la table d'échange et le réglage par injection manuelle, voir la [documentation de maintenance du Raspberry Pi](https://github.com/essensys-hub/essensys-raspberry-install/blob/V.1.3.0/docs/maintenance/debug.md).
