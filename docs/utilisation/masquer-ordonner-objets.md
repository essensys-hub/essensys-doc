---
title: "Masquer et ordonner les lumières et les volets"
description: "Désactiver les lumières, volets et stores que vous n'utilisez pas et choisir l'ordre d'affichage, depuis le portail ou l'application, puis revenir à l'ordre d'origine."
---

# Masquer et ordonner les lumières et les volets

L'armoire gère 33 lumières et 16 volets et stores, mais votre logement n'en utilise pas forcément autant. L'administrateur peut **désactiver** les objets inutilisés pour les masquer, et **changer leur ordre** d'affichage. Rien ne change dans l'armoire : seul l'affichage est modifié.

Cette fonction est la jumelle de [Renommer une lumière](renommer-lumiere.md) et de [Renommer un volet ou un store](renommer-volet.md) : mêmes droits, même synchronisation.

!!! info "Réservé à l'administrateur"
    Seul l'administrateur de l'armoire voit l'écran de gestion et son bouton d'accès. Un utilisateur simple voit le résultat (objets masqués, ordre choisi). Le contrôle est aussi fait par le serveur : masquer le bouton n'est pas la protection.

## L'écran de gestion

Il existe un écran pour les lumières et un pour les volets et stores, ouverts depuis l'écran Lumières et l'écran Volets (portail cloud, portail local, application Android, application iPhone).

L'écran liste **tous** les objets du genre, y compris les objets désactivés, dans l'ordre actuel, avec le nom affiché (le nom personnalisé s'il existe). Pour chaque objet :

- un interrupteur **Activé / Désactivé** ;
- des boutons **Monter** et **Descendre**.

Les modifications restent sur l'écran tant que vous n'avez pas appuyé sur **Enregistrer** : un seul enregistrement envoie l'ensemble. Le bouton **Ordre d'origine** remet tout actif et dans l'ordre d'usine.

## L'ordre

L'ordre ne déplace jamais un objet d'un groupe à l'autre. Monter ou descendre échange un objet avec son voisin **du même groupe** :

| Genre | Groupes |
| --- | --- |
| Lumières | Éclairage principal (21), Éclairage indirect (12) |
| Volets et stores | Volets (14), Éléments spéciaux (2) |

Les boutons Monter et Descendre sont inactifs en tête et en queue de groupe.

## Ce qu'un objet désactivé devient

Un objet désactivé est masqué **pour tous les utilisateurs** de l'armoire :

- dans les listes de commandes (lumières principales, indirectes, volets, store, éléments spéciaux) ;
- dans les boutons **Tout allumer / Tout éteindre** et **Tout ouvrir / Tout fermer** : une commande de groupe n'inclut pas les objets désactivés ;
- dans l'écran **Temporisations** (lumières) ;
- dans l'écran **Temps de course** (volets).

Aucune commande n'est envoyée pour un objet désactivé. Si un groupe n'a plus aucun objet actif, ses boutons de groupe disparaissent et le texte « Aucune lumière activée » ou « Aucun volet activé » s'affiche.

Les écrans qui n'ont pas de groupes (Temporisations, Temps de course) suivent l'ordre global, privé des objets désactivés.

## Synchronisation entre le cloud et la gateway

La disposition est conservée dans le cloud et dans la gateway de l'armoire, **en un seul document par genre** (un pour les lumières, un pour les volets).

- Une disposition enregistrée dans le portail cloud arrive sur la gateway en moins d'une minute, et inversement.
- Sans connexion Internet, la gateway garde sa disposition et fonctionne normalement ; la synchronisation reprend au retour de la connexion.
- Si la disposition est modifiée des deux côtés, **la modification la plus récente l'emporte, pour le document entier** (pas objet par objet). Les deux côtés finissent avec la même valeur.
- Les dispositions des lumières, celles des volets et les noms sont synchronisés séparément : l'échec de l'un ne bloque pas les autres.

## Limites

- Les **scénarios** et l'éditeur de scénarios gardent le catalogue complet : un objet désactivé y reste disponible.
- Une armoire par compte : un administrateur qui gère plusieurs armoires règle celle qui est liée à son compte.
- Si la lecture de la disposition est impossible (ancien serveur, réseau), tous les objets s'affichent dans l'ordre d'origine, sans message bloquant.
- Désactiver un objet ne coupe rien dans l'armoire : le matériel reste commandable par les boutons physiques.

## Si ça ne marche pas

- Le bouton de gestion n'apparaît pas : le compte n'est pas administrateur de l'armoire.
- Une erreur « noms indisponibles » sur le portail local : le stockage de la gateway est absent, voir [Fichier des noms de la gateway](../install/noms-lumieres-gateway.md).
- La disposition ne se propage pas : vérifiez que la gateway et le cloud sont à jour (le cloud se déploie en premier).
