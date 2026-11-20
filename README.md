
# Hash-Audit AI – IA d'audit de hachage

### Système multi-agents d'audit des mécanismes de hachage et de stockage des mots de passe

Hash-Audit AI est un prototype pédagogique local associant **cybersécurité, cryptographie appliquée et intelligence artificielle multi-agents**.

Il analyse statiquement du code source Python afin d'identifier les mécanismes de hachage utilisés, d'évaluer les risques associés et de proposer des recommandations de sécurisation.

**[Documentation](https://imeldamague.github.io/hash-audit-ai/)** · **[GitHub](https://github.com/imeldamague/hash-audit-ai)** · **[Zenodo v1.0.0](https://doi.org/10.5281/zenodo.24382721)** · **[Zenodo v1.0.2](https://doi.org/10.5281/zenodo.24380585)**

---

## Présentation

Hash-Audit AI repose sur une architecture composée de **six agents spécialisés**, coordonnés par un orchestrateur.

Chaque agent intervient dans une étape du processus d'audit : exploration du code, identification des mécanismes cryptographiques, évaluation des risques, recommandations, vérification et synthèse.

L'objectif est de proposer une approche structurée et traçable de l'analyse des mécanismes de stockage des mots de passe.

Le projet est conçu pour fonctionner localement et peut utiliser des modèles de langage exécutés avec Ollama.

## Fonctionnalités principales

- Analyse statique de fichiers source Python.
- Identification de mécanismes de hachage tels que MD5, SHA-256 avec sel et Argon2id.
- Évaluation des risques associés aux pratiques détectées.
- Comparaison d'Argon2id, bcrypt, scrypt et PBKDF2-SHA256.
- Génération d'un jeu de données de 1 000 comptes synthétiques.
- Génération et audit de 25 fichiers Python de test.
- Simulation d'attaque par dictionnaire.
- Gestion du pepper (secret supplémentaire).
- Vérification facultative des mots de passe compromis avec Pwned Passwords et le mécanisme de k-anonymat.
- Simulation statistique d'une migration sur 90 jours.
- Génération de rapports et de traces d'audit au format JSONL.
- Exécution des expériences avec la commande `make reproduce`.
- Documentation des résultats et de l'environnement d'exécution.

## Architecture multi-agents

Les six agents spécialisés sont coordonnés par un orchestrateur.

| Agent | Responsabilité |
|---|---|
| Explorateur | Recueillir et analyser les éléments à auditer |
| Identificateur | Repérer les mécanismes de hachage |
| Évaluateur | Analyser les risques associés |
| Correcteur | Proposer des recommandations de sécurisation |
| Testeur | Vérifier les résultats produits |
| Auditeur | Contrôler et synthétiser l'audit |

Les agents partagent un état de travail permettant de coordonner les différentes étapes du traitement.

La génération de recommandations n'implique pas nécessairement l'application automatique d'un correctif. Les propositions doivent être vérifiées avant utilisation.

[Consulter le schéma détaillé de l'architecture](https://imeldamague.github.io/hash-audit-ai/architecture/).

## Technologies utilisées

| Technologie | Utilisation |
|---|---|
| Python 3.11+ | Développement du système |
| Argon2id | Référence de stockage sécurisé des mots de passe |
| bcrypt, scrypt, PBKDF2-SHA256 | Comparaison des mécanismes de dérivation |
| Ollama | Exécution facultative de modèles de langage locaux |
| Pytest | Tests automatisés |
| pytest-cov | Mesure de la couverture du code |
| GitHub Actions | Intégration continue |
| Material for MkDocs | Documentation technique |
| GPG | Signature numérique des fichiers d'intégrité |
| Zenodo | Archivage scientifique et attribution de DOI |

## Installation

### Prérequis

- Python 3.11 ou supérieur
- Git
- PowerShell sous Windows ou un terminal sous Linux
- GNU Make pour la commande de reproduction
- Ollama, facultatif selon les expériences

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

L'installation et l'exécution complète depuis un clone vierge n'ont pas encore été validées indépendamment.

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

## Reproduction des expériences

La version `v1.0.2` contient un Makefile permettant d'exécuter les principales expériences du projet avec une commande unique.

```bash
make reproduce
```

Cette commande enchaîne notamment :

1. La génération des 1 000 comptes synthétiques.
2. La génération des 25 fichiers Python mutés.
3. L'audit des mutations.
4. Les benchmarks cryptographiques.
5. La simulation de migration sur 90 jours.
6. L'exécution des tests automatisés.

L'exécution a été validée dans l'environnement Windows local du projet.

**Limite de reproductibilité :** l'exécution depuis un environnement entièrement vierge n'a pas été vérifiée par un tiers. Les sels aléatoires peuvent également produire des empreintes différentes entre deux générations du jeu de données.

## Résultats de validation

### Résultats principaux

| Indicateur | Résultat |
|---|---:|
| Tests automatisés réussis | 66 |
| Couverture de code de référence | 87 % |
| Comptes synthétiques | 1 000 |
| Fichiers Python de test | 25 |
| Correspondances attendues sur les cas contrôlés | 25/25 |
| Taux de correspondance sur les cas contrôlés | 100 % |
| Simulation statistique | 90 jours |
| Algorithmes comparés | 4 |

La couverture de 87 % correspond à une mesure de référence du 12 novembre 2026 et n'a pas été recalculée lors de la dernière reproduction.

Les 25 correspondances obtenues concernent exclusivement les fichiers synthétiques contrôlés du jeu de validation. Elles ne constituent pas une mesure de précision généralisable aux applications réelles.

### Benchmarks cryptographiques

Résultats enregistrés dans `results/hash_benchmark.csv` pour la version `v1.0.2`.

| Algorithme | Hachage moyen | Vérification moyenne |
|---|---:|---:|
| Argon2id | 27,98 ms | 27,60 ms |
| scrypt | 54,67 ms | 54,55 ms |
| bcrypt | 253,63 ms | 254,11 ms |
| PBKDF2-SHA256 | 295,38 ms | 298,84 ms |

Chaque mesure repose sur 10 répétitions locales.

Ces résultats dépendent notamment du matériel, de l'environnement d'exécution et des paramètres cryptographiques retenus.

Ils ne permettent pas, à eux seuls, de classer les algorithmes en matière de sécurité.

### Simulation de migration

La simulation statistique couvre 90 jours, avec 91 observations correspondant aux jours 0 à 90.

| Indicateur | Résultat |
|---|---:|
| Taux migré au jour 0 | 33,3 % |
| Taux migré au jour 54 | 90,1 % |
| Taux migré au jour 90 | 96,9 % |

Ces résultats proviennent d'une simulation et ne correspondent pas à la migration de comptes réels.

### Durée et mémoire de reproduction

Une exécution instrumentée de `make reproduce` a été réalisée le **20 novembre 2026**.

| Indicateur | Résultat |
|---|---:|
| Durée totale mesurée | 90,65 secondes |
| Pic RAM observé | 82,79 Mo |
| Tests réussis | 66 |
| Mutations analysées | 25/25 |

Le pic RAM constitue une estimation basée sur les processus Python et Make visibles pendant la surveillance. Cette mesure n'isole pas exclusivement les processus du projet.

Le code de sortie du processus n'a pas été capturé, mais les journaux indiquent la réussite des 66 tests et la fin de la commande de reproduction.

Ces mesures ont été effectuées après l'archivage de `v1.0.2`.

### Fichiers de résultats

Les principaux artefacts expérimentaux sont disponibles dans le dossier `results/`.

| Fichier | Contenu |
|---|---|
| `accounts.json` | Comptes synthétiques et empreintes |
| `mutation_audit.json` | Résultats d'audit des mutations |
| `hash_benchmark.csv` | Performances des algorithmes |
| `migration.json` | Simulation de migration |
| `model_benchmark.csv` | Mesures d'expériences avec les modèles |
| `model_comparison.csv` | Comparaisons de réponses de modèles |
| `metrics.json` | Synthèse des métriques |
| `ENVIRONMENT.json` | Informations sur l'environnement d'exécution |

Les fichiers `metrics.json` et `ENVIRONMENT.json` ont été inclus à partir de la version `v1.0.2`.

### Exécuter les tests

```bash
python -m pytest
```

### Mesurer la couverture

```bash
python -m pytest --cov=src/hash_audit --cov-report=term-missing
```

## Modèles de langage locaux

Hash-Audit AI peut utiliser Ollama pour les expérimentations avec des modèles de langage locaux.

Les modèles suivants ont été identifiés dans l'environnement de travail le 20 novembre 2026.

### Llama 3.2 – 3B

```text
Modèle : llama3.2:3b
Digest : a80c4f17acd55265feec403c7aef86be0c25983ab279d83f3bcd3abbcb5b8b72
```

### Qwen 3 – 4B

```text
Modèle : qwen3:4b
Digest : 359d7dd4bcdab3d86b87d73ac27966f4dbb9f5efdfcc75d34a8764a09474fae7
```

Ces digests correspondent aux modèles installés localement au moment de leur vérification.

L'utilisation des modèles est facultative pour certaines expériences. Les réponses générées doivent être contrôlées et ne constituent pas des preuves de sécurité indépendantes.

## Intégrité et signatures numériques

L'intégrité de l'archive Zenodo `v1.0.2` est documentée par trois fichiers publiés sur la branche `main` :

- [SHA256SUMS](https://github.com/imeldamague/hash-audit-ai/blob/main/SHA256SUMS)
- [SHA256SUMS.sig](https://github.com/imeldamague/hash-audit-ai/blob/main/SHA256SUMS.sig)
- [gpg-public-key.asc](https://github.com/imeldamague/hash-audit-ai/blob/main/gpg-public-key.asc)

### Empreinte SHA-256 de l'archive Zenodo v1.0.2

```text
8cb56d85ba290d19ac033f1b647543d8f5b98fc831fd473e60b7dacf2753779d
```

Cette empreinte a été calculée à partir de l'archive ZIP téléchargée depuis Zenodo.

### Empreinte de la clé publique GPG

```text
AF708E936B509CD316FF73CBB5BA3E50495E2F52
```

### Vérification de la signature

Après téléchargement des fichiers `SHA256SUMS`, `SHA256SUMS.sig` et `gpg-public-key.asc` :

```bash
gpg --import gpg-public-key.asc
gpg --verify SHA256SUMS.sig SHA256SUMS
```

Pour vérifier également le contenu de l'archive, télécharger le ZIP correspondant, le nommer `hash-audit-ai-v1.0.2.zip` et le placer dans le même dossier que `SHA256SUMS`.

Sous Linux :

```bash
sha256sum -c SHA256SUMS
```

Sous Windows PowerShell :

```powershell
Get-FileHash .\hash-audit-ai-v1.0.2.zip -Algorithm SHA256
```

Comparer l'empreinte obtenue avec celle enregistrée dans `SHA256SUMS`.

La signature GPG a été vérifiée avec succès le 20 novembre 2026.

**Important :** les fichiers de signature ont été ajoutés sur `main` après l'archivage de `v1.0.2`. Ils constituent des preuves complémentaires et ne sont pas inclus rétroactivement dans son archive Zenodo.

## Documentation

La documentation technique complète est disponible sur GitHub Pages.

**[Consulter la documentation de Hash-Audit AI](https://imeldamague.github.io/hash-audit-ai/)**

| Rubrique | Description |
|---|---|
| Architecture | Organisation des agents et orchestration |
| Fonctionnement | Déroulement des audits |
| Résultats | Tests et expérimentations |
| Installation | Installation et utilisation |
| Sécurité et limites | Périmètre et précautions |

Autres documents :

- [Rapport technique PDF](https://github.com/imeldamague/hash-audit-ai/blob/v1.0.2/docs/rapport.pdf)
- [Procédure d'audit – AUDIT.md](https://github.com/imeldamague/hash-audit-ai/blob/v1.0.2/AUDIT.md)
- [Carte du système – SYSTEM_CARD.md](https://github.com/imeldamague/hash-audit-ai/blob/v1.0.2/SYSTEM_CARD.md)
- [Déclaration d'usage de l'IA – AI_USAGE.md](https://github.com/imeldamague/hash-audit-ai/blob/v1.0.2/AI_USAGE.md)

## Sécurité et limites

Hash-Audit AI est un prototype pédagogique local.

Il ne constitue ni une certification de sécurité ni un remplacement d'un audit professionnel.

Les précautions suivantes doivent être prises en compte :

- Les démonstrations utilisent des données synthétiques.
- Les fichiers analysés ne doivent pas être exécutés simplement parce qu'ils sont soumis à l'audit.
- L'analyse statique peut produire des faux positifs et des faux négatifs.
- L'intégration d'Ollama est facultative et ses réponses nécessitent une vérification.
- La vérification avec Pwned Passwords est facultative et désactivée par défaut dans la démonstration.
- Les recommandations et correctifs doivent être validés par une personne compétente avant toute utilisation.
- La simulation de migration ne modifie aucun compte réel.
- Les résultats expérimentaux peuvent varier selon le matériel et l'environnement.
- Une reproduction depuis un clone vierge reste à vérifier indépendamment.

## Publication et archivage

Le projet est publié sur GitHub et archivé sur Zenodo.

### Versions officielles

| Information | Valeur |
|---|---|
| Dépôt GitHub public | [imeldamague/hash-audit-ai](https://github.com/imeldamague/hash-audit-ai) |
| Version initiale | [v1.0.0](https://github.com/imeldamague/hash-audit-ai/releases/tag/v1.0.0) |
| DOI Zenodo v1.0.0 | [10.5281/zenodo.24382721](https://doi.org/10.5281/zenodo.24382721) |
| Version d'archivage intermédiaire | [v1.0.1](https://github.com/imeldamague/hash-audit-ai/releases/tag/v1.0.1) |
| DOI Zenodo v1.0.1 | [10.5281/zenodo.24178005](https://doi.org/10.5281/zenodo.24178005) |
| Version expérimentale enrichie | [v1.0.2](https://github.com/imeldamague/hash-audit-ai/releases/tag/v1.0.2) |
| DOI Zenodo v1.0.2 | [10.5281/zenodo.24380585](https://doi.org/10.5281/zenodo.24380585) |
| Licence | MIT |
| Langage principal | Python |

### Distinction entre les versions

**v1.0.0**

Première version stable du projet, comprenant l'architecture multi-agents, les fonctionnalités d'audit, les simulations et les tests automatisés.

Cette version dispose d'une archive Zenodo spécifique publiée le 20 novembre 2026.

**v1.0.1**

Version intermédiaire consacrée à l'archivage et à la traçabilité de la première version stable.

**v1.0.2**

Version enrichie comprenant notamment :

- Le Makefile complet avec `make reproduce`.
- Le rapport technique `docs/rapport.pdf`.
- Les métriques dans `results/metrics.json`.
- Les informations d'environnement dans `results/ENVIRONMENT.json`.
- Les résultats de benchmarks actualisés.
- La documentation du projet.

Les archives Zenodo sont figées : les modifications publiées ultérieurement sur `main` ne modifient pas les versions déjà archivées.

### Limites de la publication

L'archive `v1.0.0` a été déposée séparément sur Zenodo. Sa correspondance exacte avec le tag GitHub a été déclarée lors du dépôt, mais n'a pas fait l'objet d'une vérification indépendante documentée ici.

L'exécution de l'intégration continue sur le tag `v1.0.0`, la reproduction depuis un clone vierge et certains justificatifs complémentaires restent à vérifier.

## Auteur

**Imelda Magué**

- GitHub : [@imeldamague](https://github.com/imeldamague)
- Documentation : [Hash-Audit AI](https://imeldamague.github.io/hash-audit-ai/)
- Projet individuel : Cryptographie appliquée et IA agentique
- Promotion : **2026–2027**

Projet consacré à la cybersécurité, à l'analyse des mécanismes de hachage et à l'intelligence artificielle multi-agents.

---

**Hash-Audit AI – Prototype pédagogique de recherche et d'expérimentation en cybersécurité.**
