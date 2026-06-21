# Exemples de plans et tâches

## Format YAML recommandé

```yaml
project:
  name: "Migration API v2"
  description: "Migration de l'API REST vers GraphQL"
  
tasks:
  - id: "TASK-001"
    title: "Configurer Apollo Server"
    context: |
      Le projet utilise Express.js avec TypeScript.
      L'API actuelle est REST, on migre vers GraphQL.
    objective: |
      Installer et configurer Apollo Server avec Express.
      Créer le schéma de base et le resolver health-check.
    files: |
      - `src/graphql/index.ts` - Point d'entrée Apollo
      - `src/graphql/schema.ts` - Schéma GraphQL
      - `package.json` - Dépendances Apollo
    constraints: |
      - Utiliser Apollo Server v4
      - Garder l'API REST fonctionnelle pendant la migration
    success_criteria: |
      - [ ] Apollo Server démarre sur /graphql
      - [ ] Query health-check fonctionne
      - [ ] Tests d'intégration passent
    depends_on: []
    
  - id: "TASK-002"
    title: "Définir les types User"
    context: |
      Les utilisateurs ont: id, email, name, role, createdAt.
      Le modèle Prisma existe déjà dans schema.prisma.
    objective: |
      Créer les types GraphQL pour User et les resolvers CRUD.
    files: |
      - `src/graphql/types/user.ts` - Types User
      - `src/graphql/resolvers/user.ts` - Resolvers
    depends_on: ["TASK-001"]
    
  - id: "TASK-003"
    title: "Définir les types Product"
    context: |
      Les produits ont: id, name, price, stock, categoryId.
      Relations: Product -> Category (N:1)
    objective: |
      Créer les types GraphQL pour Product avec relations.
    depends_on: ["TASK-001"]
    
  - id: "TASK-004"
    title: "Implémenter l'authentification GraphQL"
    context: |
      L'auth actuelle utilise JWT dans le header Authorization.
      Le middleware Express valide déjà le token.
    objective: |
      Intégrer le contexte auth dans Apollo pour protéger les mutations.
    depends_on: ["TASK-001", "TASK-002"]
```

## Format Markdown simplifié

```markdown
# Plan: Refactoring Module Paiement

## [TASK-001] Extraire l'interface PaymentProvider

depends_on: []

Créer une interface abstraite pour tous les providers de paiement.

### Fichiers
- `src/payments/interfaces.ts` - Nouvelle interface
- `src/payments/stripe.ts` - Adapter à l'interface

### Critères
- Interface définit: charge, refund, getStatus
- Tests unitaires pour chaque méthode

## [TASK-002] Migrer Stripe vers nouvelle interface

depends_on: [TASK-001]

Adapter le provider Stripe existant à la nouvelle interface.

### Fichiers
- `src/payments/providers/stripe.ts`

## [TASK-003] Ajouter provider PayPal

depends_on: [TASK-001]

Implémenter PayPal selon la même interface.

### Fichiers
- `src/payments/providers/paypal.ts`

## [TASK-004] Factory de sélection provider

depends_on: [TASK-002, TASK-003]

Créer une factory qui sélectionne le provider selon la config.
```

## Prompt autonome généré (exemple)

Voici ce que produit le script pour TASK-004 :

```markdown
# TASK-004: Factory de sélection provider

## Contexte
Le module paiement supporte maintenant plusieurs providers (Stripe, PayPal)
via une interface commune PaymentProvider.

## Objectif
Créer une factory qui instancie le bon provider selon la configuration
de l'utilisateur ou du tenant.

## Fichiers concernés
| Fichier | Action | Raison |
|---------|--------|--------|
| `src/payments/factory.ts` | Créer | Factory principale |
| `src/payments/index.ts` | Modifier | Export factory |
| `tests/payments/factory.test.ts` | Créer | Tests unitaires |

## Implémentation suggérée
```typescript
// src/payments/factory.ts
import { PaymentProvider } from './interfaces';
import { StripeProvider } from './providers/stripe';
import { PayPalProvider } from './providers/paypal';

export function createPaymentProvider(type: 'stripe' | 'paypal'): PaymentProvider {
  switch (type) {
    case 'stripe':
      return new StripeProvider(process.env.STRIPE_KEY);
    case 'paypal':
      return new PayPalProvider(process.env.PAYPAL_KEY);
    default:
      throw new Error(`Unknown payment provider: ${type}`);
  }
}
```

## Dépendances
### Prérequis (compléter avant de commencer)
- **TASK-002**: Migrer Stripe vers nouvelle interface
- **TASK-003**: Ajouter provider PayPal

### Bloque (attend cette tâche)
Aucune tâche en attente.

## Critères de succès
- [ ] Factory retourne le bon provider
- [ ] Erreur explicite si provider inconnu
- [ ] Tests couvrent tous les cas
- [ ] Documentation JSDoc

## Commandes de validation
```bash
npm run build
npm run test -- --grep "factory"
npm run lint
```

---
dependencies:
  requires: ["TASK-002", "TASK-003"]
  blocks: []
---
```

## Graphe de dépendances

```
TASK-001 (Apollo Server)
    ├── TASK-002 (Types User) ──┐
    │                           ├── TASK-004 (Auth GraphQL)
    └── TASK-003 (Types Product)
```

Le script crée les tâches dans l'ordre : 001 → 002 → 003 → 004
