---
title: "Sonnette UniFi"
description: "Voir la vidéo de la sonnette UniFi dans le portail local, faire clignoter des lumières choisies, limiter la sonnette à des plages horaires et recevoir une notification sur Android ou iPhone, sans rien changer à l'armoire."
---

# Sonnette UniFi

Quand quelqu'un appuie sur la sonnette UniFi, le portail local de la gateway CM5 affiche une fenêtre **« Quelqu'un sonne »** avec l'image de la caméra, et peut **faire clignoter des lumières** que vous avez choisies. Les lumières choisies finissent **allumées**.

Le clignotement et la vidéo sont locaux : ils ne passent pas par le cloud et ne sont pas synchronisés. Les [notifications sur téléphone](#notifications-sur-telephone) sont la seule partie qui passe par le cloud. Elle est jumelle de [Masquer et ordonner les lumières et les volets](masquer-ordonner-objets.md) pour le stockage des réglages et pour l'affichage des noms.

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

## Plages horaires

Par défaut, la sonnette est active **à toute heure**. Dans l'écran **Sonnette**, la section **Plages horaires** permet de choisir quand elle réagit (par exemple pas la nuit).

- **Mode** : *Toujours actif* (la grille est ignorée) ou *Personnalisé*.
- **Grille 7 × 24** : une case par jour de la semaine (lundi en premier) et par heure. Une case active signifie que la sonnette réagit pendant cette heure locale. Cliquez ou faites glisser pour cocher plusieurs cases.
- **Présélections** : des modèles de grille pour partir d'une base, que vous ajustez ensuite case par case.
- **Fuseau horaire** : réglable (`Europe/Paris` par défaut). L'éditeur affiche l'heure locale actuelle dans ce fuseau et indique si la sonnette est **dans la plage maintenant**. Un fuseau faux décale toutes les plages. Le changement d'heure est géré automatiquement.

!!! note "Grille entièrement vide"
    En mode *Personnalisé*, une grille sans aucune case active est valide : la sonnette ne réagit alors jamais.

**Hors plage**, un appui ne fait ni **clignoter** les lumières ni **envoyer de notification**. En revanche, la **vidéo locale reste affichée** dans le portail : quelqu'un à la maison veut voir qui sonne. Le bouton **Essayer** ignore la plage.

## Notifications sur téléphone

Dans la plage, la gateway prévient le cloud, qui envoie une notification **« Quelqu'un sonne »** sur les téléphones concernés, même hors du Wi-Fi de la maison. Le message ne contient ni image ni nom d'armoire. Toucher la notification ouvre l'app sur l'écran d'accueil.

- **Android et iPhone** : les deux apps proposent la notification.
- **Option « Sonnette »** : elle apparaît dans les réglages de l'app **seulement si une gateway est liée** à votre compte. L'interrupteur **« Me prévenir quand quelqu'un sonne »** est **désactivé par défaut** : chaque téléphone doit l'activer lui-même.
- **Permission de notification** : à l'activation, le système demande l'autorisation d'afficher des notifications (Android 13 et plus, iPhone). Si vous la refusez, l'interrupteur revient à zéro et l'app renvoie aux réglages du système, où vous pouvez l'accorder.
- **Déconnexion** : se déconnecter de l'app supprime ce téléphone des appareils notifiés.
- **Sonnette à activer sur la gateway** : l'option apparaît dès qu'une gateway est liée, mais la notification n'arrive que si la sonnette est activée sur la gateway (voir plus haut) et si l'appui tombe dans la plage.

Le service d'envoi (Firebase pour Android, Apple pour iPhone) est installé par l'exploitant, voir [Notifications push de la sonnette](../install/sonnette-notifications-push.md). Tant qu'il n'est pas installé, aucune notification n'est envoyée, sans que la gateway ni la sonnette locale en souffrent.

## Présence de la gateway

Le portail cloud et les apps indiquent l'état de la gateway liée :

| Affichage | Signification |
| --- | --- |
| **Gateway en ligne** | la gateway a donné de ses nouvelles récemment (moins de 2 minutes) |
| **Gateway hors ligne** | elle est liée mais ne répond plus |
| **Aucune gateway liée** | aucune gateway n'est liée à votre compte : l'option « Sonnette » des apps n'est pas proposée |

## Essayer

Le bouton **Essayer** simule une pression sur la sonnette : la fenêtre s'affiche et les lumières clignotent. Attention, l'essai agit sur les vraies lumières de l'armoire, qui finissent allumées. Un essai à sec (mode de test, sans armoire) ne commande aucune lumière et ne bloque pas une vraie sonnerie qui suivrait.

## Ce qui se passe quand on sonne

- La fenêtre « Quelqu'un sonne » s'ouvre sur **toutes les pages** du portail, pendant 60 secondes. Vous pouvez la fermer ; elle ne se rouvre pas pour la même sonnerie, mais s'ouvre à la sonnerie suivante.
- Chaque lumière choisie est éteinte puis allumée en alternance, le nombre de fois choisi (de 1 à 10), et termine **allumée**. Les autres lumières et les volets ne sont pas touchés.
- Une seule séquence de clignotement à la fois. Une nouvelle pression dans les 30 secondes qui suivent le début d'une séquence réaffiche la vidéo mais ne relance pas le clignotement.
- Si vous commandez vous-même une lumière pendant le clignotement, elle sort de la séquence : votre ordre n'est pas écrasé.
- Une pression pendant une séquence met à jour la sonnerie en cours sans relancer de clignotement.

## Limites

- **Pas de garantie de livraison** des notifications : un téléphone éteint, sans réseau ou en économie d'énergie peut recevoir la notification en retard, ou pas du tout. La notification ne remplace pas la sonnette physique.
- Un appui n'est **jamais perdu** côté gateway : le clignotement et la vidéo locale ne dépendent pas du cloud. Si le cloud est injoignable, la gateway réessaie brièvement puis abandonne après 60 secondes : la notification peut alors être **absente** ou **en retard**, jamais le clignotement.
- Deux notifications du même appui sont **fusionnées** en une seule sur le téléphone. Un second appui moins de 30 secondes après le premier ne déclenche pas de nouvelle séquence (voir plus haut).
- **Wi-Fi ou hors Wi-Fi** : la notification arrive par Internet, donc aussi hors de la maison. La vidéo, elle, n'est affichée que dans le portail local, sur le réseau de la maison ; les apps n'affichent pas la vidéo.
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
