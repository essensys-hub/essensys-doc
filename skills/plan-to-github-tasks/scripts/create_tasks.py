#!/usr/bin/env python3
"""
Crée des tâches GitHub Project depuis un fichier de plan structuré.

Usage:
    python create_tasks.py plan.yaml --project "Nom du Projet" --owner "username"
    python create_tasks.py plan.md --project 5 --owner "org-name" --org

Formats supportés:
    - YAML: Structure directe des tâches
    - Markdown: Parse les sections ## comme tâches
"""

import argparse
import json
import subprocess
import sys
import re
from pathlib import Path
from typing import Optional

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def run_gh_graphql(query: str, variables: dict) -> dict:
    """Exécute une requête GraphQL via gh cli."""
    cmd = ["gh", "api", "graphql", "-f", f"query={query}"]
    for key, value in variables.items():
        if isinstance(value, bool):
            cmd.extend(["-F", f"{key}={str(value).lower()}"])
        elif isinstance(value, int):
            cmd.extend(["-F", f"{key}={value}"])
        else:
            cmd.extend(["-f", f"{key}={value}"])
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Erreur GraphQL: {result.stderr}", file=sys.stderr)
        sys.exit(1)
    return json.loads(result.stdout)


def get_project_id(owner: str, project: str, is_org: bool = False) -> str:
    """Récupère l'ID du projet GitHub."""
    if project.isdigit():
        number = int(project)
        if is_org:
            query = """
            query($org: String!, $number: Int!) {
                organization(login: $org) {
                    projectV2(number: $number) { id title }
                }
            }"""
            result = run_gh_graphql(query, {"org": owner, "number": number})
            return result["data"]["organization"]["projectV2"]["id"]
        else:
            query = """
            query($user: String!, $number: Int!) {
                user(login: $user) {
                    projectV2(number: $number) { id title }
                }
            }"""
            result = run_gh_graphql(query, {"user": owner, "number": number})
            return result["data"]["user"]["projectV2"]["id"]
    else:
        if is_org:
            query = """
            query($org: String!) {
                organization(login: $org) {
                    projectsV2(first: 50) {
                        nodes { id title }
                    }
                }
            }"""
            result = run_gh_graphql(query, {"org": owner})
            projects = result["data"]["organization"]["projectsV2"]["nodes"]
        else:
            query = """
            query($user: String!) {
                user(login: $user) {
                    projectsV2(first: 50) {
                        nodes { id title }
                    }
                }
            }"""
            result = run_gh_graphql(query, {"user": owner})
            projects = result["data"]["user"]["projectsV2"]["nodes"]
        
        for p in projects:
            if p["title"].lower() == project.lower():
                return p["id"]
        
        print(f"Projet '{project}' non trouvé", file=sys.stderr)
        sys.exit(1)


def create_draft_issue(project_id: str, title: str, body: str) -> str:
    """Crée un draft issue dans le projet."""
    query = """
    mutation($projectId: ID!, $title: String!, $body: String!) {
        addProjectV2DraftIssue(input: {
            projectId: $projectId
            title: $title
            body: $body
        }) {
            projectItem { id }
        }
    }"""
    result = run_gh_graphql(query, {
        "projectId": project_id,
        "title": title,
        "body": body
    })
    return result["data"]["addProjectV2DraftIssue"]["projectItem"]["id"]


def parse_yaml_plan(path: Path) -> list[dict]:
    """Parse un fichier YAML de plan."""
    if not HAS_YAML:
        print("PyYAML requis: pip install pyyaml", file=sys.stderr)
        sys.exit(1)
    
    with open(path) as f:
        data = yaml.safe_load(f)
    
    return data.get("tasks", [])


def parse_markdown_plan(path: Path) -> list[dict]:
    """Parse un fichier Markdown de plan (format basique)."""
    with open(path) as f:
        content = f.read()
    
    tasks = []
    task_pattern = re.compile(
        r'^##\s+(?:\[([A-Z]+-\d+)\]\s+)?(.+?)$',
        re.MULTILINE
    )
    
    matches = list(task_pattern.finditer(content))
    for i, match in enumerate(matches):
        task_id = match.group(1) or f"TASK-{i+1:03d}"
        title = match.group(2).strip()
        
        start = match.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(content)
        body = content[start:end].strip()
        
        depends_on = []
        dep_match = re.search(r'depends_on:\s*\[([^\]]+)\]', body)
        if dep_match:
            depends_on = [d.strip() for d in dep_match.group(1).split(',')]
        
        tasks.append({
            "id": task_id,
            "title": title,
            "body": body,
            "depends_on": depends_on
        })
    
    return tasks


