---
title: "Renommer un volet ou un store"
description: "Donner un nom personnalisé à un volet ou à un store (par exemple Volet baie vitrée à la place de Volet 1 Salon) depuis le portail ou l'application, et revenir au nom d'origine."
---

# Renommer un volet ou un store

Chaque volet et chaque store de l'armoire porte un nom d'origine (« Volet 1 Salon », « Volet Petite Chambre 3 », « Store (banne) »…). Vous pouvez lui donner le nom qui correspond à votre logement, par exemple « Volet baie vitrée » à la place de « Volet 1 Salon ». Le nouveau nom s'affiche partout : portail, applications Android et iPhone, confirmations d'ouverture et de fermeture, écran « Temps de course ».

Cette fonction est la jumelle de [Renommer une lumière](renommer-lumiere.md) : mêmes droits, mêmes règles, même synchronisation.

!!! info "Réservé à l'administrateur"
    Seul l'administrateur de l'armoire peut renommer un volet. Un utilisateur simple voit les noms, mais pas le champ de modification. Le contrôle est aussi fait par le serveur : masquer le champ n'est pas la protection.

## Les 16 volets et stores

Les 14 volets et les 2 éléments spéciaux (`Volet "Store"` et `Store (banne)`) sont tous renommables. Le nom d'origine est affiché tant qu'aucun nom n'est défini.

## Où renommer

Ouvrez la **fiche du volet**, puis modifiez son nom. Le réglage est disponible dans :

- le portail cloud ;
- le portail local (celui de la gateway) ;
- l'application Android ;
- l'application iPhone.

## Les règles du nom

| Règle | Détail |
| --- | --- |
| Longueur | De 1 à 40 caractères, espaces de début et de fin retirés |
| Caractères interdits | Les caractères de contrôle et les balises `<` et `>` |
| Guillemets | Permis (le nom d'origine de `Volet "Store"` en contient) |
| Affichage | Le nom est toujours affiché comme du texte brut |

Un nom hors règle est refusé avec un message d'erreur et le volet garde son nom précédent.

## Revenir au nom d'origine

Le bouton **Nom d'origine** (ou un nom laissé vide) supprime le nom personnalisé : le volet retrouve son nom d'usine. La remise à zéro se propage comme un renommage.

## Où le nom apparaît

- la liste des commandes de l'écran Volets ;
- les confirmations et messages de dernière action (« Ouvert », « Fermé ») ;
- l'écran **Temps de course**, où chaque volet est présenté sous son nom personnalisé. Un nom de 40 caractères doit tenir sur la ligne, éventuellement sur deux lignes.

Les titres génériques (« Volets », « Volets & stores ») et les boutons « Tout ouvrir » et « Tout fermer » ne changent pas.

## Synchronisation entre le cloud et la gateway

Le nom est conservé dans le cloud et dans la gateway de l'armoire.

- Un nom saisi dans le portail cloud arrive sur la gateway en moins d'une minute.
- Un nom saisi sur le portail local, ou dans une application en mode local, arrive dans le cloud en moins d'une minute.
- Sans connexion Internet, la gateway garde ses noms et fonctionne normalement ; la synchronisation reprend au retour de la connexion.
- Si le même volet est renommé des deux côtés, **la modification la plus récente l'emporte**, volet par volet.
- Les noms des volets et ceux des lumières sont synchronisés séparément : l'échec de l'un ne bloque pas l'autre.

## Limites

- Un nom par volet : renommer un volet ne renomme pas la pièce, ni les lumières.
- Une armoire par compte : un administrateur qui gère plusieurs armoires renomme celle qui est liée à son compte (le sélecteur d'armoire est prévu dans un ticket suivant).
- Renommer ne modifie rien dans l'armoire : seul l'affichage change. Les temps de course ne sont pas touchés.

## Si ça ne marche pas

- Le champ n'apparaît pas : le compte n'est pas administrateur de l'armoire.
- Le nom est refusé : vérifiez qu'il fait de 1 à 40 caractères et ne contient ni `<` ni `>`.
- Une erreur « noms indisponibles » sur le portail local : le stockage des noms de la gateway est absent, voir [Fichier des noms de la gateway](../install/noms-lumieres-gateway.md).
