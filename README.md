
# Hash-Audit AI

**Système d'intelligence artificielle multi-agents pour l'audit de sécurité des mécanismes de hachage et de stockage des mots de passe.**

## Présentation

Hash-Audit AI est un projet de cybersécurité et d'IA agentique conçu pour analyser les pratiques de stockage des mots de passe, détecter des mécanismes de hachage faibles et proposer des recommandations de sécurisation.

Le projet combine des mécanismes d'audit de sécurité, des expérimentations cryptographiques et une architecture multi-agents afin d'évaluer les risques associés au stockage des mots de passe.

## Fonctionnalités

- Jeu de données synthétique de 1 000 comptes.
- Analyse de MD5, SHA-256 salé et Argon2id.
- Architecture composée de six agents spécialisés et d'un orchestrateur.
- Audit de 25 fichiers Python synthétiques.
- Simulation d'attaque par dictionnaire.
- Comparaison d'Argon2id, scrypt, bcrypt et PBKDF2-SHA256.
- Gestion du pepper.
- Vérification facultative des mots de passe compromis avec Pwned Passwords et le mécanisme k-anonymity.
- Simulation statistique d'une migration sur 90 jours.
- Génération de résultats et de traces d'audit.

## Architecture

Le système repose sur six agents spécialisés coordonnés par un orchestrateur :

1. Agent explorateur : collecte et analyse les données.
2. Agent identificateur : identifie les mécanismes de hachage.
3. Agent évaluateur : évalue les risques de sécurité.
4. Agent correcteur : propose des recommandations de sécurisation.
5. Agent testeur : vérifie les résultats et les corrections.
6. Agent auditeur : contrôle et synthétise les résultats.

## Technologies utilisées

- **Langage :** Python 3.11 ou supérieur.
- **Intelligence artificielle :** architecture multi-agents.
- **Cryptographie :** Argon2id, scrypt, bcrypt et PBKDF2-SHA256.
- **Sécurité :** analyse des mécanismes de stockage, pepper et Pwned Passwords.
- **Tests :** pytest et pytest-cov.
- **Gestion de versions :** Git et GitHub.
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

L'application et ses fonctionnalités peuvent être lancées depuis l'environnement virtuel après installation des dépendances.

Les résultats des audits et les traces d'exécution sont enregistrés dans les répertoires prévus à cet effet dans le projet.

## Tests

### Exécuter les tests

```bash
python -m pytest -q
```

### Mesurer la couverture de code

```bash
python -m pytest --cov=src/hash_audit --cov=app --cov-report=term-missing
```

### Résultats de validation

Derniers résultats locaux mesurés le 12 novembre 2026 :

- **66 tests réussis.**
- **87 % de couverture de code.**
- Intégration continue vérifiée avec GitHub Actions.

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

[Consulter la dernière release](https://github.com/imeldamague/hash-audit-ai/releases/tag/v1.0.0)

## Auteur

**Imelda Magué**

- GitHub : [@imeldamague](https://github.com/imeldamague)
- Dépôt du projet : [Hash-Audit AI](https://github.com/imeldamague/hash-audit-ai)
