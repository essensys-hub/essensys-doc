# Reference — Execute GitHub Project

Queries GraphQL et commandes pour l'execution des taches.

## 1. Lire les items du projet

```bash
gh api graphql -f query='
  query($pid: ID!) {
    node(id: $pid) {
      ... on ProjectV2 {
        title
        items(first: 50) {
          nodes {
            id
            content {
              ... on DraftIssue { title body }
              ... on Issue { title body number url }
            }
          }
        }
      }
    }
  }' -f pid="PROJECT_ID"
```

## 2. Recuperer les champs du projet (Status field)

```bash
gh api graphql -f query='
  query($pid: ID!) {
    node(id: $pid) {
      ... on ProjectV2 {
        fields(first: 20) {
          nodes {
            ... on ProjectV2SingleSelectField {
              id
              name
              options { id name }
            }
            ... on ProjectV2FieldCommon { id name }
          }
        }
      }
    }
  }' -f pid="PROJECT_ID"
```

Retourne les champs dont `Status` avec ses options (`Todo`, `In Progress`, `Done`).

Conserver :
- `STATUS_FIELD_ID` : l'ID du champ Status
- `OPTION_IN_PROGRESS` : l'ID de l'option "In Progress"
- `OPTION_DONE` : l'ID de l'option "Done"

## 3. Convertir un draft en issue

Les drafts n'acceptent pas de commentaires. Il faut :

### 3.1 Creer l'issue dans le repo

```bash
ISSUE_URL=$(gh issue create \
  --repo OWNER/REPO \
  --title "[TASK-001] Titre" \
  --body "$BODY" \
  2>&1 | tail -1)

ISSUE_NUMBER=$(echo "$ISSUE_URL" | grep -o '[0-9]*$')
```

### 3.2 Ajouter l'issue au projet

```bash
# Obtenir l'ID node de l'issue
ISSUE_NODE_ID=$(gh api graphql -f query='
  query($owner: String!, $repo: String!, $number: Int!) {
    repository(owner: $owner, name: $repo) {
      issue(number: $number) { id }
    }
  }' -f owner="OWNER" -f repo="REPO" -f number="$ISSUE_NUMBER" \
  --jq '.data.repository.issue.id')

# Ajouter au projet
NEW_ITEM_ID=$(gh api graphql -f query='
  mutation($pid: ID!, $contentId: ID!) {
    addProjectV2ItemById(input: {
      projectId: $pid
      contentId: $contentId
    }) {
      item { id }
    }
  }' -f pid="PROJECT_ID" -f contentId="$ISSUE_NODE_ID" \
  --jq '.data.addProjectV2ItemById.item.id')
```

### 3.3 Supprimer le draft du projet

```bash
gh api graphql -f query='
  mutation($pid: ID!, $itemId: ID!) {
    deleteProjectV2Item(input: {
      projectId: $pid
      itemId: $itemId
    }) {
      deletedItemId
    }
  }' -f pid="PROJECT_ID" -f itemId="DRAFT_ITEM_ID"
```

## 4. Mettre a jour le statut d'un item

```bash
gh api graphql -f query='
  mutation($pid: ID!, $itemId: ID!, $fieldId: ID!, $optionId: String!) {
    updateProjectV2ItemFieldValue(input: {
      projectId: $pid
      itemId: $itemId
      fieldId: $fieldId
      value: { singleSelectOptionId: $optionId }
    }) {
      projectV2Item { id }
    }
  }' \
  -f pid="PROJECT_ID" \
  -f itemId="ITEM_ID" \
  -f fieldId="STATUS_FIELD_ID" \
  -f optionId="OPTION_ID"
```

**OPTION_ID** :
- `In Progress` → utiliser l'ID de cette option (recupere en section 2)
- `Done` → utiliser l'ID de cette option

## 5. Ajouter un commentaire sur une issue

```bash
gh issue comment ISSUE_NUMBER --repo OWNER/REPO --body "MESSAGE"
```

Ou via GraphQL (si le body est long) :

```bash
gh api graphql -f query='
  mutation($subjectId: ID!, $body: String!) {
    addComment(input: {
      subjectId: $subjectId
      body: $body
    }) {
      commentEdge { node { id url } }
    }
  }' -f subjectId="ISSUE_NODE_ID" -f body="$BODY"
```

