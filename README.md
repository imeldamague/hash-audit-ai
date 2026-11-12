
# Hash-Audit AI

**Système d'intelligence artificielle multi-agents pour l'audit de sécurité des mécanismes de hachage et de stockage des mots de passe.**

## Présentation

Hash-Audit AI est un projet de cybersécurité et d'intelligence artificielle agentique conçu pour analyser les pratiques de stockage des mots de passe, détecter des mécanismes de hachage faibles et proposer des recommandations de sécurisation.

Le projet combine des mécanismes d'audit de sécurité, des expérimentations cryptographiques et une architecture multi-agents afin d'évaluer les risques associés au stockage des mots de passe.

## Fonctionnalités

- Génération d'un jeu de données synthétiques de 1 000 comptes.
- Analyse de mécanismes de hachage : MD5, SHA-256 salé et Argon2id.
- Architecture composée de six agents spécialisés et d'un orchestrateur.
- Audit de 25 fichiers Python synthétiques présentant différents mécanismes ou défauts de hachage.
- Simulation d'attaque par dictionnaire.
- Comparaison d'Argon2id, scrypt, bcrypt et PBKDF2-SHA256.
- Gestion du pepper (poivre cryptographique).
- Vérification facultative des mots de passe compromis avec Pwned Passwords et le mécanisme k-anonymity.
- Simulation statistique d'une migration sur 90 jours.
- Génération de résultats et de traces d'audit.

## Architecture multi-agents

Le système repose sur six agents spécialisés coordonnés par un orchestrateur :

- **Agent explorateur :** collecte et analyse les données.
- **Agent identificateur :** identifie les mécanismes de hachage.
- **Agent évaluateur :** évalue les risques de sécurité.
- **Agent correcteur :** propose des recommandations de sécurisation.
- **Agent testeur :** vérifie les résultats et les corrections.
- **Agent auditeur :** contrôle et synthétise les résultats.

## Technologies utilisées

- **Langage :** Python 3.11 ou supérieur.
- **Intelligence artificielle :** architecture multi-agents.
- **Cryptographie :** Argon2id, scrypt, bcrypt et PBKDF2-SHA256.
- **Sécurité :** analyse des mécanismes de stockage, pepper et Pwned Passwords.
- **Tests :** pytest et pytest-cov.
- **Gestion des versions :** Git et GitHub.
- **Intégration continue :** GitHub Actions.

## Installation

### Prérequis

- Python 3.11 ou supérieur.
- Git.

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
.venv\Scripts\Activate.ps1
```

Sous Linux ou macOS :

```bash
source .venv/bin/activate
```

### 4. Installer les dépendances

```bash
python -m pip install -e ".[dev]"
```

## Configuration

Un fichier `.env.example` est fourni comme modèle de configuration.

Pour créer un fichier local :

```powershell
Copy-Item .env.example .env
```

Renseigner les variables nécessaires dans le fichier `.env`.

**Important :** ne jamais publier de secrets, de clés ou de valeurs sensibles dans le dépôt GitHub.

## Utilisation

Après l'installation, les fonctionnalités sont accessibles depuis le terminal avec la commande `hash-audit`.

### Afficher les commandes disponibles

```powershell
hash-audit --help
```

### 1. Auditer un fichier Python

```powershell
hash-audit audit chemin/vers/fichier.py
```

Les résultats comprennent les détections et les traces d'exécution. La trace est également enregistrée dans `traces/latest.jsonl`.

### 2. Générer les fichiers de test

```powershell
hash-audit mutations
```

Les fichiers Python synthétiques et le fichier `ground_truth.json` sont générés dans `data/mutations`.

### 3. Auditer les fichiers de test

```powershell
hash-audit audit-batch
```

Le rapport est enregistré dans `results/mutation_audit.json`.

Pour personnaliser les chemins :

```powershell
hash-audit audit-batch --input data/mutations --out results/mon_rapport.json
```

### 4. Générer un jeu de données de comptes

```powershell
hash-audit dataset
```

Le résultat est enregistré dans `results/accounts.json`.

### 5. Simuler une migration

```powershell
hash-audit migration
```

Le résultat est enregistré dans `results/migration.json`.

Les chemins de sortie peuvent être personnalisés avec l'option `--out`.

## Tests

### Exécuter les tests

```bash
python -m pytest -q
```

### Mesurer la couverture de code

```bash
python -m pytest --cov=src/hash_audit --cov=app --cov-report=term-missing
```

## Résultats de validation

Derniers résultats locaux mesurés le 12 novembre 2026 :

- **66 tests réussis.**
- **87 % de couverture de code.**
- Intégration continue vérifiée avec GitHub Actions.
- Audit de 25 fichiers Python synthétiques avec une détection de 100 % sur les cas de test contrôlés.

Le taux de détection correspond aux mutations synthétiques évaluées et ne constitue pas une garantie de performance dans un environnement de production.

## Sécurité et limites

- Les données utilisées sont synthétiques.
- Les résultats obtenus sur les 25 fichiers de test ne garantissent pas une détection parfaite en environnement de production.
- Les performances des algorithmes dépendent du matériel utilisé.
- La simulation de migration sur 90 jours est statistique et ne représente pas une migration réelle.
- La vérification des mots de passe compromis est facultative.
- Une validation humaine reste nécessaire avant toute utilisation en production.

Ce projet constitue un outil expérimental et pédagogique. Il ne remplace pas un audit de sécurité réalisé dans un environnement réel.

## Documentation

Les documents complémentaires sont disponibles à la racine du dépôt :

- [AUDIT.md](AUDIT.md) : méthodologie et résultats de l'audit.
- [SYSTEM_CARD.md](SYSTEM_CARD.md) : présentation et fonctionnement du système.
- [AI_USAGE.md](AI_USAGE.md) : documentation de l'utilisation de l'intelligence artificielle.

## Licence

Ce projet est distribué sous licence MIT.

Consultez le fichier [LICENSE](LICENSE).

## Version

**Version actuelle : v1.0.0**

[Consulter la dernière version](https://github.com/imeldamague/hash-audit-ai/releases/latest)

## Auteur

**Imelda Magué**

GitHub : [@imeldamague](https://github.com/imeldamague)

Dépôt du projet : [Hash-Audit AI](https://github.com/imeldamague/hash-audit-ai)