def topological_sort(tasks: list[dict]) -> list[dict]:
    """Trie les tâches par ordre topologique (dépendances d'abord)."""
    task_map = {t["id"]: t for t in tasks}
    visited = set()
    result = []
    
    def visit(task_id: str):
        if task_id in visited:
            return
        visited.add(task_id)
        task = task_map.get(task_id)
        if task:
            for dep in task.get("depends_on", []):
                visit(dep)
            result.append(task)
    
    for task in tasks:
        visit(task["id"])
    
    return result


def generate_autonomous_prompt(task: dict, all_tasks: dict) -> str:
    """Génère un prompt autonome complet pour la tâche."""
    task_id = task["id"]
    depends_on = task.get("depends_on", [])
    blocks = task.get("blocks", [])
    
    prompt = f"""# {task_id}: {task['title']}

## Contexte
{task.get('context', 'Voir la description du projet principal.')}

## Objectif
{task.get('objective', task.get('body', 'Accomplir cette tâche.'))}

## Fichiers concernés
{task.get('files', 'À déterminer selon l\'analyse.')}

## Contraintes
{task.get('constraints', '- Respecter les conventions du projet')}

## Critères de succès
{task.get('success_criteria', '- [ ] Implémentation complète\\n- [ ] Tests passent\\n- [ ] Code review')}

## Dépendances
"""
    
    if depends_on:
        prompt += "### Prérequis (compléter avant de commencer)\n"
        for dep_id in depends_on:
            dep_task = all_tasks.get(dep_id, {})
            prompt += f"- **{dep_id}**: {dep_task.get('title', 'Tâche prérequise')}\n"
    else:
        prompt += "### Prérequis\nAucun - cette tâche peut démarrer immédiatement.\n"
    
    if blocks:
        prompt += "\n### Bloque (attend cette tâche)\n"
        for block_id in blocks:
            block_task = all_tasks.get(block_id, {})
            prompt += f"- **{block_id}**: {block_task.get('title', 'Tâche en attente')}\n"
    
    prompt += f"""
## Commandes de validation
```bash
# À adapter selon le projet
npm run build
npm run test
npm run lint
```

---
dependencies:
  requires: {json.dumps(depends_on)}
  blocks: {json.dumps(blocks)}
---
"""
    return prompt


def main():
    parser = argparse.ArgumentParser(
        description="Crée des tâches GitHub Project depuis un plan"
    )
    parser.add_argument("plan", type=Path, help="Fichier de plan (YAML ou MD)")
    parser.add_argument("--project", required=True, help="Nom ou numéro du projet")
    parser.add_argument("--owner", required=True, help="Username ou org")
    parser.add_argument("--org", action="store_true", help="Owner est une organisation")
    parser.add_argument("--dry-run", action="store_true", help="Affiche sans créer")
    
    args = parser.parse_args()
    
    if args.plan.suffix in [".yaml", ".yml"]:
        tasks = parse_yaml_plan(args.plan)
    else:
        tasks = parse_markdown_plan(args.plan)
    
    if not tasks:
        print("Aucune tâche trouvée dans le plan", file=sys.stderr)
        sys.exit(1)
    
    tasks = topological_sort(tasks)
    task_map = {t["id"]: t for t in tasks}
    
    for task in tasks:
        for dep_id in task.get("depends_on", []):
            if dep_id in task_map:
                task_map[dep_id].setdefault("blocks", []).append(task["id"])
    
    print(f"📋 {len(tasks)} tâches à créer")
    
    if args.dry_run:
        for task in tasks:
            prompt = generate_autonomous_prompt(task, task_map)
            print(f"\n{'='*60}")
            print(f"[{task['id']}] {task['title']}")
            print(f"{'='*60}")
            print(prompt[:500] + "..." if len(prompt) > 500 else prompt)
        return
    
    project_id = get_project_id(args.owner, args.project, args.org)
    print(f"✅ Projet trouvé: {project_id[:20]}...")
    
    created = {}
    for task in tasks:
        title = f"[{task['id']}] {task['title']}"
        body = generate_autonomous_prompt(task, task_map)
        
        item_id = create_draft_issue(project_id, title, body)
        created[task["id"]] = item_id
        print(f"✅ Créé: {title}")
    
    print(f"\n🎉 {len(created)} tâches créées avec succès!")


if __name__ == "__main__":
    main()
