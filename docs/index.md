
# Hash-Audit AI

### Audit intelligent des mécanismes de stockage des mots de passe

Hash-Audit AI est un prototype pédagogique local associant cybersécurité et intelligence artificielle multi-agents.

Il analyse le code source pour identifier les mécanismes de hachage utilisés, évaluer les risques et proposer des recommandations de sécurisation.

[Découvrir l'architecture](architecture.md) · [Accéder au dépôt GitHub](https://github.com/imeldamague/hash-audit-ai)

---

## Présentation du projet

Le projet repose sur six agents spécialisés coordonnés par un orchestrateur. Chaque agent intervient dans une étape précise du processus d'audit, de l'analyse du code jusqu'à la synthèse des résultats.

## Indicateurs clés

| Indicateur | Résultat |
|---|---:|
| Comptes synthétiques | 1 000 |
| Fichiers Python de test | 25 |
| Tests automatisés | 66 |
| Couverture de tests | 87 % |
| Simulation de migration | 90 jours |

Les résultats de détection sur les 25 fichiers concernent exclusivement des jeux de test synthétiques contrôlés.

## Les six agents spécialisés

| Agent | Responsabilité |
|---|---|
| Explorateur | Collecte et analyse les éléments à auditer |
| Identificateur | Repère les mécanismes de hachage |
| Évaluateur | Analyse les risques associés |
| Correcteur | Propose des recommandations |
| Testeur | Vérifie les résultats produits |
| Auditeur | Contrôle et synthétise l'audit |

[Consulter le schéma de l'architecture](architecture.md)

## Objectifs

- Identifier les mécanismes de stockage des mots de passe.
- Détecter les pratiques cryptographiques faibles ou inadaptées.
- Évaluer les risques associés aux mécanismes identifiés.
- Proposer des recommandations de sécurisation.
- Illustrer une migration progressive vers Argon2id.
- Assurer la traçabilité des opérations d'audit.

## Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python 3.11+ | Développement de l'application |
| Argon2id | Référence de stockage sécurisé |
| bcrypt, scrypt, PBKDF2-SHA256 | Comparaison des mécanismes de dérivation |
| Ollama | Exécution facultative de modèles locaux |
| Pytest et pytest-cov | Tests et couverture |
| GitHub Actions | Intégration continue |

## Documentation

| Rubrique | Contenu |
|---|---|
| [Architecture](architecture.md) | Organisation des agents et orchestration |
| [Fonctionnement](fonctionnement.md) | Déroulement des audits |
| [Résultats](resultats.md) | Tests et expérimentations |
| [Installation](installation.md) | Installation et utilisation |
| [Sécurité et limites](securite-limites.md) | Périmètre et précautions |

## Sécurité et limites

Hash-Audit AI est un prototype pédagogique local. Il ne constitue ni une certification de sécurité ni un remplacement d'un audit professionnel.

Les résultats, recommandations et éventuels correctifs nécessitent une validation humaine avant toute utilisation. Aucun correctif automatique ne doit être appliqué sans vérification.

## Publication et archivage

| Information | Valeur |
|---|---|
| Version | v1.0.1 |
| Licence | MIT |
| DOI | [10.5281/zenodo.24178005](https://doi.org/10.5281/zenodo.24178005) |
| Dépôt | [GitHub – Hash-Audit AI](https://github.com/imeldamague/hash-audit-ai) |

---

Projet développé autour de la cybersécurité, de l'analyse des mécanismes de hachage et de l'intelligence artificielle multi-agents.
