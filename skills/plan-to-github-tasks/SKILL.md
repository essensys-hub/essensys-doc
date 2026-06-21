---
name: plan-to-github-tasks
description: Transforme un plan structuré en tâches GitHub Projects avec prompts autonomes pour agents IA. Gère les dépendances inter-tâches. Utiliser quand l'utilisateur demande de créer des issues depuis un plan, d'organiser un projet GitHub, ou de préparer des tâches pour délégation à des agents.
---

# Plan vers GitHub Tasks

Transforme un plan de développement en tâches GitHub Projects autonomes avec contexte complet pour exécution par agents IA.

## Prérequis

```bash
gh auth login --scopes "project"
```

## Workflow

### Étape 1: Analyser le plan source

Identifier dans le plan :
- Les tâches principales (features, fixes, refactors)
- Les sous-tâches pour chaque tâche
- Les dépendances explicites et implicites
- Le contexte technique nécessaire

### Étape 2: Structurer les tâches

Pour chaque tâche, créer une structure :

```yaml
task:
  id: "TASK-001"
  title: "Titre concis de la tâche"
  depends_on: ["TASK-000"]  # IDs des prérequis
  blocks: ["TASK-002"]       # IDs des tâches bloquées
  prompt: |
    ## Contexte
    [Description du contexte projet et technique]
    
    ## Objectif
    [Ce que la tâche doit accomplir]
    
    ## Fichiers concernés
    - `path/to/file1.ts` - [raison]
    - `path/to/file2.ts` - [raison]
    
    ## Contraintes
    - [Contrainte technique 1]
    - [Contrainte technique 2]
    
    ## Critères de succès
    - [ ] Critère 1
    - [ ] Critère 2
    
    ## Dépendances
    - Requiert: TASK-000 (description)
    - Bloque: TASK-002 (description)
```

### Étape 3: Configurer GitHub Project

1. **Obtenir l'ID du projet** :

```bash
gh api graphql -f query='
  query($user: String!) {
    user(login: $user) {
      projectsV2(first: 20) {
        nodes { id title number }
      }
    }
  }' -f user="USERNAME"
```

2. **Créer un champ personnalisé "Dependencies"** (optionnel, via l'UI GitHub)

3. **Récupérer les IDs des champs** :

```bash
gh api graphql -f query='
  query($id: ID!) {
    node(id: $id) {
      ... on ProjectV2 {
        fields(first: 20) {
          nodes {
            ... on ProjectV2FieldCommon { id name }
          }
        }
      }
    }
  }' -f id="PROJECT_NODE_ID"
```

### Étape 4: Créer les tâches

Pour chaque tâche, créer un draft issue avec le prompt complet :

```bash
gh api graphql -f query='
  mutation($projectId: ID!, $title: String!, $body: String!) {
    addProjectV2DraftIssue(input: {
      projectId: $projectId
      title: $title
      body: $body
    }) {
      projectItem { id }
    }
  }' -f projectId="PROJECT_ID" \
     -f title="[TASK-001] Titre de la tâche" \
     -f body="$TASK_BODY"
```

## Format du prompt autonome

Chaque prompt doit permettre à un agent de travailler **sans contexte additionnel** :

```markdown
# [TASK-ID] Titre de la tâche

## Contexte global
Brève description du projet et de l'architecture concernée.

## Objectif de cette tâche
Description précise de ce qui doit être accompli.

## Contexte technique
- Stack: [technologies utilisées]
- Patterns: [patterns architecturaux]
- Conventions: [conventions de code]

## Fichiers à modifier
| Fichier | Action | Raison |
|---------|--------|--------|
| `src/module/file.ts` | Modifier | Ajouter fonction X |
| `tests/file.test.ts` | Créer | Tests unitaires |

## Implémentation suggérée
[Instructions étape par étape ou pseudocode]

## Dépendances entre tâches
### Prérequis (doit être complété avant)
- **TASK-000**: [Description] - Fournit [ce que cette tâche apporte]

### Bloque (attend cette tâche)
- **TASK-002**: [Description] - A besoin de [ce que cette tâche produit]

## Critères d'acceptation
- [ ] Tests passent
- [ ] Lint clean
- [ ] Documentation mise à jour
- [ ] Review demandée

## Commandes de validation
\`\`\`bash
# Build
npm run build

# Tests
npm run test -- --grep "feature"

# Lint
npm run lint
\`\`\`
```

## Gestion des dépendances

### Convention de nommage

Préfixer les titres avec l'ID : `[TASK-001] Titre`

### Ordre de création

Créer les tâches dans l'ordre topologique (dépendances d'abord).

### Marquage des dépendances

Dans le body de chaque tâche, inclure une section structurée :

```markdown
---
dependencies:
  requires: [TASK-000, TASK-001]
  blocks: [TASK-003, TASK-004]
---
```

### Mise à jour du statut

Quand une tâche est complétée, mettre à jour les tâches dépendantes :

```bash
gh api graphql -f query='
  mutation($projectId: ID!, $itemId: ID!, $fieldId: ID!, $value: String!) {
    updateProjectV2ItemFieldValue(input: {
      projectId: $projectId
      itemId: $itemId
      fieldId: $fieldId
      value: { text: $value }
    }) {
      projectV2Item { id }
    }
  }' -f projectId="PROJECT_ID" \
     -f itemId="ITEM_ID" \
     -f fieldId="STATUS_FIELD_ID" \
     -f value="Ready"
```

## Script d'automatisation

Voir [scripts/create_tasks.py](scripts/create_tasks.py) pour automatiser la création.

Usage :
```bash
python scripts/create_tasks.py plan.md --project "Mon Projet" --owner "username"
```

## Checklist de création

```
- [ ] Plan analysé et tâches identifiées
- [ ] Dépendances cartographiées
- [ ] Prompts autonomes rédigés pour chaque tâche
- [ ] Ordre topologique déterminé
- [ ] Project GitHub créé/identifié
- [ ] Tâches créées dans l'ordre
- [ ] Dépendances documentées dans chaque tâche
```
