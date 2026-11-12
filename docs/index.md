
# Hash-Audit AI

## Audit intelligent des mécanismes de stockage des mots de passe

Hash-Audit AI est un prototype pédagogique local de cybersécurité et d'intelligence artificielle agentique. Il permet d'analyser du code source, d'identifier des mécanismes de hachage faibles et de proposer des recommandations de sécurisation.

[Découvrir l'architecture](architecture.md)

[Consulter le dépôt GitHub](https://github.com/imeldamague/hash-audit-ai)

---

## Objectifs du projet

- Identifier les mécanismes de stockage des mots de passe.
- Détecter des pratiques cryptographiques faibles ou inadaptées.
- Évaluer les risques associés aux mécanismes identifiés.
- Proposer des recommandations de sécurisation.
- Illustrer une migration progressive vers Argon2id.
- Assurer la traçabilité des opérations d'audit.

## Architecture multi-agents

Le système repose sur six agents spécialisés coordonnés par un orchestrateur :

| Agent | Responsabilité |
|---|---|
| Explorateur | Collecte et analyse des données |
| Identificateur | Identification des mécanismes de hachage |
| Évaluateur | Évaluation des risques |
| Correcteur | Proposition de recommandations |
| Testeur | Vérification des résultats |
| Auditeur | Contrôle et synthèse de l'audit |

## Chiffres clés

| Indicateur | Résultat |
|---|---:|
| Comptes synthétiques | 1 000 |
| Fichiers Python de test | 25 |
| Tests automatisés | 66 |
| Couverture de tests | 87 % |
| Simulation de migration | 90 jours |

Les résultats de détection concernent exclusivement les fichiers synthétiques contrôlés du projet.

## Technologies

- Python 3.11+
- Argon2id, bcrypt, scrypt et PBKDF2-SHA256
- Architecture multi-agents
- Ollama et modèles locaux
- Pytest et pytest-cov
- GitHub Actions

## Sécurité et limites

Hash-Audit AI est un prototype pédagogique. Il ne remplace ni un audit professionnel ni une validation humaine.

Les résultats, recommandations et éventuels correctifs doivent être examinés par une personne compétente avant toute utilisation. Aucun correctif automatique ne doit être appliqué sans vérification.

## Publication et archivage

- **Version :** v1.0.1
- **Licence :** MIT
- **DOI :** [10.5281/zenodo.24178005](https://doi.org/10.5281/zenodo.24178005)
- **Dépôt :** [GitHub – Hash-Audit AI](https://github.com/imeldamague/hash-audit-ai)



