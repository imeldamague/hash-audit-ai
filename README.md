
# Hash-Audit AI

### Système multi-agents d'audit des mécanismes de hachage et de stockage des mots de passe

Hash-Audit AI est un prototype pédagogique local associant cybersécurité et intelligence artificielle multi-agents.

Il analyse le code source afin d'identifier les mécanismes de hachage utilisés, d'évaluer les risques associés et de proposer des recommandations de sécurisation.

<p align="center">
  <a href="https://imeldamague.github.io/hash-audit-ai/">Documentation</a> ·
  <a href="https://github.com/imeldamague/hash-audit-ai">Dépôt GitHub</a> ·
  <a href="https://doi.org/10.5281/zenodo.24178005">Archive Zenodo</a>
</p>

---

## Présentation

Le projet repose sur une architecture composée de six agents spécialisés coordonnés par un orchestrateur.

Chaque agent intervient dans une étape du processus d'audit : exploration, identification des mécanismes cryptographiques, évaluation des risques, recommandations, vérification et synthèse.

L'objectif est de proposer une approche structurée et traçable de l'analyse des mécanismes de stockage des mots de passe.

## Fonctionnalités principales

- Analyse statique de fichiers source Python.
- Identification de mécanismes de hachage tels que MD5, SHA-256 avec sel et Argon2id.
- Évaluation des risques associés aux pratiques détectées.
- Comparaison d'Argon2id, bcrypt, scrypt et PBKDF2-SHA256.
- Génération d'un jeu de données de 1 000 comptes synthétiques.
- Génération et audit de 25 fichiers Python de test.
- Simulation d'attaque par dictionnaire.
- Gestion du pepper.
- Vérification facultative des mots de passe compromis avec Pwned Passwords et le mécanisme de k-anonymat.
- Simulation statistique d'une migration sur 90 jours.
- Production de rapports et de traces d'audit au format JSONL.

## Architecture multi-agents

Les six agents spécialisés sont coordonnés par un orchestrateur.

| Agent | Responsabilité |
|---|---|
| Explorateur | Collecte et analyse les éléments à auditer |
| Identificateur | Repère les mécanismes de hachage |
| Évaluateur | Analyse les risques associés |
| Correcteur | Propose des recommandations |
| Testeur | Vérifie les résultats produits |
| Auditeur | Contrôle et synthétise l'audit |

Les agents partagent un état de travail permettant de coordonner les différentes étapes du traitement.

Consulter le [schéma détaillé de l'architecture](https://imeldamague.github.io/hash-audit-ai/architecture/).

## Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python 3.11+ | Développement du système |
| Argon2id | Référence de stockage sécurisé |
| bcrypt, scrypt, PBKDF2-SHA256 | Comparaison des mécanismes de dérivation |
| Ollama | Exécution facultative de modèles locaux |
| Pytest | Tests automatisés |
| pytest-cov | Mesure de la couverture |
| GitHub Actions | Intégration continue |
| MkDocs Material | Documentation technique |

## Installation

### Prérequis

- Python 3.11 ou supérieur
- Git
- PowerShell sous Windows ou un terminal sous Linux

### 1. Cloner le dépôt

```bash
git clone https://github.com/imeldamague/hash-audit-ai.git
cd hash-audit-ai
```

### 2. Créer un environnement virtuel

```bash
python -m venv .venv
```

### 3. Activer l'environnement virtuel

Sous Windows PowerShell :

```powershell
.\.venv\Scripts\Activate.ps1
```

Sous Linux :

```bash
source .venv/bin/activate
```

### 4. Installer les dépendances

```bash
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

## Utilisation

### Analyser un fichier source

```bash
python -m hash_audit.cli audit app/demo.py
```

### Générer les fichiers de test

```bash
python -m hash_audit.cli mutations --out data/mutations
```

### Réaliser un audit en lot

```bash
python -m hash_audit.cli audit-batch --input data/mutations --out results/mutation_audit.json
```

### Générer un jeu de données synthétiques

```bash
python -m hash_audit.cli dataset --out results/accounts.json
```

### Simuler une migration

```bash
python -m hash_audit.cli migration --out results/migration.json
```

## Résultats de validation

Résultats de référence mesurés le 12 novembre 2026 :

| Indicateur | Résultat |
|---|---:|
| Tests automatisés réussis | 66 |
| Couverture de code | 87 % |
| Comptes synthétiques | 1 000 |
| Fichiers Python de test | 25 |
| Correspondances correctes sur les cas contrôlés | 25/25 |
| Simulation statistique | 90 jours |

Les résultats de détection concernent exclusivement les fichiers synthétiques contrôlés du jeu de validation. Ils ne constituent pas une mesure de précision généralisable à des applications réelles.

### Exécuter les tests

```bash
python -m pytest
```

### Mesurer la couverture

```bash
python -m pytest --cov=src/hash_audit --cov-report=term-missing
```

## Documentation

La documentation complète est disponible sur GitHub Pages :

**[Consulter la documentation de Hash-Audit AI](https://imeldamague.github.io/hash-audit-ai/)**

| Rubrique | Description |
|---|---|
| Architecture | Organisation des agents et orchestration |
| Fonctionnement | Déroulement des audits |
| Résultats | Tests et expérimentations |
| Installation | Installation et utilisation |
| Sécurité et limites | Périmètre et précautions |

## Sécurité et limites

Hash-Audit AI est un prototype pédagogique local. Il ne constitue ni une certification de sécurité ni un remplacement d'un audit professionnel.

Quelques précautions importantes :

- Les démonstrations utilisent des données synthétiques.
- Les fichiers analysés ne doivent pas être exécutés simplement parce qu'ils sont soumis à l'audit.
- L'analyse statique peut produire des faux positifs et des faux négatifs.
- L'intégration d'Ollama est facultative et ses réponses nécessitent une vérification.
- La vérification Pwned Passwords est facultative et désactivée par défaut dans la démonstration.
- Les recommandations et correctifs doivent être validés par une personne compétente avant toute utilisation.
- La simulation de migration ne modifie aucun compte réel.

## Publication et archivage

| Information | Valeur |
|---|---|
| Version | v1.0.1 |
| Licence | MIT |
| DOI | [10.5281/zenodo.24178005](https://doi.org/10.5281/zenodo.24178005) |
| Dépôt | [GitHub – Hash-Audit AI](https://github.com/imeldamague/hash-audit-ai) |

## Auteur

Projet développé par **Imelda Magué**.

- GitHub : [@imeldamague](https://github.com/imeldamague)
- Documentation : [Hash-Audit AI](https://imeldamague.github.io/hash-audit-ai/)

---

*Projet réalisé autour de la cybersécurité, de l'analyse des mécanismes de hachage et de l'intelligence artificielle multi-agents.*
