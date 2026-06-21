---
name: execute-github-project
description: Execute les taches d'un GitHub Project V2 via des sub-agents autonomes. Gere les dependances, met a jour le statut (In Progress / Done / Failed), ajoute des logs en commentaires sur les issues, et lie les commits aux taches. Utiliser quand l'utilisateur demande d'executer, lancer, ou travailler sur les taches d'un projet GitHub.
---

# Execute GitHub Project Tasks

Execute les taches d'un GitHub Project V2 en lancant des sub-agents, avec tracabilite complete (logs, commits, statut).

## Prerequis

- `gh auth login --scopes "project"` (scope `project` + `repo`)
- Les taches du projet doivent suivre le format `[TASK-XXX] Titre` avec section `dependencies:` YAML dans le body
- Skill complementaire : [plan-to-github-tasks](../plan-to-github-tasks/SKILL.md) pour creer les taches

## Workflow principal

### Phase 1 — Preparation

1. **Identifier le projet** : obtenir le `PROJECT_ID` et le `REPO` (owner/name)
2. **Lire toutes les taches** : recuperer items du projet via GraphQL (voir [reference.md](reference.md))
3. **Convertir les drafts en issues** : les draft issues n'acceptent pas de commentaires — creer une vraie issue pour chaque draft, puis supprimer le draft du projet
4. **Recuperer le Status field ID** : necessaire pour mettre a jour le statut des items

```bash
# Lister les items du projet
gh api graphql -f query='...' -f pid="PROJECT_ID"

# Pour chaque draft issue → creer une vraie issue
gh issue create --repo OWNER/REPO --title "$TITLE" --body "$BODY"

# Ajouter l'issue au projet
gh api graphql -f query='mutation { addProjectV2ItemById(...) { ... } }'
```

Voir [reference.md](reference.md) pour les queries completes.

### Phase 2 — Resolution des dependances

Parser la section `dependencies:` YAML de chaque tache :

```yaml
---
dependencies:
  requires: [TASK-001, TASK-002]
  blocks: [TASK-004]
---
```

Construire le graphe de dependances et determiner l'ordre topologique. Les taches sans prerequis (`requires: []`) sont executables immediatement.

**Regles** :
- Une tache est **prete** quand tous ses `requires` sont au statut `Done`
- Les taches pretes **sans dependance entre elles** peuvent etre lancees en parallele (max 3-4 sub-agents simultanes)
- Si une tache echoue, ses dependants sont bloques → marquer `Blocked`

### Phase 3 — Execution des taches

Pour chaque tache prete, suivre ce cycle :

#### 3.1 — Debut de tache

```bash
# 1. Mettre le statut "In Progress" dans le projet
# (voir reference.md pour la mutation GraphQL)

# 2. Ajouter un commentaire de demarrage
gh issue comment ISSUE_NUMBER --repo OWNER/REPO --body "$(cat <<'EOF'
## 🚀 Agent started

**Task**: TASK-XXX
**Started**: $(date -u +"%Y-%m-%d %H:%M UTC")
**Agent**: sub-agent ID
**Dependencies met**: TASK-001 ✅, TASK-002 ✅

---
_Automated by execute-github-project_
EOF
)"
```

#### 3.2 — Lancer le sub-agent

Utiliser l'outil **Task** pour lancer un sub-agent avec un prompt qui inclut :

1. Le **body complet de l'issue** (le prompt autonome de la tache)
2. Les **instructions de logging** (voir template ci-dessous)
3. Le **numero d'issue** pour les commits et commentaires
4. Le **repo** (owner/name) pour les commandes `gh`

**Template prompt sub-agent** :

```
Tu executes la tache #{ISSUE_NUMBER} du projet {REPO}.

## Instructions de tracabilite

1. COMMITS : chaque commit doit inclure "refs #{ISSUE_NUMBER}" dans le message.
   Exemple : git commit -m "feat: add CRC-16 module refs #{ISSUE_NUMBER}"

2. LOGS : a chaque etape significative, ajouter un commentaire sur l'issue :
   gh issue comment {ISSUE_NUMBER} --repo {REPO} --body "### Progression\n- Etape: [description]\n- Fichiers: [liste]\n- Status: [en cours/fait]"

3. ERREURS : si une erreur survient, ajouter un commentaire avec le detail :
   gh issue comment {ISSUE_NUMBER} --repo {REPO} --body "### ⚠️ Erreur\n```\n[erreur]\n```\nAction: [ce qui a ete tente]"

4. FIN : ne PAS mettre a jour le statut du projet — le workflow principal s'en charge.

## Tache a executer

{ISSUE_BODY}
```

