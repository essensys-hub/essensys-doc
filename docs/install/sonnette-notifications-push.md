# Notifications push de la sonnette

Cette page s'adresse à l'**exploitant** du cloud Essensys. Elle décrit l'installation des deux fournisseurs de notification utilisés par la [Sonnette UniFi](../utilisation/sonnette-unifi.md) : **Firebase Cloud Messaging** (FCM, Android) et **Apple Push Notification service** (APNs, iPhone).

!!! warning "Aucun secret dans un dépôt"
    Les valeurs ci-dessous sont des **placeholders**. Les vraies valeurs vivent uniquement dans les secrets chiffrés (SOPS) du déploiement. Ne les collez jamais dans un ticket, un journal, une page ou un message.

## Principe

Le backend cloud reçoit l'appui envoyé par la gateway, puis envoie la notification aux téléphones liés qui l'ont demandée. Il lit sa configuration dans des variables d'environnement, alimentées par le déploiement (Ansible) depuis les secrets SOPS.

Les fournisseurs sont **indépendants** : on peut n'installer que l'un des deux. Un fournisseur non configuré est simplement désactivé : le cloud accepte l'appui, n'envoie rien pour cette plateforme et journalise une seule fois `push_unavailable`. La gateway ne voit jamais d'erreur.

Contenu de la notification : titre « Quelqu'un sonne », corps « Sonnette de votre maison », sans image ni nom d'armoire, en priorité haute.

## Clés SOPS attendues

| Clé SOPS | Fournisseur | Contenu |
| --- | --- | --- |
| `fcm_project_id` | FCM | identifiant du projet Firebase |
| `fcm_service_account_json` | FCM | fichier JSON du compte de service (contenu complet) |
| `apns_key_p8` | APNs | contenu de la clé d'authentification `.p8` |
| `apns_key_id` | APNs | identifiant de la clé (10 caractères) |
| `apns_team_id` | APNs | identifiant de l'équipe Apple Developer (10 caractères) |
| `apns_bundle_id` | APNs | identifiant de l'app iPhone (`bundle id`) |
| `apns_env` | APNs | `production` ou `development` |

## Installer Firebase Cloud Messaging (Android)

1. Dans la console Firebase, créez (ou choisissez) un projet. Notez son identifiant : `<fcm-project-id>`.
2. Ajoutez l'app Android au projet avec son identifiant d'application. Téléchargez le fichier de configuration (`google-services.json`) : il est fourni **à la compilation de l'app Android**, pas au cloud.
3. Dans les paramètres du projet, onglet des comptes de service, créez une clé privée au format JSON pour le compte de service autorisé à envoyer des messages (API Cloud Messaging HTTP v1).
4. Rangez l'identifiant du projet dans `fcm_project_id` et le contenu du fichier JSON dans `fcm_service_account_json`, dans les secrets SOPS. Supprimez ensuite le fichier téléchargé de votre poste.
5. Déployez (voir la section suivante).

## Installer APNs (iPhone)

1. Dans le compte Apple Developer, créez une **clé d'authentification APNs** (fichier `.p8`, téléchargeable **une seule fois**). Notez son identifiant `<apns-key-id>` et l'identifiant d'équipe `<apns-team-id>`.
2. Vérifiez l'identifiant de l'app iPhone : `<apns-bundle-id>`.
3. Choisissez l'environnement : `production` pour les builds distribués (TestFlight, App Store), `development` pour les builds de développement. Un mauvais environnement fait rejeter les jetons.
4. Rangez les cinq valeurs dans les secrets SOPS : `apns_key_p8`, `apns_key_id`, `apns_team_id`, `apns_bundle_id`, `apns_env`.
5. Déployez (voir la section suivante). L'app iPhone reçoit par APNs directement, sans SDK Firebase.

## Déployer

Les secrets sont transmis au backend cloud par le déploiement Ansible. Ordre de livraison :

1. la migration de base (table des appareils) sur la base de production, **avant** le code qui en dépend ;
2. le backend cloud avec ses variables d'environnement, puis le portail cloud ;
3. la gateway CM5 et son portail local ;
4. les apps (APK Android, build iPhone) en dernier.

Changer une variable d'environnement impose de **recréer** le conteneur backend : un simple `docker restart` ne relit pas l'environnement.

## Vérifier sans afficher de secret

Ne vérifiez jamais en affichant une valeur. Procédez ainsi :

- **Présence** : contrôlez que les clés existent dans le fichier SOPS sans les déchiffrer en clair à l'écran, par exemple en listant seulement leurs noms (`sops decrypt` filtré sur les noms de clés, ou un test de présence qui répond oui ou non).
- **Journal du backend** : après le déploiement, cherchez le message `push_unavailable`. S'il est présent, un fournisseur n'est pas configuré. Le journal ne contient jamais de jeton ni de clé ; s'il en contenait, c'est une anomalie à corriger.
- **Essai à blanc** : la route de signalement accepte l'en-tête `X-Essensys-Test-Mode: dry-run`. La réponse est `dry_run` et aucun fournisseur n'est appelé : cela valide le chemin gateway vers cloud, pas l'envoi.
- **Essai réel** : sur un **téléphone physique** (Android, iPhone) dont l'interrupteur « Sonnette » est activé, déclenchez le bouton **Essayer** du portail local avec la sonnette activée et dans la plage, et vérifiez la réception. Le simulateur iPhone ne reçoit pas d'APNs réelles.

## Faire tourner une clé

La rotation se fait **sans interruption** de la sonnette locale.

1. Créez la nouvelle clé chez le fournisseur : nouvelle clé privée JSON du compte de service (FCM), ou nouvelle clé `.p8` avec son nouvel identifiant (APNs).
2. Mettez à jour les clés SOPS correspondantes (`fcm_service_account_json`, ou `apns_key_p8` et `apns_key_id` ensemble).
3. Redéployez le backend cloud (conteneur recréé) et refaites la vérification ci-dessus.
4. **Seulement ensuite**, révoquez l'ancienne clé chez le fournisseur.
5. Détruisez les copies locales de la clé téléchargée.

En cas de fuite supposée, révoquez d'abord l'ancienne clé, puis installez la nouvelle : les notifications sont interrompues entre les deux, la sonnette locale ne l'est pas.

## Dépannage

| Symptôme | Cause probable |
| --- | --- |
| Aucune notification, `push_unavailable` au journal | fournisseur non configuré : variables absentes après le déploiement |
| Android reçoit, iPhone non | clés APNs absentes ou `apns_env` incorrect |
| iPhone reçoit, Android non | secrets FCM absents ou compte de service sans droit d'envoi |
| Un téléphone ne reçoit plus rien | jeton périmé : le cloud supprime l'appareil, il suffit de rouvrir l'app et de réactiver l'option |
| Notification en retard ou absente | pas de garantie de livraison (téléphone éteint, économie d'énergie, cloud injoignable plus de 60 secondes) |
