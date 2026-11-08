# Configuration UniFi de la gateway (sonnette)

La fonction [Sonnette UniFi](../utilisation/sonnette-unifi.md) s'appuie sur le client UniFi Protect de la gateway CM5. Cette page décrit la configuration à déployer et le dépannage.

## Configuration UniFi

Le backend lit le bloc `unifi:` de son fichier de configuration :

```yaml
unifi:
  enabled: true
  base_url: "https://console-unifi.example.org"
  api_key: "<clé d'API, fournie par le déploiement chiffré>"
```

- `enabled` : `false` par défaut. Sans UniFi activé, la sonnette est indisponible et le reste de la gateway n'est pas touché.
- `base_url` : adresse de la console UniFi Protect, joignable depuis la CM5.
- `api_key` : clé d'API de la console. Elle reste sur la gateway : le portail ne la voit jamais, et elle n'est jamais journalisée.
- `username` et `password` : méthode de connexion de repli, si la console n'accepte pas la clé d'API.

Le déploiement (Ansible) range l'adresse et la clé dans les secrets chiffrés (SOPS), jamais en clair dans un dépôt.

!!! warning "Recréer le conteneur"
    Activer UniFi pour la première fois change la configuration du conteneur backend : il faut le **recréer**, un simple `docker restart` ne suffit pas.

## Section `doorbell` du fichier des noms

Les réglages de la sonnette sont dans le fichier `light-names.json`, dans une section de plus, à côté de `lights`, `shutters` et des dispositions. Voir [Fichier des noms de la gateway](noms-lumieres-gateway.md#section-doorbell). Aucune nouvelle clé de configuration ni aucun nouveau montage.

## Dépannage

### Erreur 503 `doorbell_unavailable`

La gateway renvoie `{"error":"doorbell_unavailable"}` quand la console est injoignable ou quand UniFi est désactivé. À vérifier dans l'ordre :

1. `unifi.enabled` vaut `true` dans la configuration rendue, et le conteneur a été recréé ;
2. l'adresse `base_url` répond depuis la CM5 (réseau, certificat) ;
3. la clé d'API est valide et autorisée sur la caméra de la sonnette ;
4. la caméra choisie existe encore sur la console.

La gateway se reconnecte seule, avec une attente de 1 à 60 secondes. Pendant ce temps, `available` vaut faux dans l'état et aucune fenêtre ne s'ouvre.

### Erreur 503 `names_unavailable`

Les réglages ne peuvent pas être lus ou écrits : même cause et mêmes vérifications que pour les noms, voir [le dépannage du fichier des noms](noms-lumieres-gateway.md#depannage-erreur-503-names_unavailable).

### Erreurs de réglage

| Erreur | Cause |
| --- | --- |
| `unknown_light` | une lumière choisie n'existe pas dans le catalogue |
| `unknown_camera` | la caméra choisie n'existe pas sur la console |
| `invalid_blinks` | nombre de clignotements hors limites |
