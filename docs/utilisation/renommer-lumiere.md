---
title: "Renommer une lumière"
description: "Donner un nom personnalisé à une lumière (par exemple WC 3 à la place de Dressing) depuis le portail ou l'application, et revenir au nom d'origine."
---

# Renommer une lumière

Chaque lumière de l'armoire porte un nom d'origine (« Dressing », « Salon », « Grande Chambre (chevet 1) »…). Vous pouvez lui donner le nom qui correspond à votre logement, par exemple « WC 3 » à la place de « Dressing ». Le nouveau nom s'affiche partout : portail, applications Android et iPhone, menu des temporisations.

!!! info "Réservé à l'administrateur"
    Seul l'administrateur de l'armoire peut renommer une lumière. Un utilisateur simple voit les noms, mais pas le champ de modification. Le contrôle est aussi fait par le serveur : masquer le champ n'est pas la protection.

## Où renommer

Ouvrez la **fiche de la lumière**, puis modifiez son nom. Le réglage est disponible dans :

- le portail cloud ;
- le portail local (celui de la gateway) ;
- l'application Android ;
- l'application iPhone.

## Les règles du nom

| Règle | Détail |
| --- | --- |
| Longueur | De 1 à 40 caractères, espaces de début et de fin retirés |
| Caractères interdits | Les caractères de contrôle et les balises `<` et `>` |
| Affichage | Le nom est toujours affiché comme du texte brut |

Un nom hors règle est refusé avec un message d'erreur et la lumière garde son nom précédent.

## Revenir au nom d'origine

Le bouton **Nom d'origine** (ou un nom laissé vide) supprime le nom personnalisé : la lumière retrouve son nom d'usine. La remise à zéro se propage comme un renommage.

## Synchronisation entre le cloud et la gateway

Le nom est conservé dans le cloud et dans la gateway de l'armoire.

- Un nom saisi dans le portail cloud arrive sur la gateway en moins d'une minute.
- Un nom saisi sur le portail local, ou dans une application en mode local, arrive dans le cloud en moins d'une minute.
- Sans connexion Internet, la gateway garde ses noms et fonctionne normalement ; la synchronisation reprend au retour de la connexion.
- Si la même lumière est renommée des deux côtés, **la modification la plus récente l'emporte**, lumière par lumière.

## Limites

- Seules les **lumières** se renomment : ni les volets, ni les pièces.
- Une armoire par compte : un administrateur qui gère plusieurs armoires renomme celle qui est liée à son compte (le sélecteur d'armoire est prévu dans un ticket suivant).
- Renommer ne modifie rien dans l'armoire : seul l'affichage change.
- Le menu des temporisations (extinction automatique des lumières) s'affiche avec le nom personnalisé.

## Si ça ne marche pas

- Le champ n'apparaît pas : le compte n'est pas administrateur de l'armoire.
- Le nom est refusé : vérifiez qu'il fait de 1 à 40 caractères et ne contient ni `<` ni `>`.
- Une erreur « noms indisponibles » sur le portail local : le stockage des noms de la gateway est absent, voir [Fichier des noms de la gateway](../install/noms-lumieres-gateway.md).