## 6. Lister les commits lies a une issue

```bash
git log --oneline --all --grep="refs #${ISSUE_NUMBER}"
```

## 7. Fermer une issue

```bash
gh issue close ISSUE_NUMBER --repo OWNER/REPO --comment "Completed by agent"
```

## 8. Templates de commentaires

### Demarrage

```markdown
## 🚀 Agent started

| Field | Value |
|-------|-------|
| **Task** | TASK-XXX |
| **Issue** | #NUMBER |
| **Started** | YYYY-MM-DD HH:MM UTC |
| **Dependencies** | TASK-001 ✅, TASK-002 ✅ |

---
_Automated by execute-github-project_
```

### Progression

```markdown
### 📋 Progress update

- **Step**: Description de l'etape
- **Files modified**: `file1.c`, `file2.h`
- **Status**: En cours / Fait
- **Notes**: Details pertinents

---
_Automated by execute-github-project_
```

### Succes

```markdown
## ✅ Task completed

| Field | Value |
|-------|-------|
| **Finished** | YYYY-MM-DD HH:MM UTC |
| **Duration** | X min |
| **Commits** | N commits |

### Commits
```
abc1234 feat(scope): description refs #N
def5678 test(scope): add tests refs #N
```

### Files changed
- `path/to/file1.c` (created)
- `path/to/file2.h` (modified)

### Summary
Description du travail accompli.

---
_Automated by execute-github-project_
```

### Echec

```markdown
## ❌ Task failed

| Field | Value |
|-------|-------|
| **Failed at** | YYYY-MM-DD HH:MM UTC |
| **Duration** | X min |
| **Last step** | Description |

### Error
```
Error message or stack trace
```

### Partial commits
```
abc1234 partial work refs #N
```

### Debug info
Informations pertinentes pour le debug.

### Suggested fix
Suggestion de correction si possible.

---
_Automated by execute-github-project_
```

## 9. Template prompt sub-agent

```
Tu executes la tache #{ISSUE_NUMBER} du repo {OWNER}/{REPO}.
Working directory : {WORKSPACE_PATH}

## Instructions de tracabilite OBLIGATOIRES

### Commits
Chaque commit DOIT inclure "refs #{ISSUE_NUMBER}" dans le message.
Format : type(scope): description refs #{ISSUE_NUMBER}
Exemples :
- feat(bp): add CRC-16 module refs #{ISSUE_NUMBER}
- fix(ba): correct I2C address refs #{ISSUE_NUMBER}
- test: add MD5 test vectors refs #{ISSUE_NUMBER}

### Logs de progression
A chaque etape significative, ajouter un commentaire :
gh issue comment {ISSUE_NUMBER} --repo {OWNER}/{REPO} --body "### 📋 Progress\n- Step: [etape]\n- Files: [fichiers]\n- Status: [en cours|fait]"

### Erreurs
Si une erreur survient :
gh issue comment {ISSUE_NUMBER} --repo {OWNER}/{REPO} --body "### ⚠️ Error\n\`\`\`\n[erreur]\n\`\`\`\nAction: [tentative]"

### IMPORTANT
- Ne PAS fermer l'issue
- Ne PAS modifier le statut du projet
- Le workflow principal gere le statut et la fermeture

## Tache

{ISSUE_BODY}
```

## 10. Ordre topologique — algorithme

Pour resoudre les dependances, utiliser l'algorithme de Kahn :

```
1. Calculer in_degree[t] = nombre de requires non-Done pour chaque tache t
2. file = [t for t if in_degree[t] == 0]  # taches pretes
3. while file:
     t = file.pop()
     executer(t)
     for d in t.blocks:
       in_degree[d] -= 1
       if in_degree[d] == 0:
         file.append(d)
4. Si des taches restent avec in_degree > 0 → cycle de dependances
```

En pratique dans le workflow Cursor, le resolution se fait manuellement :
1. Lire les `requires` de chaque tache
2. Les taches sans requires → lot 1 (parallele)
3. Apres lot 1, les taches dont tous les requires sont Done → lot 2
4. Etc.