#### 3.3 — Fin de tache (succes)

```bash
# 1. Lister les commits lies
COMMITS=$(git log --oneline --grep="refs #${ISSUE_NUMBER}" | head -20)

# 2. Commentaire de cloture
gh issue comment $ISSUE_NUMBER --repo $REPO --body "$(cat <<EOF
## ✅ Task completed

**Finished**: $(date -u +"%Y-%m-%d %H:%M UTC")

### Commits
\`\`\`
$COMMITS
\`\`\`

### Summary
[Resume du travail effectue par le sub-agent]

---
_Automated by execute-github-project_
EOF
)"

# 3. Mettre le statut "Done" dans le projet
# (mutation GraphQL — voir reference.md)

# 4. Fermer l'issue
gh issue close $ISSUE_NUMBER --repo $REPO
```

#### 3.4 — Fin de tache (echec)

```bash
# 1. Commentaire d'echec
gh issue comment $ISSUE_NUMBER --repo $REPO --body "$(cat <<EOF
## ❌ Task failed

**Failed at**: $(date -u +"%Y-%m-%d %H:%M UTC")
**Error**: [description de l'erreur]
**Last action**: [derniere action tentee]

### Partial commits
\`\`\`
$COMMITS
\`\`\`

### Debug info
[Logs pertinents du sub-agent]

---
_Automated by execute-github-project_
EOF
)"

# 2. Statut "Failed" et label
gh issue edit $ISSUE_NUMBER --repo $REPO --add-label "blocked"
```

### Phase 4 — Boucle de progression

Apres chaque tache terminee :

1. Verifier quelles taches sont maintenant **debloquees** (tous `requires` en `Done`)
2. Lancer les taches nouvellement pretes (max 3-4 paralleles)
3. Repeter jusqu'a ce que toutes les taches soient `Done` ou `Failed`

```
while taches_restantes:
    pretes = [t for t in taches if all(dep.status == 'Done' for dep in t.requires)]
    for t in pretes[:4]:  # max 4 paralleles
        lancer_sub_agent(t)
    attendre_fin_agents()
    mettre_a_jour_statuts()
```

### Phase 5 — Rapport final

Ajouter un commentaire recapitulatif sur la premiere tache ou dans le README du projet :

```markdown
## Pipeline Report

| Task | Status | Duration | Commits |
|------|--------|----------|---------|
| TASK-001 | ✅ Done | 5 min | abc1234, def5678 |
| TASK-002 | ✅ Done | 3 min | 789abcd |
| TASK-003 | ❌ Failed | 8 min | - |
```

## Gestion des erreurs

| Situation | Action |
|-----------|--------|
| Sub-agent timeout | Commenter l'issue avec les logs, statut `Failed` |
| Dependance echouee | Taches dependantes → statut `Blocked`, commentaire explicatif |
| Conflit git | Commenter l'issue, tenter `git pull --rebase`, retry une fois |
| Build casse | Commenter avec l'erreur, statut `Failed`, ne pas continuer |

## Conventions commits

Format : `type(scope): description refs #ISSUE_NUMBER`

```
feat(bp): add CRC-16 module refs #42
fix(ba): correct I2C address for SC940 refs #45
test(bp): add MD5 RFC 1321 test vectors refs #48
docs: update migration checklist refs #52
```

## Checklist d'execution

```
- [ ] Projet identifie (PROJECT_ID, REPO)
- [ ] Drafts convertis en issues
- [ ] Status field ID recupere
- [ ] Dependances resolues (ordre topologique)
- [ ] Taches sans deps lancees en premier
- [ ] Chaque tache : start comment → agent → end comment → status update
- [ ] Commits lies aux issues via "refs #N"
- [ ] Taches echouees documentees
- [ ] Rapport final genere
```

## Ressources

- Queries GraphQL detaillees : [reference.md](reference.md)
- Creation de taches : [plan-to-github-tasks](../plan-to-github-tasks/SKILL.md)
