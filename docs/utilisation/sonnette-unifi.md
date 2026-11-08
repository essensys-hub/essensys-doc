---
title: "Sonnette UniFi"
description: "Voir la vidéo de la sonnette UniFi dans le portail local quand quelqu'un sonne, et faire clignoter des lumières choisies, sans rien changer à l'armoire."
---

# Sonnette UniFi

Quand quelqu'un appuie sur la sonnette UniFi, le portail local de la gateway CM5 affiche une fenêtre **« Quelqu'un sonne »** avec l'image de la caméra, et peut **faire clignoter des lumières** que vous avez choisies. Les lumières choisies finissent **allumées**.

La fonction est locale : elle ne passe pas par le cloud et n'est pas synchronisée. Elle est jumelle de [Masquer et ordonner les lumières et les volets](masquer-ordonner-objets.md) pour le stockage des réglages et pour l'affichage des noms.

## Prérequis

- Une console UniFi Protect avec une caméra sonnette, joignable depuis la gateway CM5.
- UniFi activé dans la configuration de la gateway (adresse de la console et clé d'API), voir [Configuration UniFi de la gateway](../install/sonnette-unifi-gateway.md).
- Le fichier des noms de la gateway, qui porte aussi les réglages, voir [Fichier des noms de la gateway](../install/noms-lumieres-gateway.md).

## Activer et régler

!!! info "Réservé à l'administrateur"
    Seul l'administrateur de l'armoire voit l'écran **Sonnette** du portail local (tous les utilisateurs si l'IAM LAN est désactivé). Le contrôle est aussi fait par le serveur : masquer l'écran n'est pas la protection.

Dans l'écran **Sonnette** :

1. Activez la fonction (elle est **désactivée par défaut**).
2. Choisissez la **caméra** de la sonnette.
3. Choisissez les **lumières** à faire clignoter. La liste affiche les noms personnalisés et ne propose pas les lumières masquées. Par défaut, aucune lumière n'est choisie : seule la vidéo s'affiche.
4. Choisissez le **nombre de clignotements** (5 par défaut).
5. Appuyez sur **Enregistrer**.

## Essayer

Le bouton **Essayer** simule une pression sur la sonnette : la fenêtre s'affiche et les lumières clignotent. Attention, l'essai agit sur les vraies lumières de l'armoire, qui finissent allumées. Un essai à sec (mode de test, sans armoire) ne commande aucune lumière et ne bloque pas une vraie sonnerie qui suivrait.

## Ce qui se passe quand on sonne

- La fenêtre « Quelqu'un sonne » s'ouvre sur **toutes les pages** du portail, pendant 60 secondes. Vous pouvez la fermer ; elle ne se rouvre pas pour la même sonnerie, mais s'ouvre à la sonnerie suivante.
- Chaque lumière choisie est éteinte puis allumée en alternance, le nombre de fois choisi (de 1 à 10), et termine **allumée**. Les autres lumières et les volets ne sont pas touchés.
- Une seule séquence de clignotement à la fois. Une nouvelle pression dans les 30 secondes qui suivent le début d'une séquence réaffiche la vidéo mais ne relance pas le clignotement.
- Si vous commandez vous-même une lumière pendant le clignotement, elle sort de la séquence : votre ordre n'est pas écrasé.
- Une pression pendant une séquence met à jour la sonnerie en cours sans relancer de clignotement.

## Limites

- La vidéo est une **suite d'instantanés, environ une image par seconde**, pas une vidéo fluide. Elle n'a pas de son.
- La gateway ne peut pas lire l'état réel des lumières : elle ne peut donc pas le restaurer. Une lumière éteinte avant la sonnerie reste **allumée** après le clignotement. C'est une limite assumée.
- Le clignotement est **lent** (au moins 2 secondes par phase), parce que l'armoire lit les ordres à son rythme.
- La fonction suit une seule caméra de sonnette.
- Si la console UniFi est injoignable ou UniFi est désactivé, aucune fenêtre ne s'ouvre et le reste de la gateway fonctionne normalement ; la gateway se reconnecte seule, avec une attente croissante (1 à 60 secondes).
- Les lumières masquées ne sont pas proposées ; une lumière choisie puis masquée ensuite est ignorée.

## Si ça ne marche pas

- L'écran **Sonnette** n'apparaît pas : le compte n'est pas administrateur.
- Erreur « sonnette indisponible » : la console UniFi est injoignable ou UniFi est désactivé, voir [Configuration UniFi de la gateway](../install/sonnette-unifi-gateway.md).
- Erreur « noms indisponibles » : le stockage de la gateway est absent, voir [Fichier des noms de la gateway](../install/noms-lumieres-gateway.md).
